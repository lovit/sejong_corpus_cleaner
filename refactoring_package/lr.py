def to_lr(eojeol, morphtags, xsv_as_verb=False):
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
    return eojeol_, morphtags_
