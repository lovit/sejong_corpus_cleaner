from refactoring_package._lr_rules import _rules
from refactoring_package.simple_tag import to_simple_tag
from refactoring_package.loader import MorphTag
from refactoring_package.utils import is_jaum, is_moum

def to_lr(eojeol, morphtags, xsv_as_verb=False, rules=None):
    lr_morphemes = morphtags_to_lr(eojeol, morphtags, xsv_as_verb, rules)
    return None

def morphtags_to_lr(eojeol, morphtags, xsv_as_verb=False, rules=None):

    eojeol, morphtags = preprocess(eojeol, morphtags)
    if (not eojeol) or (not morphtags):
        message = 'Filtered by preprocessor. eojeol = {}, morphtags = {}'.format(
            eojeol, morphtags)
        raise ValueError(message)

    l, r = transform_with_rules(eojeol, morphtags, rules=None)
    if l is not None:
        return l, r

    # prepare materials
    morphs = [mt.morph for mt in morphtags]
    tags = [mt.tag for  mt in morphtags]
    simple_tags = [to_simple_tag(tag) for tag in tags]

    l, r = transform_with_short_morphtags(eojeol, morphs, tags, simple_tags)
    if l is not None:
        return l, r

    # 전성 어미가 존재할 경우.
    # xsv_as_verb = True 이면 "시작/NNG + 하/XSV + ㄴ다/EP" -> "시작하/Verb + ㄴ다/Eomi"
    # xsv_as_verb = False 이면 "시작/Noun + 한다/Verb" 로 변형한다.
    l, r = transform_when_noun_is_changed_to_predicator(
        eojeol, morphs, tags, simple_tags, xsv_as_verb)
    if l is not None:
        return l, r

    l, r = basic(eojeol, morphs, tags, simple_tags)
    if l is not None:
        return l, r
#     raise NotImplemented

def preprocess(eojeol, morphtags):
    """
    It removes useless morphemes from eojeol and morphtags.

    Arguments
    ---------
    eojeol : str
        Text of eojeol
    morphtags : list of MorphTag

    Returns
    -------
    eojeol : str
        After removing useless morphemes
    morphtags : list of MorphTag
        After removing useless morphemes

    Usage
    -----
        >>> print(sent)
        $ 걔      걔/NP
          두      두/MM
          명이    명/NNB + 이/JKS
          하는    하/VV + 는/ETM
          거야.   거/NNB + (이)/VCP + 야/EF + ./SF

        >>> for eojeol, morphtags in sent:
        >>>     eojeol, morphtags = preprocess(eojeol, morphtags)
        >>>     print(eojeol, morphtags)
        $ 걔 [걔/NP]
          두 [두/MM]
          명이 [명/NNB, 이/JKS]
          하는 [하/VV, 는/ETM]
          거야 [거/NNB, 야/EF]
    """
    def is_useless(morph, tag):
        return '(' in morph or ')' in morph or tag[0] == 'S' or tag[:1] == 'NA'

    eojeol_ = eojeol
    morphtags_ = []
    for morphtag in morphtags:
        if is_useless(morphtag.morph, morphtag.tag):
            eojeol_ = eojeol_.replace(morphtag.morph, '', 1)
        else:
            morphtags_.append(morphtag)
    # TODO: 용언이 두 개가 넘개 존재하는 경우는 띄어쓰기가 되어 있지 않은 상태에서 형태소 분석을 한 것이기 때문에 이를 제외.
    return eojeol_, morphtags_

def transform_with_rules(eojeol, morphtags, rules=None):
    if to_simple_tag(morphtags[-1].tag) == 'Noun':
        return ((eojeol, 'Noun'), ('', ''))
    if rules is None:
        rules = _rules
    return rules.get(eojeol, (None, None))

def transform_with_short_morphtags(eojeol, morphs, tags, simple_tags):
    if len(morphs) == 1:
        return ((morphs[0], simple_tags[0]), ('', ''))
    if len(morphtags) == 2:
        return lr_form(eojeol, morphs, tags, simple_tags, 0)
    return None, None

def transform_when_noun_is_changed_to_predicator(eojeol, morphs, tags, simple_tags, xsv_as_verb):
    """XSV, XSA, VCP, VCN 과 같은 전성어미가 존재하는 경우"""
    for target in 'XSV XSA VCP VCN'.split():
        i = rindex(tags, target)
        if not (i > 0 and simple_tags[i-1] == 'Noun'):
            continue
        if xsv_as_verb:
            return lr_form(eojeol, morphs, tags, simple_tags, i)
        else:
            return lr_form(eojeol, morphs, tags, simple_tags, i-1)
    return None, None

