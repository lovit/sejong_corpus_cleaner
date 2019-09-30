import os
import sys
import subprocess

sep = os.path.sep
install_path = sep.join(os.path.abspath(__file__).split(sep)[:-1])
data_dir = sep.join(os.path.abspath(__file__).split(sep)[:-2] + ['data', 'raw', ''])

def check_encoding(paths):
    """
    Argument
    --------
    paths : str or list of str
        File path

    Returns
    -------
    encodings : list of str
        File encoding information for each file

    Usage
    -----
    With a file
        >>> check_encoding('../data/raw/written/BTAA0001.txt')
        $ ['../data/raw/written/BTAA0001.txt: text/html; charset=utf-16le']

    With multiple files
        >>> check_encoding(['../data/raw/written/BTAA0001.txt', '../data/raw/colloquial/5CT_0016.txt'])
        $ ['../data/raw/written/BTAA0001.txt: text/html; charset=utf-16le',
           '../data/raw/colloquial/5CT_0016.txt: text/plain; charset=utf-16le']
    """
    if isinstance(paths, str):
        paths = [paths]

    # OS
    if os.name == 'posix':
        encodings = [subprocess.getstatusoutput("file %s" % path)[1] for path in paths]
        return encodings
    else:
        print('Not support to {}'.format(os.name))
        return None

unicode_mapper = {
  'ᆨ': 'ㄱ', # 4520
  'ᆩ': 'ㄲ', # 4521
  'ᆪ': 'ㄳ', # 4522
  'ᆫ': 'ㄴ', # 4523
  'ᆬ': 'ㄵ', # 4524
  'ᆭ': 'ㄶ', # 4525
  'ᆮ': 'ㄷ', # 4526
  'ᆯ': 'ㄹ', # 4527
  'ᆰ': 'ㄺ', # 4528
  'ᆱ': 'ㄻ', # 4529
  'ᆲ': 'ㄼ', # 4530
  'ᆳ': 'ㄽ', # 4531
  'ᆴ': 'ㄾ', # 4532
  'ᆵ': 'ㄿ', # 4533
  'ᆶ': 'ㅀ', # 4534
  'ᆷ': 'ㅁ', # 4535
  'ᆸ': 'ㅂ', # 4536
  'ᆹ': 'ㅄ', # 4537
  'ᆺ': 'ㅅ', # 4538
  'ᆻ': 'ㅆ', # 4539
  'ᆼ': 'ㅇ', # 4540
  'ᆽ': 'ㅈ', # 4541
  'ᆾ': 'ㅊ', # 4542
  'ᆿ': 'ㅋ', # 4543
  'ᇀ': 'ㅌ', # 4544
  'ᇁ': 'ㅍ', # 4545
  'ᇂ': 'ㅎ', # 4546
  'ᄀ': 'ㄱ', # 4352
  'ᄁ': 'ㄲ', # 4353
  'ᄂ': 'ㄴ', # 4354
  'ᄃ': 'ㄷ', # 4355
  'ᄄ': 'ㄸ', # 4356
  'ᄅ': 'ㄹ', # 4357
  'ᄆ': 'ㅁ', # 4358
  'ᄇ': 'ㅂ', # 4359
  'ᄈ': 'ㅃ', # 4360
  'ᄉ': 'ㅅ', # 4361
  'ᄊ': 'ㅆ', # 4362
  'ᄋ': 'ㅇ', # 4363
  'ᄌ': 'ㅈ', # 4364
  'ᄍ': 'ㅉ', # 4365
  'ᄎ': 'ㅊ', # 4366
  'ᄏ': 'ㅋ', # 4367
  'ᄐ': 'ㅌ', # 4368
  'ᄑ': 'ㅍ', # 4369
  'ᄒ': 'ㅎ', # 4370
}

def unicode_character(c):
    return unicode_mapper.get(c, c)

def unicode_sentence(sent):
    """
    Argument
    --------
    sent : str
        Input sentence

    Returns
    -------
    sent : str
        Fix non-unicode character
    """
    return ''.join(unicode_character(c) for c in sent)

