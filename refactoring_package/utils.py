import os
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

    # OSX
    if os.environ['_system_name'] == 'OSX':
        encodings = [subprocess.getstatusoutput("file -I %s" % path)[1] for path in paths]
    # Ubuntu
    else:
        encodings = [subprocess.getstatusoutput("file %s" % path)[1] for path in paths]
    return encodings

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

    # 원형 L 마지막 음절의 초/중/종성
    cho_l, jung_l, jong_l = decompose(l[0][-1])
    # 원형 R 첫음절의 초/중/종성
    if not r:
        cho_r, jung_r, jong_r = ('', '', '')
    elif is_jaum(r[0][0]):
        cho_r, jung_r, jong_r = ('', '', r[0][0])
    else:
        cho_r, jung_r, jong_r = decompose(r[0][0])

    b = len(l[0])
    l_, r_ = eojeol[:b], eojeol[b:]
    cho_l_, jung_l_, jong_l_ = decompose(l_[-1]) # 표현형 L 마지막 음절의 초/중/종성
    cho_r_, jung_r_, jong_r_ = decompose(r_[0]) if r_ else ('', '', '') # 표현형 R 첫음절의 초/중/종성

    if debug:
        print('Surfacial form : {} + {}'.format(l_, r_))
        print('Canonical form : {} + {}'.format(l, r))
        print('cho/jung/jong of L_surf = ({}, {}, {})'.format(cho_l_, jung_l_, jong_l_))
        print('cho/jung/jong of L_canon = ({}, {}, {})'.format(cho_l, jung_l, jong_l))
        print('cho/jung/jong of R_surf = ({}, {}, {})'.format(cho_r_, jung_r_, jong_r_))
        print('cho/jung/jong of R_canon = ({}, {}, {})'.format(cho_r, jung_r, jong_r))

    # ('어제는', ('어제', 'Noun'), ('는', 'Josa'))
    # ('어제는', ('어제', 'Noun'), None)
    if (l_ == l[0]) and ((not r) or (r_ == r[0])):
        return True

    # ('스쳐갔다', ('스쳐가', 'Verb'), ('았다', 'Eomi'))
    if (l_[:-1] == l[0][:-1]) and (cho_l_ == cho_l) and (jong_l_ == jong_r):
        return True

    return False
