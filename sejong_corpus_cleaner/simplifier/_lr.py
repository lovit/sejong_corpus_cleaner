from pprint import pprint

from ._simplify import to_simple_tag
from .. import is_hangle
from .. import is_jaum
from .. import is_moum
from .. import compose
from .. import decompose


def remove_symbol(eojeol, poses):
    symbols = {pos[0] for pos in poses if pos[1][0] == 'S'}
    for s in symbols:
        eojeol = eojeol.replace(s, '')
    poses = [pos for pos in poses if (not pos[1][0] == 'S') and (not '(' in pos[0])]
    return eojeol, poses

def eojeol_poses_sentence_to_lr(sent):
    try:
        sent_ = [eojeol_pos_to_lr(eojeol, poses) for eojeol, poses in sent]
        return sent_
    except Exception as e:
        print(e)
        pprint(sent)
        return []

def eojeol_pos_to_lr(eojeol, poses):

    eojeol, poses = remove_symbol(eojeol, poses)

    if eojeol in _hard_code:
        return _hard_code[eojeol]

    return _eojeol_pos_to_lr(eojeol, poses)

_hard_code = {
    '못지': ('못지', '', 'Adverb', ''),
    '그런지는': ('그렇', 'ㄴ지는', 'Adjective', 'Eomi'),
    '어떤질': ('어떠하', 'ㄴ질', 'Adjective', 'Eomi'),
    '짝짝짝두': ('짝짝짝', '두', 'Noun', 'Josa'),
}

def _eojeol_pos_to_lr(eojeol, poses):
    if not eojeol or not poses:
        return ('', '', '', '')

    first_tag = to_simple_tag(poses[0][1])
    if first_tag == 'Josa' or first_tag == 'Eomi':
        return (eojeol, '', first_tag, '')

    # 일/NR + 년NNG
    last_tag = to_simple_tag(poses[-1][1])
    if last_tag == 'Noun':
        return (eojeol, '', 'Noun', '')

    if len(poses) == 1:
        return eojeol, '', to_simple_tag(poses[0][1]), ''

    if len(poses) == 2:
        return reformat(eojeol, poses, 0, first_tag)

    for tag in 'Noun Pronoun Number Verb Adjective'.split():
        tag_i = last_tag_index(poses, tag)
        if tag_i >= 0:
            # 어쩌구 [['어찌', 'MAG'], ['하', 'XSV'], ['구', 'EC']]
            if poses[tag_i] == ['하', 'XSV'] and to_simple_tag(poses[tag_i-1][1]) == 'Adverb':
                l = ''.join(w for w, _ in poses[:tag_i+1])
                r = ''.join(w for w, _ in poses[tag_i+1:])
                return l, r, tag, 'Eomi'
            return reformat(eojeol, poses, tag_i, tag)

    # 지금/MAG + 도/JX
    # XX/UNC + 를/JKO
    # 그래/IC + 요/JX
    for tag in 'Adverb Unk Exclamation'.split():
        tag_i = last_tag_index(poses, tag)
        if (tag_i >= 0):
            if tag_i + 1== len(poses):
                return eojeol, '', tag, ''
            if ((to_simple_tag(poses[tag_i+1][1]) == 'Josa') or
                (to_simple_tag(poses[tag_i+1][1]) == 'Eomi')
               ):
                return reformat(eojeol, poses, tag_i, 'Noun', 'Josa')

    second_tag = to_simple_tag(poses[1][1])
    if second_tag == 'Josa':
        return reformat(eojeol, poses, 0, 'Noun', 'Josa')
    raise ValueError('Exception: eojeol = {}, poses = {}'.format(eojeol, poses))

def last_tag_index(poses, tag):
    noun_index = -1
    for i, (w, t) in enumerate(poses):
        if to_simple_tag(t) == tag:
            noun_index = i
    return noun_index

def split_index(poses, index):
    previous_subword = ''.join([remove_jamo(pos[0]) for pos in poses[:index+1]])
    return len(previous_subword)

def remove_jamo(word):
    return ''.join(c for c in word if not (is_jaum(c) or is_moum(c)))

def reformat(eojeol, poses, tag_i, l_tag, r_tag_=None):
    if tag_i == len(poses)-1:
        return eojeol, '', l_tag, ''

    # 오고, [['들어오', 'VV'], ['고', 'EC']]
    # 맞이해, [['맞이하', 'VV'], ['여', 'EC']]
    if len(poses) == 2 and is_hangle(poses[1][0][0]):
        l, r = poses[0][0], poses[1][0]
        l_tag = to_simple_tag(poses[0][1])
        r_tag = to_simple_tag(poses[1][1])
        return l, r, l_tag, r_tag

    s_index = split_index(poses, tag_i)

    l = eojeol[:s_index]
    r = eojeol[s_index:]

    # use last character of poses[tag_i]
    # 따라 [['따르', 'VV'], ['ㅏ', 'EC']]
    l = l[:-1] +  poses[tag_i][0][-1]

    first_word = poses[tag_i+1][0] # R parts 의 첫 단어
    first_char = first_word[0]     # R parts 의 첫 글자
    second_char = '' if len(first_word) == 1 else first_word[1]      # R parts 의 두번째 글자
    second_word = '' if tag_i+2 == len(poses) else poses[tag_i+2][0] # R parts 의 두번째 단어

    # 보내 [['보내', 'VV'], ['ㅓ', 'EC']]
    # 돼요 [['되', 'VV'], ['ㅓ요', 'EF']]
    if not is_hangle(first_char):
        if len(first_word) == 1:
            if is_jaum(first_char):
                r = first_char + r
            elif is_moum(first_char):
                r = compose('ㅇ', first_char, ' ') + r
        elif len(first_word) == 2:
            if is_jaum(first_char) and is_moum(second_char):
                r = compose(first_char, second_char, ' ') + r
            elif is_moum(first_char) and is_jaum(second_char):
                r = compose('ㅇ', first_char, second_char) + r
            elif is_moum(first_char) and is_hangle(second_char):
                r = compose('ㅇ', first_char, ' ') + r
            elif is_jaum(first_char) and is_hangle(second_char):
                r = first_char + r
            else:
                raise ValueError('reformat: check pos : tag_i = {}, poses = {}'.format(tag_i, poses))

    # 했어요 [['하', 'VV'], ['았', 'EP'], ['어요', 'EF']]
    # 예외적인, [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']]
    elif r and (r[0] != first_char) and second_word and is_hangle(second_word[0]):
        r = first_char + r

    if (l_tag == 'Verb' or l_tag == 'Adjective'):
        # 다해, [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']]
        if not r:
            r = first_word
        # 통해서, [['통하', 'VV'], ['ㅕ서', 'EC']]
        elif l[-1] == '하' and r[0] == '여':
            r = '아' + r[1:]

    if l_tag == 'Noun':
        r_tag = 'Josa'
    else:
        r_tag = to_simple_tag(poses[tag_i+1][1])

    if r_tag_ is not None:
        r_tag = r_tag_

    return l, r, l_tag, r_tag