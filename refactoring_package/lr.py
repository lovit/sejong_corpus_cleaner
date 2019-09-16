from ._lr_rules import _rules
from .simple_tag import to_simple_tag
from .loader import MorphTag
from .utils import is_jaum, is_moum, is_hangle, compose, decompose

def to_lr(eojeol, morphtags, noun_xsv_as_verb=False, rules=None, debug=False):
    """
    Arguments
    ---------
    eojeol : str
        Eojeol text
    morphtags : list of MorphTag
        list of namedtuple of (morpheme, tag)
    noun_xsv_as_verb : Boolean
        For a morpheme, tag sequence "시작/NNG + 하/XSV + ㄴ다/EP"
        If True, it returns "시작하/Verb + ㄴ다/Eomi"
        Else it returns "시작/Noun + 한다/Verb"
    rules : dict
        L, R tramsform rules
        {eojeol: ((L morph, L tag), (R morph, R tag))}
    debug : Boolean
        If True, it shows local variables.

    Returns
    -------
    preprocessed_eojeol : str
        Eojeol text after removing symbols
    l : MorphTag
        namedtuple of (morph, tag) in L-R format
    r : MorphTag
        namedtuple of (morph, tag) in L-R format
    """

    # ('6.25', [('6', 'SN'), ('.', 'SF'), ('25', 'SN')], 2),
    # ('6.25의', [('6', 'SN'), ('.', 'SF'), ('25', 'SN'), ('의', 'JKO')], 2),
    eojeol_, l, r = transform_symbol_noun(eojeol, morphtags, debug)
    if l is not None:
        return eojeol_, l, r

    eojeol_, morphtags = preprocess(eojeol, morphtags)
    if (not eojeol) or (not morphtags):
        if debug:
            message = 'Filtered by preprocessor. eojeol = {}, morphtags = {}'.format(
                eojeol, morphtags)
            raise ValueError(message)
        return eojeol_, None, None

    l, r = transform_with_rules(eojeol_, morphtags, rules=None, debug=debug)
    if l is not None:
        return eojeol_, l, r

    # prepare materials
    morphs = [mt.morph for mt in morphtags]
    tags = [mt.tag for  mt in morphtags]
    simple_tags = [to_simple_tag(tag) for tag in tags]

    l, r = transform_uni_morphtag(eojeol_, morphs, tags, simple_tags, debug)
    if l is not None:
        return eojeol_, l, r

    # 전성 어미가 존재할 경우.
    # noun_xsv_as_verb = True 이면 "시작/NNG + 하/XSV + ㄴ다/EP" -> "시작하/Verb + ㄴ다/Eomi"
    # noun_xsv_as_verb = False 이면 "시작/Noun + 한다/Verb" 로 변형한다.
    l, r = transform_when_noun_is_changed_to_predicator(
        eojeol_, morphs, tags, simple_tags, noun_xsv_as_verb, debug)
    if l is not None:
        return eojeol_, l, r

    l, r = transform_normal_case(eojeol_, morphs, tags, simple_tags, debug)
    if l is not None:
        return eojeol_, l, r

    l, r = transform_exceptional_case(eojeol_, morphs, tags, simple_tags, debug)
    if l is not None:
        return eojeol_, l, r

    message = 'Exception: Eojeol = {}, morphtags = {}'.format(eojeol, morphtags)
    print(eojeol_, morphtags)
    raise ValueError(message)

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
        return '(' in morph or ')' in morph or (tag[0] == 'S' and tag != 'SN') or tag[:1] == 'NA'

    eojeol_ = eojeol
    morphtags_ = []
    for morphtag in morphtags:
        if is_useless(morphtag.morph, morphtag.tag):
            eojeol_ = eojeol_.replace(morphtag.morph, '', 1)
        else:
            morphtags_.append(morphtag)
    return eojeol_, morphtags_

def transform_symbol_noun(eojeol, morphtags, debug=False):
    def all_are_number_or_symbol(simple_tags, i):
        for t in simple_tags[:i+1]:
            if not (t == 'Number' or t == 'Symbol'):
                return False
        return True

    simple_tags = [to_simple_tag(mt.tag) for mt in morphtags]
    morphs = [mt.morph for mt in morphtags]
    i = rindex(simple_tags, {'Number', 'Symbol'})
    if i >= 1 and all_are_number_or_symbol(simple_tags, i) and simple_tags[i] == 'Number':
        if debug:
            print('called transform_symbol_noun')
        morph_l = ''.join(morphs[:i+1])
        morph_r = eojeol[len(morph_l):]
        l = MorphTag(morph_l, 'Noun')
        r = MorphTag(morph_r, simple_tags[i+1]) if morph_r else None
        return eojeol, l, r
    return eojeol, None, None