hangle_begin = 44032
hangle_end = 55203
chosung_base  = 588
jungsung_base = 28
jaum_begin = 12593
jaum_end = 12622
moum_begin = 12623
moum_end = 12643

chosung_list = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
    'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
    'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

jungsung_list = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
    'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
    'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]

jongsung_list = [
    ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ',
    'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
    'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ',
    'ㅌ', 'ㅍ', 'ㅎ'
]

def is_hangle(c):
    return hangle_begin <= ord(c) <= hangle_end

def is_jaum(c):
    return jaum_begin <= ord(c) <= jaum_end

def is_moum(c):
    return moum_begin <= ord(c) <= moum_end

def compose(chosung, jungsung, jongsung):
    hangle = chr(
        hangle_begin +
        chosung_base * chosung_list.index(chosung) +
        jungsung_base * jungsung_list.index(jungsung) +
        jongsung_list.index(jongsung)
    )
    return hangle

def decompose(c):
    i = ord(c)
    if (jaum_begin <= i <= jaum_end):
        return (c, ' ', ' ')
    if (moum_begin <= i <= moum_end):
        return (' ', c, ' ')
    if not (hangle_begin <= i <= hangle_end):
        return (c, '', '')
    i -= hangle_begin
    cho  = i // chosung_base
    jung = ( i - cho * chosung_base ) // jungsung_base
    jong = ( i - cho * chosung_base - jung * jungsung_base )
    return (chosung_list[cho], jungsung_list[jung], jongsung_list[jong])

