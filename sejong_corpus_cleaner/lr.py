import re

from ._lr_rules import _rules
from .simple_tag import to_simple_tag
from .loader import MorphTag
from .utils import is_jaum, is_moum, is_hangle, compose, decompose
from .utils import check_lr_transformation
from .utils import check_lemmatization


def to_lr(eojeol, morphtags, noun_xsv_as_verb=False, xsv_as_root=False, rules=None, debug=False):
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
    xsv_as_root : Boolean
        Option for L-R format transformation.
        It executes only when noun_xsv_as_verb is False
        If True, it considers XSV as root of verb

            $ "시작/NNG + 하/XSV + 다/EP" -> ["시작/Noun", "하/Verb + 다/Eomi"]

        Else

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    rules : dict
        L, R tramsform rules
        {eojeol: ((L morph, L tag), (R morph, R tag))}
    debug : Boolean
        If True, it shows local variables.

    Returns
    -------
    list_eojeol_morphtags : list of tuple
        Each tuple consists with (preprocessed_eojeol, l, r, morphtags, b)
        preprocessed_eojeol is text after removing symbols, str type
        l is namedtuple of (morph, tag) in L-R format, MorphTag type
        r is namedtuple of (morph, tag) in L-R format, MorphTag type
        b is boundary index of morphtags
    """

    eojeol_raw = eojeol
    morphtags_raw = [mt for mt in morphtags]

    eojeol, morphtags = preprocess0(eojeol, morphtags)

    # ('6.25', [('6', 'SN'), ('.', 'SF'), ('25', 'SN')], False, False),
    # ('6.25의', [('6', 'SN'), ('.', 'SF'), ('25', 'SN'), ('의', 'JKO')], False, False),
    l, r, b = transform_symbol_noun(eojeol, morphtags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    # ('IBM에서는', [('IBM', 'SL'), ('에서', 'JKB'), ('는', 'JX'), False, False])
    l, r, b = transform_foreign_noun(eojeol, morphtags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    eojeol, morphtags = preprocess1(eojeol, morphtags)
    if (not eojeol) or (not morphtags):
        if debug:
            message = 'Filtered by preprocessor. eojeol = {}, morphtags = {}'.format(
                eojeol, morphtags)
            raise ValueError(message)
        return [(eojeol, None, None, [], -1)]

    l, r, b = transform_with_rules0(eojeol, morphtags, debug=False)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    if (not noun_xsv_as_verb) and (xsv_as_root):
        separated = split_by_xsv(eojeol, morphtags, debug)
        if len(separated) == 2:
            (eojeol_0, morphtags_0), (eojeol_1, morphtags_1) = separated
            eojeol_0, l_0, r_0, morphtags_0, b_0 = to_lr(eojeol_0, morphtags_0,
                noun_xsv_as_verb=False, xsv_as_root=False, rules=rules, debug=debug)[0]
            eojeol_1, l_1, r_1, morphtags_1, b_1 = to_lr(eojeol_1, morphtags_1,
                noun_xsv_as_verb=False, xsv_as_root=False, rules=rules, debug=debug)[0]
            return [(eojeol_0, l_0, r_0, morphtags_0, b_0), (eojeol_1, l_1, r_1, morphtags_1, b_1)]

    l, r, b = transform_with_rules(eojeol, morphtags, rules=None, debug=debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    # prepare materials
    morphs = [mt.morph for mt in morphtags]
    tags = [mt.tag for  mt in morphtags]
    simple_tags = [to_simple_tag(tag) for tag in tags]

    l, r, b = transform_short_morphtag(eojeol, morphs, tags, simple_tags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    # 전성 어미가 존재할 경우.
    # noun_xsv_as_verb = True 이면 "시작/NNG + 하/XSV + ㄴ다/EP" -> "시작하/Verb + ㄴ다/Eomi"
    # noun_xsv_as_verb = False 이면 "시작/Noun + 한다/Verb" 로 변형한다.
    l, r, b = transform_when_noun_is_changed_to_predicator(
        eojeol, morphs, tags, simple_tags, noun_xsv_as_verb, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        # ('될텐데', [('되', 'VV'), ('ㄹ', 'ETM'), ('터', 'NNB'), ('이', 'VCP'), ('ㄴ데', 'EC')], False, False)
        if (xsv_as_root or noun_xsv_as_verb) and (l.tag == 'Noun') and (r.tag == 'Adjective' or r.tag == 'Verb'):
            r = MorphTag(r.morph, 'Josa')
        return [(eojeol, l, r, morphtags, b)]

    l, r, b = transform_normal_case(eojeol, morphs, tags, simple_tags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    # ('왜냐,', [('왜', 'MAG'), ('냐', 'EF'), (',', 'SP')], False, False),
    # ('진짜야?', [('진짜', 'MAG'), ('야', 'EF'), ('?', 'SF')], False, False),
    # ('야라는', [('야','IC'), ('라는','ETM')], False, False),
    # ('야라니?', [('야','IC'), ('라니','EF'), ('?','SF')], False, False),
    # ('여보셔요!"', [('여보','IC'), ('시','EP'), ('어요','EF'), ('!','SF'), ('"','SS')], False, False),
    l, r, b = transform_exceptional_case(eojeol, morphs, tags, simple_tags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    l, r, b = transform_only_eomi_josa(eojeol, morphtags, tags, simple_tags, debug)
    if l is not None and check_lemmatization(eojeol, l, r):
        return [(eojeol, l, r, morphtags, b)]

    message = 'Exception: Eojeol = {}, morphtags = {}'.format(eojeol_raw, morphtags_raw)
    raise ValueError(message)

def split_by_xsv(eojeol, morphtags, debug=False):
    """XSV, XSA, VCP, VCN 과 같은 전성어미가 존재하는 경우"""

    tags = [mt.tag for mt in morphtags]
    simple_tags = [to_simple_tag(mt.tag) for mt in morphtags]
    for target in 'XSV XSA VCP VCN'.split():
        i = rindex(tags, target)
        if not (i > 0 and (simple_tags[i-1] == 'Noun' or simple_tags[i-1] == 'Adverb')):
            continue
        eojeol_0_len = len(''.join([c for mt in morphtags[:i] for c in mt.morph if (not is_jaum(c) and not is_moum(c))]))
        eojeol_0 = eojeol[:eojeol_0_len]
        eojeol_1 = eojeol[len(eojeol_0):]
        morphtags_0 = morphtags[:i]
        morphtags_1 = morphtags[i:]
        # ('문화다.', [('문화', 'NNG'), ('이', 'VCP'), ('다', 'EF'), ('.', 'SF')], True, False),
        if (eojeol_1) and (eojeol_1[0] == morphtags_1[1].morph[0]) or (eojeol_1[0] == morphtags_1[1].morph[1:2]):
            continue
        if debug:
            print('called split_by_xsv')
        if (not eojeol_0) or (not eojeol_1) or (not morphtags_0) or (not morphtags_1):
            message = """Failed to split morphtags by xsv. eojeol={}, morphtags={}
            -> eojeol_0 = ({}), morphtags_0 = ({})
            -> eojeol_1 = ({}), morphtags_1 = ({})""".format(
                eojeol, morphtags, eojeol_0, morphtags_0, eojeol_1, morphtags_1)
            raise ValueError(message)
        return [(eojeol_0, morphtags_0), (eojeol_1, morphtags_1)]
    return [(eojeol, morphtags)]

def preprocess0(eojeol, morphtags):
    # remove empty morphs
    morphtags_raw = [mt for mt in morphtags]
    morphtags = [mt for mt in morphtags if mt.morph]

    if (eojeol[0] in set('뭐뭔뭡뭘') and morphtags[0].morph == '무엇'):
        replace = lambda mt: MorphTag('뭐', mt.tag) if mt.morph == '무엇' else mt
        morphtags = [replace(mt) for mt in morphtags]

    # "네것을" = "너/NP + 의/JKG + 것/NNB + 을/JKO (1)"
    if (eojeol[0] == '네' or eojeol[0] == '내' or eojeol[0] == '제') and (morphtags[0].tag == 'NP'):
        morphtags = [MorphTag(eojeol[0], 'NP')] + morphtags[2:]

    return eojeol, morphtags

def preprocess1(eojeol, morphtags):
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

    pattern = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z·]')
    normalize = lambda s:pattern.sub('', s)

    morphtags_ = []
    for morphtag in morphtags:
        if is_useless(morphtag.morph, morphtag.tag):
            eojeol = eojeol.replace(morphtag.morph, '', 1)
        else:
            morphtags_.append(morphtag)
    eojeol = normalize(eojeol)
    return eojeol, morphtags_

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
        return l, r, i
    return None, None, -1

def transform_foreign_noun(eojeol, morphtags, debug=False):
    simple_tags = [to_simple_tag(mt.tag) for mt in morphtags]
    if (morphtags[0].tag == 'SH') or (morphtags[0].tag == 'SL'):
        if debug:
            print('called transform_foreign_noun')
        if len(morphtags) == 1:
            return MorphTag(morphtags[0].morph, 'Noun'), None, 0
        elif simple_tags[1] != 'Symbol':
            morph_l = morphtags[0].morph
            morph_r = eojeol[len(morph_l):]
            return MorphTag(morph_l, 'Noun'), MorphTag(morph_r, simple_tags[1]), 0
    return None, None, -1

def transform_with_rules0(eojeol, morphtags, debug=False):
    if eojeol[:2] == '어쨌':
        return MorphTag('어찌하', 'Verb'), MorphTag('았'+eojeol[2:], 'Eomi'), -1
    if eojeol[:2] == '어쩔':
        return MorphTag('어찌하', 'Verb'), MorphTag('알'+eojeol[2:], 'Eomi'), -1
    if eojeol[:2] == '제것':
        return MorphTag('제것', 'Noun'), MorphTag(eojeol[2:], 'Josa'), -1
    if eojeol[:3] == '이뤄졌':
        return MorphTag('이뤄지', 'Verb'), MorphTag(eojeol[3:], 'Eomi'), -1
    return None, None, -1

def transform_with_rules(eojeol, morphtags, rules=None, debug=False):
    if to_simple_tag(morphtags[-1].tag) == 'Noun':
        if debug:
            print('called transform_with_rules')
        return MorphTag(eojeol, 'Noun'), None, len(morphtags)-1
    if rules is None:
        rules = _rules
    (morph_l, tag_l), (morph_r, tag_r) = rules.get(eojeol, ((None, None), (None, None)))
    if morph_l is None:
        return None, None, -1
    if debug:
        print('called transform_with_rules')
    l = MorphTag(morph_l, tag_l)
    r = MorphTag(morph_r, tag_r) if morph_r is not None else None
    return l, r, -1

def transform_short_morphtag(eojeol, morphs, tags, simple_tags, debug=False):
    morph_l = morphs[0]
    tag_l = simple_tags[0]
    l = MorphTag(morph_l, tag_l)

    if len(morphs) == 1:
        if debug:
            print('called transform_short_morphtag')
        return l, None, 0

    exception_tags = {'Eomi', 'Josa', 'Adverb', 'Unk', 'Exclamation', 'Number', 'Determiner'}
    if (len(morphs) <= 2) and (not simple_tags[0] in exception_tags):
        if debug:
            print('called transform_short_morphtag')
        if simple_tags[0] in {'Noun', 'Pronoun', 'Numeral'}:
            tag_r = 'Josa'
        else:
            tag_r = simple_tags[1]

        if check_lr_transformation(eojeol, (morph_l, tag_l), (postprocessing(morphs[1]), simple_tags[1]), debug):
            r = MorphTag(postprocessing(morphs[1]), simple_tags[1])
            return l, r, 0

        surface_l = eojeol[:len(morph_l)]
        surface_r = eojeol[len(morph_l):]
        morph_r = lemmatize_r(eojeol, surface_l, surface_r, morph_l, tag_l, tag_r, morphs, 0, debug)
        r = MorphTag(postprocessing(morph_r), tag_r)

        if not check_lr_transformation(eojeol, l, r, debug):
            return None, None, -1

        return l, r, 0
    return None, None, -1

def transform_when_noun_is_changed_to_predicator(
    eojeol, morphs, tags, simple_tags, noun_xsv_as_verb, debug=False):
    """XSV, XSA, VCP, VCN 과 같은 전성어미가 존재하는 경우"""

    for target in 'XSV XSA VCP VCN'.split():
        i = rindex(tags, target)
        if not ((i > 0) and (simple_tags[i-1] == 'Noun' or simple_tags[i-1] == 'Pronoun' or simple_tags[i-1] == 'Numeral' or simple_tags[i-1] == 'Adverb')):
            continue
        if debug:
            print('called transform_when_noun_is_changed_to_predicator')
        if noun_xsv_as_verb:
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i, debug)
        else:
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i-1, debug)
        return l, r, i
    return None, None, -1

def transform_normal_case(eojeol, morphs, tags, simple_tags, debug=False):
    for target in 'Noun Pronoun Numeral Verb Adjective'.split():
        i = rindex(simple_tags, target)
        if i >= 0:
            if debug:
                print('called transform_normal_case')
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i, debug)
            return l, r, i
    return None, None, -1

def transform_exceptional_case(eojeol, morphs, tags, simple_tags, debug=False):
    for target in 'Adverb Unk Exclamation Number Determiner'.split():
        i = rindex(simple_tags, target)
        if i < 0:
            continue
        if debug:
            print('called transform_exceptional_case')
        if target == 'Number':
            if i == 0:
                l, r = lr_form(eojeol, morphs, tags, simple_tags, i, tag_l='Number')
            else:
                l, r = lr_form(eojeol, morphs, tags, simple_tags, i, tag_l='Noun')
            return l, r, i
        if i == len(tags) - 1:
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i)
            return l, r, i
        elif simple_tags[i+1] == 'Josa':
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i, debug, tag_l='Noun', tag_r='Josa')
            return l, r, i
        elif target == 'Adverb' and simple_tags[i+1] == 'Eomi' and simple_tags[-1] == 'Eomi':
            l, r = MorphTag(eojeol, 'Adverb'), None
            return l, r, i
        elif target == 'Exclamation' and simple_tags[i+1] == 'Eomi' and simple_tags[-1] == 'Eomi':
            l, r = lr_form(eojeol, morphs, tags, simple_tags, i, tag_l='Exclamation', tag_r='Josa')
            return l, r, i
    return None, None, -1

def transform_only_eomi_josa(eojeol, morphtags, tags, simple_tags, debug=False):
    def all_eomi_or_josa(simple_tags):
        for t in simple_tags:
            if not (t == 'Josa' or t == 'Eomi'):
                return False
        return True

    if not all_eomi_or_josa(simple_tags):
        return None, None, -1
    if debug:
        print('called transform_only_eomi_josa')
    return MorphTag(eojeol, simple_tags[0]), None, len(morphtags) - 1

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

def lr_form(eojeol, morphs, tags, simple_tags, i, debug=False,
    tag_l=None, tag_r=None, boundary_index_shift=0):

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
    boundary_index_shift : int
        The movement from return of the surface_boundary function.

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

        morphs_l_concat = ''.join(morphs[:i+1])
        morphs_r_concat = ''.join([only_hangle(m) for m in morphs[i+1:]])

        # ('세워져', [('세우', 'VV'), ('어', 'EC'), ('지', 'VX'), ('어', 'EC')], False, False),
        if is_compound_predicator():
            return len(eojeol) - len(morphs_r_concat) + boundary_index_shift
        b = len(morphs_l_concat)

        # ('별로야.', [('별로', 'MAG'), ('이', 'VCP'), ('야', 'EF'), ('.', 'SF')], False, False),
        if morphs[i] == '이' and tags[i] == 'VCP' and eojeol[b-1] == morphs[i+1][0]:
            b -= 1
        return b

    b = surface_boundary()
    if b > len(eojeol):
        return None, None

    surface_l, surface_r = eojeol[:b], eojeol[b:]

    if tag_l is None:
        tag_l = simple_tags[i]
    if tag_r is None:
        tag_r = simple_tags[i+1] if i < (n-1) else None
        if (tags[i+1] == 'VCP'):
            # ('문화다.', [('문화', 'NNG'), ('이', 'VCP'), ('다', 'EF'), ('.', 'SF')], False, False),
            if (surface_r and surface_r[0] == morphs[i+2][0]):
                tag_r = 'Josa'
            # ('건지도', [('것', 'NNB'), ('이', 'VCP'), ('ㄴ지', 'EC'), ('도', 'JX')], False, False),
            if (is_jaum(morphs[i+2][0])) and (len(morphs[i+2]) >= 2) and (surface_r[0] == morphs[i+2][1]):
                tag_r = 'Josa'

    # ('이데올로기다.', [('이데올로기', 'NNG'), ('이', 'VCP'), ('다', 'EF')], False, False)
    if (i > 0) and (tags[i] == 'VCP' and morphs[i] == '이') and (surface_l[-1] == morphs[i-1][-1]):
        tag_l = 'Noun'
        tag_r = 'Josa'
        morph_l = surface_l
    else:
        morph_l = lemmatize_l(eojeol, surface_l, surface_r, morphs, tags, simple_tags, i, debug)

    if tag_l in {'Verb', 'Adjective', 'Noun', 'Pronoun', 'Numeral'}:
        morph_r = lemmatize_r(eojeol, surface_l, surface_r, morph_l, tag_l, tag_r, morphs, i, debug)
    else:
        morph_r = surface_r

    right_form = check_lr_transformation(eojeol, (morph_l, tag_l), (morph_r, tag_r), debug)

    if debug:
        print('Boundary  : {}'.format(b))
        print('[surface / morph / tag]')
        print('[{} / {} / {}]'.format(surface_l, morph_l, tag_l))
        print('[{} / {} / {}]'.format(surface_r, morph_r, tag_r))
        print('L-R checker : {}'.format(right_form))

    if not right_form:
        if (b + boundary_index_shift) >= len(eojeol):
            return None, None
        if debug:
            print('-- re-try with shifting boundary index +1 --')
        l, r = lr_form(eojeol, morphs, tags, simple_tags, i, debug,
            tag_l, tag_r, boundary_index_shift+1)
        return l, r

    return MorphTag(morph_l, tag_l), MorphTag(morph_r, tag_r)

def lemmatize_l(eojeol, surface_l, surface_r, morphs, tags, simple_tags, i, debug=False):
    # use last character of morphs
    # 따라 [['따르', 'VV'], ['ㅏ', 'EC']]
    if (i > 0) and (morphs[i] == '이') and (tags[i] == 'VCP') and (morphs[i-1][-1] == surface_l[-1]):
        if debug:
            print('lemmatize_l: 별로야 = 별로 + (이) + 야')
        morph_l = surface_l
    else:
        if debug:
            print('lemmatize_l: default')
        morph_l = surface_l[:-1] +  morphs[i][-1]

    # ('어째서', [('어찌', 'MAG'), ('하', 'XSV'), ('아서', 'EC')], False, False)
    # ('어째서', [('어찌', 'MAG'), ('하', 'XSA'), ('아서', 'EC')], False, False)
    if (i > 0) and (morphs[i] == '하' and tags[i][:2] == 'XS') and (morphs[i-1][-1] != morph_l[-2]):
        if debug:
            print('lemmatize_l: 어째서 = 어찌 + 하 + 아서')
        morph_l = morph_l[:-2] + morphs[i-1][-1] + morphs[i]

    # ('용케', [('용하', 'VA'), ('게', 'EC')], False, False)
    if (simple_tags[i] == 'Verb' or simple_tags[i] == 'Adjective') and (surface_l[-1] == '케'):
        if debug:
            print('lemmatize_l: 하 + 게 -> 케')
        morph_l = surface_l[:-1] + '하'

    # ('사용토록', [('사용', 'NNG'), ('하', 'XSV'), ('도록', 'EC')], False, False)
    if (simple_tags[i] == 'Verb' or simple_tags[i] == 'Adjective') and (surface_l[-1] == '토'):
        if debug:
            print('lemmatize_l: 하 + 도 -> 토')
        morph_l = surface_l[:-1] + '하'

    if morph_l[-1] == 'ㅎ':
        if debug:
            print('lemmatize_l: -ㅎ + R -> -하 + R')
        morph_l = morph_l[:-1] + '하'
    if morph_l[-1] == 'ㄱ':
        if debug:
            print('lemmatize_l: -ㄱ + R -> -가 + R')
        morph_l = morph_l[:-1] + '가'

    return morph_l

def lemmatize_r(eojeol, surface_l, surface_r, morph_l, tag_l, tag_r, morphs, i, debug=False):
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
        print('tag_r     : {}'.format(tag_r))
        print('morphs    : {}'.format(morphs))
        print('i         : {}'.format(i))
        print('w0        : {}'.format(w0))
        print('c0, c1    : {}'.format(c0, c1))
        print('concat_r  : {}'.format(concat_r))

    ###############
    # lemmatizing josa #
    if ((tag_l == 'Noun') or (tag_l == 'Pronoun') or (tag_l == 'Numeral')) and (tag_r == 'Josa'):
        if c0 and is_jaum(c0):
            if debug:
                print('lemmatize_r: Noun + 자음')
            return c0 + surface_r
        elif not (len(concat_r) >= 3 and c0 == '이' and is_jaum(concat_r[1])):
            if debug:
                print('lemmatize_r : Noun + Josa')
            # ('뭘로', [('무엇', 'NP'), ('으로', 'JKB')], False, False),
            morph_r = surface_r
            _, _, jong_canon = decompose(morph_l[-1])
            _, _, jong_surf = decompose(surface_l[-1])
            if (jong_canon == ' ') and (jong_surf != ' '):
                if morph_r and morph_r[0] != jong_surf:
                    morph_r = jong_surf + morph_r
                elif not morph_r:
                    morph_r = jong_surf
            return morph_r

    ###############
    # lemmatizing eomis #

    if len(concat_r) + 2 <= len(surface_r):
        return ''
        #raise ValueError('어절에 잘못된 글자가 포함되어 있을 경우: eojeol={}, morphs={}'.format(eojeol, morphs))

    # 활용시 2음절이 1음절로 변하는 경우 (1음절 R 이 합쳐진 경우)
    # 복원시 1음절을 2음절로 확장
    # ('다해', [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']], False, False)
    if (not surface_r) and (surface_l[-1] != '케') and (surface_l[-1] !='토'):
        if debug:
            print('lemmatize_r: surface_r not case')
        morph_r = w0

    # ('용케', [('용하', 'VA'), ('게', 'EC')], False, False)
    elif (tag_l == 'Verb' or tag_l == 'Adjective') and (surface_l[-1] == '케'):
        morph_r = '게' + surface_r

    # ('사용토록', [('사용', 'NNG'), ('하', 'XSV'), ('도록', 'EC')], False, False)
    elif (tag_l == 'Verb' or tag_l == 'Adjective') and (surface_l[-1] == '토'):
        morph_r = '도' + surface_r

    # ('생각케', [('생각', 'NNG'), ('하', 'XSV'), ('게', 'EC')], False, False)
    elif (tag_l == 'Noun') and (tag_r == 'Verb' or tag_r == 'Adjective') and (surface_r[0] == '케') and (morphs[i+1] == '하'):
        if debug:
            print('lemmatize_r: "생각 + 하 + 게 -> 생각 + 케" case')
        morph_r = '하게' + surface_r[1:]

    # ('사용토록', [('사용', 'NNG'), ('하', 'XSV'), ('도록', 'EC')], False, False)
    elif (tag_l == 'Noun') and (tag_r == 'Verb' or tag_r == 'Adjective') and (surface_r[0] == '토') and (morphs[i+1] == '하'):
        if debug:
            print('lemmatize_r: "생각 + 하 + 도록 -> 생각 + 토록" case')
        morph_r = '하도' + surface_r[1:]

    # 활용시 2음절이 1음절이 변하는 경우 (1음절 L 과 1음절 R 이 합쳐진 경우, -하다 동사류)
    # 복원시 1음절을 2음절 (1음절 L 과 1음절 R) 로 확장
    # ('통해서', [['통하', 'VV'], ['ㅕ서', 'EC']], False, False)
    elif morph_l[-1] == '하' and (c0 == '여' or c0 == 'ㅕ' or c0 == '어' or c0 == 'ㅓ'):
        if debug:
            print('lemmatize_r: "- 하 + 여" case')
        morph_r = '아' + surface_r

    # 활용시 2음절이 1음절이 변하는 경우 (2음절 R 이 1음절로 축약된 경우, -하다 동사류 외)
    # 복원시 1음절을 2음절 (1음절 L 과 1음절 R) 로 확장
    # ('느꼈으니', [['느끼', 'VV'], ['었', 'EP'], ['으니', 'EC']], False, False)
    elif surface_r == concat_r[1:]:
        if debug:
            print('lemmatize_r: "+ 었" case')
        morph_r = c0 + surface_r

    # 활용시 첫글자가 자음인 R 이 L 에 병합된 경우
    # 복원시 R 의 자음을 surface 에 부착
    # ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']], False, False)
    elif is_jaum(c0):
        if debug:
            print('lemmatize_r: "+ ㄴ" case')
        morph_r = c0 + surface_r

    # 활용시 R 에 1음절이 추가된 경우
    # 복원시 R 에 추가된 음절을 포함
    # ('반가우면서도', [['반갑', 'VA'], ['면서', 'EC'], ['도', 'JX']], False, False),
    elif surface_r[1:] == concat_r:
        if debug:
            print('lemmatize_r: R 에 1음절이 추가된 경우')
        morph_r = surface_r[0] + concat_r

    # 활용시 1음절의 L 과 2음절의 R 이 각각 활용된 1음절과 축약된 1음절로 변형된 경우
    # 복원시 L 의 마지막 음절을 복원하고, R 의 첫음절을 두 개의 음절로 복원
    # ('거셨을', [('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')], False, False)
    # ('분석해보자.', [('분석', 'NNG'), ('하', 'XSV'), ('아', 'EC'), ('보', 'VX'), ('자', 'EF'), ('.', 'SF')], False, False),
    elif surface_r[1:] == concat_r[2:]:
        if debug:
            print('lemmatize_r: 1음절의 L 과 2음절의 R 이 축약된 경우')
        if concat_r[:2] == '하아':
            morph_r = '해' + concat_r[2:]
        else:
            morph_r = concat_r

    # ('세웠다', [('세우', 'VV'), ('어', 'EC'), ('ㅆ다', 'EF')], False, False)
    elif concat_r[:2] == '어ㅆ':
        if debug:
            print('lemmatize_r: "(어)ㅆ다" case')
        morph_r = '었' + surface_r

    # ('봤는데,', [('보', 'VV'), ('ㅏㅆ', 'EP'), ('는데', 'EC'), (',', 'SP')], False, False)
    elif concat_r[:2] == 'ㅏㅆ':
        if debug:
            print('lemmatize_r: "ㅏㅆ" case')
        morph_r = '았' + surface_r

    elif concat_r[:2] == 'ㅓㅆ':
        if debug:
            print('lemmatize_r: "ㅓㅆ" case')
        morph_r = '었' + surface_r

    # ('건지도', [('것', 'NNB'), ('이', 'VCP'), ('ㄴ지', 'EC'), ('도', 'JX')], False, False),
    # ('뭡니까.', [('무엇','NP'), ('이','VCP'), ('ㅂ니까','EF'), ('.','SF')], False, False)
    elif (len(concat_r) >= 3 and surface_r[0] == concat_r[2]) and (concat_r[0] == '이' and is_jaum(concat_r[1])):
        if debug:
            print('lemmatize_r: "것 + (이) + ㄴ지 + 도" case')
        morph_r = compose('ㅇ', 'ㅣ', concat_r[1]) + surface_r

    else:
        if debug:
            print('lemmatize_r: 그 외의 변형')
        morph_r = c0 + surface_r[1:]

    return postprocessing(morph_r)

def postprocessing(morph_r):
    # R 의 첫글자가 모음인 경우
    # ('통해서', [['통하', 'VV'], ['ㅏ서', 'EC']], False, False)
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