def transform_with_rules(eojeol, morphtags, rules=None, debug=False):
    if to_simple_tag(morphtags[-1].tag) == 'Noun':
        if debug:
            print('called transform_with_rules')
        return (MorphTag(eojeol, 'Noun'), None)
    if rules is None:
        rules = _rules
    l, r = rules.get(eojeol, (None, None))
    if l is not None and debug:
        print('called transform_with_rules')
    return l, r

def transform_uni_morphtag(eojeol, morphs, tags, simple_tags, debug=False):
    if len(morphs) == 1:
        if debug:
            print('called transform_uni_morphtag')
        return (MorphTag(morphs[0], simple_tags[0]), None)
    return None, None

def transform_when_noun_is_changed_to_predicator(
    eojeol, morphs, tags, simple_tags, noun_xsv_as_verb, debug=False):
    """XSV, XSA, VCP, VCN 과 같은 전성어미가 존재하는 경우"""

    for target in 'XSV XSA VCP VCN'.split():
        i = rindex(tags, target)
        if not (i > 0 and simple_tags[i-1] == 'Noun'):
            continue
        if debug:
            print('called transform_when_noun_is_changed_to_predicator')
        if noun_xsv_as_verb:
            return lr_form(eojeol, morphs, tags, simple_tags, i, debug)
        else:
            return lr_form(eojeol, morphs, tags, simple_tags, i-1, debug)
    return None, None

def transform_normal_case(eojeol, morphs, tags, simple_tags, debug=False):
    for target in 'Noun Pronoun Numeral Verb Adjective'.split():
        i = rindex(simple_tags, target)
        if i >= 0:
            if debug:
                print('called transform_normal_case')
            return lr_form(eojeol, morphs, tags, simple_tags, i, debug)
    return None, None

def transform_exceptional_case(eojeol, morphs, tags, simple_tags, debug=False):
    for target in 'Adverb Unk Exclamation Number Determiner'.split():
        i = rindex(simple_tags, target)
        if i < 0:
            continue
        if debug:
            print('called transform_exceptional_case')
        if target == 'Number':
            if i == 0:
                return lr_form(eojeol, morphs, tags, simple_tags, i, tag_l='Number')
            else:
                return lr_form(eojeol, morphs, tags, simple_tags, i, tag_l='Noun')
        if i == len(tags) - 1:
            return lr_form(eojeol, morphs, tags, simple_tags, i)
        elif simple_tags[i+1] == 'Josa':
            return lr_form(eojeol, morphs, tags, simple_tags,
                i, debug, tag_l='Noun', tag_r='Josa')
    return None, None

def rindex(tags, target):
    """
    Arguments
    ---------
    tags : list of str
        Tag list
    target : str or set of str
        A target tag or tagset

    Usage
    -----
        >>> rindex(['a', 'b', 'c', 'a', 'b'], target='a') # 3
        >>> rindex(['a', 'b', 'c', 'a', 'b'], target='c') # 2
        >>> rindex(['a', 'b', 'c', 'a', 'b'], target={'b', 'c'}) # 4
    """
    def match(tag_i, target):
        if isinstance(target, str):
            return tag_i == target
        return tag_i in target

    n = len(tags)
    for i, tag_i in enumerate(tags[::-1]):
        if match(tag_i, target):
            return n - i - 1
    return -1

