from pprint import pprint

from ._simplify import to_simple_tag
from .. import is_hangle
from .. import is_jaum
from .. import is_moum
from .. import compose
from .. import decompose


def remove_symbol(eojeol, morphtags):
    symbols = {morph for morph, tag in morphtags if tag[0] == 'S'}
    for s in symbols:
        eojeol = eojeol.replace(s, '')
    morphtags = [(morph, tag) for morph, tag in morphtags
                 if (not tag[0] == 'S') and (not '(' in morph)]
    return eojeol, morphtags

def eojeol_morphtags_sentence_to_lr(sent, separate_xsv=True):

    def format_check(lr):
        if not lr[0] or not lr[2]:
            return False
        if (lr[1] and not lr[3]) or (not lr[1] and lr[3]):
            return False
        return True

    try:
        sent_ = []
        for eojeol, morphtags in sent:
            if [morph for morph, tag in morphtags if not morph]:
                continue
            lr = eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv)
            sent_.append(lr[0])
            if len(lr) == 2:
                sent_.append(lr[1])
        # (l_word, r_word, l_tag, r_tag)
        sent_ = [lr for lr in sent_ if format_check(lr)]
        return sent_
    except Exception as e:
        message = str(e) + '\n' + '{}'.format(sent)
        raise ValueError(message)

def eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv=True):

    eojeol, morphtags = remove_symbol(eojeol, morphtags)

    if eojeol in _hard_code:
        return _hard_code[eojeol]

    return _eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv)

_hard_code = {
    '못지': ('못지', '', 'Adverb', ''),
    '그런지는': ('그렇', 'ㄴ지는', 'Adjective', 'Eomi'),
    '어떤질': ('어떠하', 'ㄴ질', 'Adjective', 'Eomi'),
    '짝짝짝두': ('짝짝짝', '두', 'Noun', 'Josa'),
}

def _eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv=True):
    if not eojeol or not morphtags:
        return (('', '', '', ''), )

    first_tag = to_simple_tag(morphtags[0][1])
    if first_tag == 'Josa' or first_tag == 'Eomi':
        return ((eojeol, '', first_tag, ''), )

    # 일/NR + 년NNG
    last_tag = to_simple_tag(morphtags[-1][1])
    if last_tag == 'Noun':
        return ((eojeol, '', 'Noun', ''), )

    if len(morphtags) == 1:
        return ((eojeol, '', to_simple_tag(morphtags[0][1]), ''), )

    if len(morphtags) == 2:
        return (reformat(eojeol, morphtags, 0, first_tag), )

    # XSV (동사형 파생 접미사), XSA: 형용사형 파생 접미사 -> 독립어절
    # 생각했어요-> (('생각', '', 'Noun', ''), ('하', '았어요', 'Verb', 'Eomi'))
    #   [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')]
    # 생각하다-> (('생각', '', 'Noun', ''), ('하', '다', 'Verb', 'Eomi'))
    #   [('생각', 'NNP'), ('하', 'XSV'), ('다', 'EF')]
    for tag in 'XSV XSA VCP VCN'.split():
        tag_i = last_tag_index(morphtags, tag, use_simple=False)
        if tag_i > 0 and to_simple_tag(morphtags[tag_i-1][1]) == 'Noun':
            if separate_xsv:
                eojeol0 = ''.join(w for w, _ in morphtags[:tag_i])
                eojeol1 = eojeol[len(eojeol0):]
                lr0 = (eojeol0, '', 'Noun', '')
                lr1 = reformat(eojeol1, morphtags[tag_i:], 0, to_simple_tag(tag))
                return (lr0, lr1)
            else:
                return (reformat(eojeol, morphtags, tag_i, to_simple_tag(tag)), )

    for tag in 'Noun Pronoun Number Verb Adjective'.split():
        tag_i = last_tag_index(morphtags, tag)
        if tag_i >= 0:
            # 어쩌구 [['어찌', 'MAG'], ['하', 'XSV'], ['구', 'EC']]
            if morphtags[tag_i] == ['하', 'XSV'] and to_simple_tag(morphtags[tag_i-1][1]) == 'Adverb':
                l = ''.join(w for w, _ in morphtags[:tag_i+1])
                r = ''.join(w for w, _ in morphtags[tag_i+1:])
                return l, r, tag, 'Eomi'
            return (reformat(eojeol, morphtags, tag_i, tag), )

    # 지금/MAG + 도/JX
    # XX/UNC + 를/JKO
    # 그래/IC + 요/JX
    for tag in 'Adverb Unk Exclamation'.split():
        tag_i = last_tag_index(morphtags, tag)
        if (tag_i >= 0):
            if tag_i + 1== len(morphtags):
                return ((eojeol, '', tag, ''), )
            if ((to_simple_tag(morphtags[tag_i+1][1]) == 'Josa') or
                (to_simple_tag(morphtags[tag_i+1][1]) == 'Eomi')
               ):
                return (reformat(eojeol, morphtags, tag_i, 'Noun', 'Josa'), )

    second_tag = to_simple_tag(morphtags[1][1])
    if second_tag == 'Josa':
        return (reformat(eojeol, morphtags, 0, 'Noun', 'Josa'), )
    raise ValueError('Exception: eojeol = {}, morphtag = {}'.format(eojeol, morphtag))