def basic(eojeol, morphs, tags, simple_tags):
    for target in 'Noun Pronoun Number Verb Adjective'.split():
        i = rindex(simple_tags, target)
        if i >= 0:
            return lr_form(eojeol, morphs, tags, simple_tags, i)
    return None, None

def rindex(tags, target):
    n = len(tags)
    for i, tag_i in enumerate(tags[::-1]):
        if tag_i == target:
            return n - i - 1
    return -1

def lr_form(eojeol, morphs, tags, simple_tags, i):
    """
    Arguments
    ---------
    eojeol : str
        Eojeol text
    morphs : list of str
        List of morphemes
    tags : list of str
        List of tags
    simple_tags : list of str
        List of simplified tags
    i : int
        Boundary index between L and R in morphs or tags.
        Last index of L

    Returns
    -------
    l, r : tuple of MorphTag
        The length of tuple is 2. The value of r is null if R is empty
    """

    n = len(morphs)
    if i == (n-1):
        return (MorphTag(eojeol, simple_tags[-1]), None)

    def only_hangle(morph):
        return ''.join(c for c in morph if not (is_jaum(c) or is_moum(c)))

    def surface_boundary():
        def is_compound_predicator():
            for tag in simple_tags[:i]:
                if tag == 'Verb' or tag == 'Adjective':
                    return True
            return False

        morphs_hangle = [only_hangle(morph) for morph in morphs]
        morphs_l_concat = ''.join(morphs_hangle[:i+1])
        morphs_r_concat = ''.join(morphs_hangle[i+1:])

        if is_compound_predicator():
            return len(eojeol) - len(morphs_r_concat)
        else:
            return len(morphs_l_concat)

    b = surface_boundary()
    surface_l, surface_r = eojeol[:b], eojeol[b:]
    tag_l = simple_tags[i]
    tag_r = simple_tags[i+1] if i < (n-1) else None

    # use last character of morphs
    # 따라 [['따르', 'VV'], ['ㅏ', 'EC']]
    morph_l = surface_l[:-1] +  morphs[i][-1]

    if tag_l == 'Verb' or tag_l == 'Adjective' or tag_l == 'Noun':
        morph_r = lemmatize(eojeol, surface_l, surface_r, morph_l, morphs, i)
    else:
        morph_r = surface_r

    print('surface morph tag')
    print('{} / {} / {}'.format(surface_l, morph_l, tag_l))
    print('{} / {} / {}'.format(surface_r, morph_r, tag_r))

    return MorphTag(morph_l, tag_l), MorphTag(morph_r, tag_r)

def lemmatize(eojeol, surface_l, surface_r, morph_l, morphs, i, debug=False):
    w0 = morphs[i+1] # first morph of R
    c0 = w0[0]       # firsr character of R
    c1 = '' if len(w0) == 1 else w0[1] # second character of R
    concat = ''.join(morphs[i+1:])

    if debug:
        print('eojeol : {}'.format(eojeol))
        print('surface_l : {}'.format(surface_l))
        print('surface_r : {}'.format(surface_r))
        print('morph_l : {}'.format(morph_l))
        print('morphs : {}'.format(morphs))
        print('i : {}'.format(i))
        print('w0 : {}'.format(w0))
        print('c0, c1 : {}'.format(c0, c1))
        print('concat : {}'.format(concat))

    # 1음절이 1음절로 변하는 경우 (1음절 R 이 합쳐진 경우)
    # 다해, [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']]
    if not surface_r:
        return w0

    # 2음절이 1음절이 변하는 경우 (2음절 R 이 1음절로 축약된 경우, -하다 동사류)
    # 통해서, [['통하', 'VV'], ['ㅕ서', 'EC']]
    elif morph_l[-1] == '하' and c0 == '여' or c0 == 'ㅕ':
        return '아' + surface_r

    # 2음절이 1음절이 변하는 경우 (2음절 R 이 1음절로 축약된 경우)
    # 느꼈으니, [['느끼', 'VV'], ['었', 'EP'], ['으니', 'EC']]
    elif surface_r == concat[1:]:
        return c0 + surface_r

    # 2음절이 1음절이 변하는 경우 (R 의 첫음절이 자음인 경우)
    # 예외적인, [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']]
    elif is_jaum(c0):
        return c0 + surface_r

    # 1 음절이 2음절로 변하는 경우
    # ('반가우면서도', [['반갑', 'VA'], ['면서', 'EC'], ['도', 'JX']]),
    elif surface_r[1:] == concat:
        return surface_r[0] + concat

    # 3음절이 2음절로 변하는 경우
    # 거셨을, [[('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')]]
    elif surface_r[1:] == concat[2:]:
        return concat[:2] + surface_r[1:]

    else:
        return c0 + surface_r[1:]