def lr_form(eojeol, morphs, tags, simple_tags, i, debug=False, tag_l=None, tag_r=None):
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
    debug : Boolean
        If True, print variables using for transforming morphemes to L-R structure
    tag_l : str or None
        User specified tag
    tag_r : str or None
        User specified tag

    Returns
    -------
    l, r : tuple of MorphTag
        The length of tuple is 2. The value of r is null if R is empty
    """

    n = len(morphs)
    if i == (n-1):
        if tag_l is None:
            tag_l = simple_tags[-1]
        return (MorphTag(eojeol, tag_l), None)

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

    if tag_l is None:
        tag_l = simple_tags[i]
    if tag_r is None:
        tag_r = simple_tags[i+1] if i < (n-1) else None

    # use last character of morphs
    # 따라 [['따르', 'VV'], ['ㅏ', 'EC']]
    morph_l = surface_l[:-1] +  morphs[i][-1]

    if tag_l == 'Verb' or tag_l == 'Adjective' or tag_l == 'Noun' or tag_l == 'Numeral':
        morph_r = lemmatize_r(eojeol, surface_l, surface_r, morph_l, tag_l, morphs, i, debug)
    else:
        morph_r = surface_r

    if debug:
        print('[surface / morph / tag]')
        print('[{} / {} / {}]'.format(surface_l, morph_l, tag_l))
        print('[{} / {} / {}]'.format(surface_r, morph_r, tag_r))

    return MorphTag(morph_l, tag_l), MorphTag(morph_r, tag_r)

def lemmatize_r(eojeol, surface_l, surface_r, morph_l, tag_l, morphs, i, debug=False):
    """
    eojeol : str
        Eojeol
    surface_l : str
        Surfacial form of L
    surface_r : str
        Surfacial form of R
    morph_l : str
        Canonical form of L
    tag_l : str
        Simple tag of L
    morphs : list of str
        Canonical form of morphemes
    i : int
        Last position of L in morphs
    debug : Boolean
        If True, it shows components
    """
    w0 = morphs[i+1] # first morph of R
    c0 = w0[0]       # firsr character of R
    c1 = '' if len(w0) == 1 else w0[1] # second character of R
    concat_r = ''.join(morphs[i+1:])

    if debug:
        print('eojeol    : {}'.format(eojeol))
        print('surface_l : {}'.format(surface_l))
        print('surface_r : {}'.format(surface_r))
        print('morph_l   : {}'.format(morph_l))
        print('tag_l     : {}'.format(tag_l))
        print('morphs    : {}'.format(morphs))
        print('i         : {}'.format(i))
        print('w0        : {}'.format(w0))
        print('c0, c1    : {}'.format(c0, c1))
        print('concat_r  : {}'.format(concat_r))

    ###############
    # lemmatizing josa #
    if tag_l == 'Noun':
        if c0 and is_jaum(c0):
            return c0 + surface_r
        else:
            return surface_r

    ###############
    # lemmatizing eomis #

    # 활용시 2음절이 1음절로 변하는 경우 (1음절 R 이 합쳐진 경우)
    # 복원시 1음절을 2음절로 확장
    # ('다해', [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']])
    if not surface_r:
        morph_r = w0

    # 활용시 2음절이 1음절이 변하는 경우 (1음절 L 과 1음절 R 이 합쳐진 경우, -하다 동사류)
    # 복원시 1음절을 2음절 (1음절 L 과 1음절 R) 로 확장
    # ('통해서', [['통하', 'VV'], ['ㅕ서', 'EC']])
    elif morph_l[-1] == '하' and (c0 == '여' or c0 == 'ㅕ' or c0 == '어' or c0 == 'ㅓ'):
        morph_r = '아' + surface_r

    # 활용시 2음절이 1음절이 변하는 경우 (2음절 R 이 1음절로 축약된 경우, -하다 동사류 외)
    # 복원시 1음절을 2음절 (1음절 L 과 1음절 R) 로 확장
    # ('느꼈으니', [['느끼', 'VV'], ['었', 'EP'], ['으니', 'EC']])
    elif surface_r == concat_r[1:]:
        morph_r = c0 + surface_r

    # 활용시 첫글자가 자음인 R 이 L 에 병합된 경우
    # 복원시 R 의 자음을 surface 에 부착
    # ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']])
    elif is_jaum(c0):
        morph_r = c0 + surface_r

    # 활용시 R 에 1음절이 추가된 경우
    # 복원시 R 에 추가된 음절을 포함
    # ('반가우면서도', [['반갑', 'VA'], ['면서', 'EC'], ['도', 'JX']]),
    elif surface_r[1:] == concat_r:
        morph_r = surface_r[0] + concat_r

    # 활용시 1음절의 L 과 2음절의 R 이 각각 활용된 1음절과 축약된 1음절로 변형된 경우
    # 복원시 L 의 마지막 음절을 복원하고, R 의 첫음절을 두 개의 음절로 복원
    # ('거셨을', [('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')])
    elif surface_r[1:] == concat_r[2:]:
        morph_r = concat_r

    else:
        morph_r = c0 + surface_r[1:]

    ##################
    # postprocessing #

    # R 의 첫글자가 모음인 경우
    # 통해서, [['통하', 'VV'], ['ㅏ서', 'EC']]
    if len(morph_r) > 0 and is_moum(morph_r[0]):
        morph_r = compose('ㅇ', morph_r[0], ' ') + morph_r[1:]

    if len(morph_r) > 1 and is_hangle(morph_r[0]):
        cjj = decompose(morph_r[0])
        # R 의 두번째 글자가 자음인 경우
        if is_jaum(morph_r[1]):
            morph_r = compose(cjj[0], cjj[1], morph_r[1]) + morph_r[2:]
        # R 의 두번째 글자가 모음인 경우
        if len(morph_r) > 1 and is_moum(morph_r[1]):
            morph_r = morph_r[0] + compose('ㅇ', morph_r[1], ' ') + morph_r[2:]
        # R 의 첫번째 글자와 두번째 글자가 이ㅣ 로 중복된 경우
        if len(morph_r) > 1 and (morph_r[1] == '이' or morph_r[1] == 'ㅣ') and (cjj[1] == 'ㅣ' and cjj[2] == ' '):
            morph_r = morph_r[0] + morph_r[2:]

    return morph_r