def last_tag_index(morphtags, tag, use_simple=True):
    last_index = -1
    for i, (morph, tag_) in enumerate(morphtags):
        if use_simple and to_simple_tag(tag_) == tag:
            last_index = i
        elif not use_simple and tag_ == tag:
            last_index = i
    return last_index

def split_index(eojeol, morphtag, index, tag):
    compound = False
    if tag == 'Verb' or tag == 'Adjective' and index > 0:
        for _, t in morphtag[:index]:
            if t == 'VV' or t == 'VA':
                compound = True
    if compound:
        following_subword = ''.join([remove_jamo(morph) for morph, tag in morphtag[index+1:]])
        return len(eojeol) - len(following_subword)
    previous_subword = ''.join([remove_jamo(morph) for morph, tag in morphtag[:index+1]])
    return len(previous_subword)

def remove_jamo(morph):
    return ''.join(c for c in morph if not (is_jaum(c) or is_moum(c)))

def reformat(eojeol, morphtags, tag_i, l_tag, r_tag_=None):
    if tag_i == len(morphtags)-1:
        return eojeol, '', l_tag, ''

    # 오고, [['들어오', 'VV'], ['고', 'EC']]
    # 맞이해, [['맞이하', 'VV'], ['여', 'EC']]
    if len(morphtags) == 2 and is_hangle(morphtags[1][0][0]):
        l, r = morphtags[0][0], morphtags[1][0]
        l_tag = to_simple_tag(morphtags[0][1])
        r_tag = to_simple_tag(morphtags[1][1])
        return l, r, l_tag, r_tag

    s_index = split_index(eojeol, morphtags, tag_i, l_tag)

    l = eojeol[:s_index]
    r = eojeol[s_index:]

    # use last character of morphtag[tag_i]
    # 따라 [['따르', 'VV'], ['ㅏ', 'EC']]
    l = l[:-1] +  morphtags[tag_i][0][-1]
    
    first_word = morphtags[tag_i+1][0] # R parts 의 첫 단어
    first_char = first_word[0]     # R parts 의 첫 글자
    second_char = '' if len(first_word) == 1 else first_word[1]      # R parts 의 두번째 글자
    second_word = '' if tag_i+2 == len(morphtags) else morphtags[tag_i+2][0] # R parts 의 두번째 단어
    rconcat = ''.join(m for m, t in morphtags[tag_i+1:])
    rsubword = eojeol[len(l):]

    """
    print('eojeol: %s'%eojeol)
    print('s_index: {}'.format(s_index))
    print('morphtags: {}'.format(morphtags))
    print('tag_i: {}'.format(tag_i))
    print('l_tag: {}'.format(l_tag))
    print('modified l = {}'.format(l))
    print('original r = {}'.format(r))
    print('first_word: {}'.format(first_word))
    print('first_char: {}'.format(first_char))
    print('second_char: {}'.format(second_char))
    print('second_word: {}'.format(second_word))
    """

    if (l_tag == 'Verb' or l_tag == 'Adjective'):
        # 다해, [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']]
        if not r:
            r = first_word
        # 통해서, [['통하', 'VV'], ['ㅕ서', 'EC']]
        elif l[-1] == '하' and r[0] == '여':
            r = '아' + r[1:]
        else:
            # 예외적인, [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']]
            if is_jaum(first_char):
                r = first_char + rsubword
            # 느꼈으니, [['느끼', 'VV'], ['었', 'EP'], ['으니', 'EC']]
            elif rsubword == rconcat[1:]:
                r = rconcat[0] + rsubword
            # 거셨을, [('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')]
            elif rsubword[1:] == rconcat[2:]:
                r = rconcat[:2] + rsubword[1:]
            # ('반가우면서도', [['반갑', 'VA'], ['면서', 'EC'], ['도', 'JX']]),
            elif rsubword[1:] == rconcat:
                r = rsubword[0] + rconcat
            else:
                r = morphtags[tag_i+1][0][0] + rsubword[1:]

    # post-processing
    if len(r) > 0 and is_moum(r[0]):
        r = compose('ㅇ', r[0], ' ') + r[1:]
    if len(r) > 1 and is_jaum(r[1]):
        cjj = decompose(r[0])
        r = compose(cjj[0], cjj[1], r[1]) + r[2:]
    elif len(r) > 1 and (r[1] == '이' or r[1] == 'ㅣ'):
        if is_hangle(r[0]):
            cjj = decompose(r[0])
            if cjj[1] == 'ㅣ' and cjj[2] == ' ':
                r = r[0] + r[2:]
    elif len(r) > 1 and is_moum(r[1]):
        r = r[0] + compose('ㅇ', r[1], ' ') + r[2:]

    if l_tag == 'Noun':
        r_tag = 'Josa'
    else:
        r_tag = to_simple_tag(morphtags[tag_i+1][1])

    if r_tag_ is not None:
        r_tag = r_tag_

    return l, r, l_tag, r_tag