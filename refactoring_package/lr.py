from ._lr_rules import _rules
from .simple_tag import to_simple_tag

def to_lr(eojeol, morphtags, xsv_as_verb=False, rules=None):
    lr_morphemes = morphtags_to_lr(eojeol, morphtags, xsv_as_verb, rules)
    return None

def morphtags_to_lr(eojeol, morphtags, xsv_as_verb=False, rules=None):

    eojeol, morphtags = preprocess(eojeol, morphtags)
    if (not eojeol) or (not morphtags):
        raise ValueError('Filtered by preprocessor. eojeol = {}, morphtags = {}'.format(eojeol, morphtags))

    l, r = transform_with_rules(eojeol, morphtags, rules=None)
    if l is not None:
        return l, r

    l, r = transform_with_short_morphtags(morphtags)
    if l is not None:
        return l, r

    # 전성 어미가 존재할 경우.
    # xsv_as_verb = True 이면 "시작/NNG + 하/XSV + ㄴ다/EP" -> "시작하/Verb + ㄴ다/Eomi"
    # xsv_as_verb = False 이면 "시작/Noun + 한다/Verb" 로 변형한다.
    l, r = transform_when_pos_is_changed(eojeol, morphtags, xsv_as_verb)
    if l is not None:
        return l, r

    raise NotImplemented

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
        $ 걔	걔/NP
          두	두/MM
          명이	명/NNB + 이/JKS
          하는	하/VV + 는/ETM
          거야.	거/NNB + (이)/VCP + 야/EF + ./SF

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

def transform_with_short_morphtags(morphtags):
    if len(morphtags) == 1:
        m0 = morphtags[0].morph
        t0 = to_simple_tag(morphtags[0].tag)
        return ((m0, t0), ('', ''))
    if len(morphtags) == 2:
        m0 = morphtags[0].morph
        t0 = to_simple_tag(morphtags[0].tag)
        m1 = morphtags[1].morph
        t1 = to_simple_tag(morphtags[1].tag)
        return ((m0, t0), (m1, t1))
    return None, None

def transform_when_pos_is_changed(eojeol, morphtags):
    """
    XSV, XSA, VCP, VCN 과 같은 전성어미가 존재하는 경우
    """
    for tag in 'XSV XSA VCP VCN'.split():
        continue
    raise NotImplemented