def check_lr_transformation(eojeol, l, r, debug=False):
    """
    Arguments
    ---------
    eojeol : str
        Eojeol text
    l : MorphTag or tuple
        (morph, tag) format
    r : MorphTag or tuple
        (morph, tag) format
    debug : Boolean
        If True, debug mode on

    Returns
    -------
    flag : Boolean
        True if the format is right.

    Usage
    -----
        >>> check_testset = [
        >>>     ('어제는', ('어제', 'Noun'), ('는', 'Josa')),
        >>>     ('어제는', ('어제', 'Noun'), None),
        >>>     ('스쳐갔다', ('스쳐가', 'Verb'), ('았다', 'Eomi')),
        >>>     ('밝혀져', ('밝혀지', 'Verb'), ('어', 'Eomi')),
        >>>     ('뭡니까', ('뭡엇', 'Pronoun'), ('까', 'Adjective')),
        >>>     ('뭡니까', ('뭐', 'Pronoun'), ('ㅂ니까', 'Josa')),
        >>> ]
        >>> for test in check_testset:
        >>>     print(test, check_lr_transformation(*test, debug=False))
    """

    if (r is None) or (l[0] + r[0] == eojeol):
        return True

    cho_l_canon, jung_l_canon, jong_l_canon = decompose(l[0][-1]) # 원형 L 마지막 음절의 초/중/종성
    # 원형 R 첫음절의 초/중/종성
    if (not r) or (not r[0]):
        cho_r_canon, jung_r_canon, jong_r_canon = ('', '', '')
    elif is_jaum(r[0][0]):
        cho_r_canon, jung_r_canon, jong_r_canon = ('', '', r[0][0])
    elif is_moum(r[0][0]):
        cho_r_canon, jung_r_canon, jong_r_canon = ('', r[0][0], '')
    else:
        cho_r_canon, jung_r_canon, jong_r_canon = decompose(r[0][0])

    b = len(l[0])
    l_surf, r_surf = eojeol[:b], eojeol[b:]
    cho_l_surf, jung_l_surf, jong_l_surf = decompose(l_surf[-1]) # 표현형 L 마지막 음절의 초/중/종성
    cho_r_surf, jung_r_surf, jong_r_surf = decompose(r_surf[0]) if r_surf else ('', '', '') # 표현형 R 첫음절의 초/중/종성

    if debug:
        print('Surfacial form : {} + {}'.format(l_surf, r_surf))
        print('Canonical form : {} + {}'.format(l, r))
        print('cho/jung/jong of L_surf = ({}, {}, {})'.format(cho_l_surf, jung_l_surf, jong_l_surf))
        print('cho/jung/jong of L_canon = ({}, {}, {})'.format(cho_l_canon, jung_l_canon, jong_l_canon))
        print('cho/jung/jong of R_surf = ({}, {}, {})'.format(cho_r_surf, jung_r_surf, jong_r_surf))
        print('cho/jung/jong of R_canon = ({}, {}, {})'.format(cho_r_canon, jung_r_canon, jong_r_canon))

    if len(l[0]) + len(r[0]) + 2 < len(eojeol):
        return False

    # ('어제는', ('어제', 'Noun'), ('는', 'Josa'))
    # ('어제는', ('어제', 'Noun'), None)
    if (l_surf == l[0]) and ((not r) or (r_surf == r[0])):
        return True

    # ('당키나', [('당하', 'VA'), ('기', 'ETN'), ('나', 'JX')], False, False)
    #   -> ('당키나', ('당하', 'Adjective') + ('기나', 'Eomi'))
    # ('당치도', [('당하', 'VA'), ('지', 'EC'), ('도', 'JX')], False, False)
    #   -> ('당치도', ('당하', 'Adjective') + ('지도', 'Eomi'))
    if l_surf[-1] in {'키', '치'} and l[0][-1] == '하' and r[0][0] in {'기', '지'} and (l[1] == 'Verb' or l[1] == 'Adjective'):
        return True

    # ('버려야겠다', [('버리', 'VX'), ('어야', 'EC'), ('하', 'VX'), ('겠', 'EP'), ('다', 'EF')], False, False),
    #  -> ('버려야겠다', ('버려야하', 'Verb'), ('겠다', 'Eomi'))
    if (l_surf[:-1] == l[0][:-1]) and (l_surf[-1] + r_surf == r[0]):
        return True

    # ('어째서', [('어찌', 'MAG'), ('하', 'XSV'), ('아서', 'EC')], False, False)
    #  -> ('어째서', ('어찌하', 'Verb'), ('아서', 'Eomi'))
    if (b >= 3) and (l[0][-1] == '하') and (l[0][:-2] == l_surf[:-2]):
        second_cho_surf, second_jung_surf, second_jong_surf = decompose(l_surf[-2])
        second_cho_canon, second_jung_canon, _ = decompose(l[0][-2])
        _, _, first_jong_r_surf = decompose(r[0][0])
        if (second_jung_canon == 'ㅣ') and (second_jong_surf == first_jong_r_surf) and (second_cho_surf == second_cho_canon):
            return True
        #if (second_jung_canon == 'ㅣ') and (compose(second_cho_canon, 'ㅐ', ' ') == l_surf[-2]):
        #    return True

    # ('퍼질고', [('퍼지르', 'VV'), ('고', 'EC')], False, False),
    #   -> ('퍼질고', ('퍼지르', 'Verb'), ('고', 'Eomi'))
    if (b >= 3) and (l_surf[:-2] == l[0][:-2]) and (decompose(l_surf[-2])[:1] == decompose(l[0][-2])[:1]) and (decompose(l_surf[-2])[2] == decompose(l[0][-1])[0]):
        return True

    # ('스쳐갔다', ('스쳐가', 'Verb'), ('았다', 'Eomi'))
    # ('사는', ('살', 'Verb'), ('는', 'Eomi'))
    if (l_surf[:-1] == l[0][:-1]) and (cho_l_surf == cho_l_canon):
        return True

    # ('생각케', [('생각', 'NNG'), ('하', 'XSV'), ('게', 'EC')], False, False),
    if (l[0][-1] == '하') and (r[0][0] == '게') and (l_surf[-1] == '케'):
        return True

    # ('사용토록', [('사용', 'NNG'), ('하', 'XSV'), ('도록', 'EC')], False, False),
    if (l[0][-1] == '하') and (r[0][0] == '도') and (l_surf[-1] == '토'):
        return True

    # ('이뤄진', [('이루어지', 'VV'), ('ㄴ', 'ETM')], False, False)
    # ('이뤄진다고', [('이루어지', 'VV'), ('ㄴ다고', 'EC')], False, False)
    if len(l[0]) >= 3 and r[0] and is_jaum(r[0][0]):
        cho3, jung3, jong3 = decompose(l[0][-3])
        cho2, jung2, jong2 = decompose(l[0][-2])
        cho1, jung1, jong1 = decompose(l[0][-1])
        comb_boundary = compose(cho1, jung1, r[0][0])
        comb_l = compose(cho3, 'ㅝ', ' ')
        if jung3 == 'ㅜ' and jong3 == ' ' and l[0][-2] == '어' and comb_l == l_surf[-2] or comb_l == l_surf[-3]:
            # ('이뤄진', [('이루어지', 'VV'), ('ㄴ', 'ETM')], False, False)
            if comb_boundary == l_surf[-1]:
                return True
            # ('이뤄진다고', [('이루어지', 'VV'), ('ㄴ다고', 'EC')], False, False)
            if (comb_boundary == l_surf[-2]) and (len(r[0]) >= 2) and (l_surf[-1] == r[0][1]):
                return True

    return False

def check_lemmatization(eojeol, l, r):
    """
    Arguments
    ---------
    eojeol : str
        Eojeol
    l : tuple of str
        (morph_l, tag_l)
    r : tuple of str
        (morph_r, tag_r)

    Returns
    -------
    Boolean
        If the eojeol is conjugated it return surface & canon tuple
        Else, it return None

    Usage
    -----
        >>> check_lemmatization('가까웠는데', ('가깝', 'Adjective'), ('었는데', 'Eomi'))
        $ True

        >>> check_lemmatization('가까워지며', ('가까워지', 'Verb'), ('며', 'Eomi'))
        $ True

        >>> check_lemmatization('펴는피는', (('펴', 'Verb'), ('는', 'Eomi'))
        $ False
    """

    if r is None:
        return True

    (lw, lt), (rw, rt) = l, r
    if not (lt == 'Adjective' or lt == 'Verb'):
        return True
    if lw + rw == eojeol:
        return True

    surface = eojeol[len(lw)-1:len(lw)+1]

    # extract_rule('어쩔', '어찌하', 'Verb', '알', 'Eomi')
    # extract_rule('이뤄진', '이루어지', 'Verb', 'ㄴ', 'Eomi')
    if not surface:
        def find_begin(eojeol, lw):
            for i, char in enumerate(eojeol):
                if char != lw[i]:
                    return i
            return i+1
        b = find_begin(eojeol, lw)
        if b == len(eojeol):
            return True
        surface = eojeol[b:]
        canon = (lw[b:], rw[0])
    elif decompose(surface[0])[0] != decompose(lw[-1])[0]:
        return False
    else:
        if len(lw) + len(rw) == len(eojeol):
            canon = (lw[-1], rw[0])
        elif len(lw) + len(rw) > len(eojeol):
            canon = (lw[-1], rw[:2])
        elif len(lw) + len(rw) + 1 == len(eojeol):
            surface = eojeol[len(lw)-1:len(lw)+2]
            canon = (lw[-1], rw[0])
        else:
            return False

    # post-processing: Ignore exception
    if len(surface) == 2 and len(canon[0]) == 1 and len(canon[1]) == 1:
        surf_cho_l = decompose(surface[0])[0]
        surf_cho_r, _, surf_jong_r = decompose(surface[1])
        canon_cho_l = decompose(canon[0][0])[0]
        canon_cho_r, canon_jung_r, canon_jong_r = decompose(canon[1][0])

        # 원형과 표현형의 어간 마지막 글자의 초성이 같은지 확인
        if surf_cho_l != canon_cho_l:
            return False
        # 원형과 표현형의 어미 첫글자의 초성이 같거나, 어미의 첫글자가 자음일 때 종성이 같은지 확인
        if not ((surf_cho_r == canon_cho_r) or (canon_jung_r == ' ' and surf_jong_r == canon_cho_r)):
            if canon_cho_r != 'ㅇ' and not (surf_cho_r == 'ㅊ' and canon_cho_r == 'ㅈ'):
                return False

    return True
