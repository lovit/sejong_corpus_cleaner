default_tagmap = {
 'EC': 'Eomi',
 'EF': 'Eomi',
 'EP': 'Eomi',
 'ETM': 'Eomi',
 'ETN': 'Eomi',
 'IC': 'Exclamation',
 'JC': 'Josa',
 'JKB': 'Josa',
 'JKC': 'Josa',
 'JKG': 'Josa',
 'JKO': 'Josa',
 'JKQ': 'Josa',
 'JKS': 'Josa',
 'JKV': 'Josa',
 'JX': 'Josa',
 'MAG': 'Adverb',
 'MAJ': 'Adverb',
 'MM': 'Determiner',
 'NA': 'Unk',
 'NNB': 'Noun',
 'NNG': 'Noun',
 'NNP': 'Noun',
 'NP': 'Pronoun',
 'NR': 'Numeral',
 'SE': 'Symbol',
 'SF': 'Symbol',
 'SH': 'Symbol',
 'SL': 'Symbol',
 'SN': 'Number',
 'SO': 'Symbol',
 'SP': 'Symbol',
 'SS': 'Symbol',
 'SW': 'Symbol',
 'VA': 'Adjective',
 'VCN': 'Adjective', # 아니
 'VCP': 'Adjective', # 이
 'VV': 'Verb',
 'VX': 'Verb', # 해왔다 -> 하/VX+아/EC+오/VX+았/EP+다/EF
 'XPN': 'Determiner', # 과/XPN+부가, 폐/XPN+휴지
 'XR': 'Noun', # 강렬, 간편, 비슷 # XR + XSV/XSA 는 동/형용사가 됨
 'XSA': 'Adjective', # 같, 답, 되, 하
 'XSN': 'Noun', # 반영구+적/XSN, 대만+산/XSN # XSN 처럼 명사 뒤에 suffix 역할을 함
 'XSV': 'Verb' # 당하, 시키
 }

tagset = {
 'Adjective': '형용사',
 'Adverb': '동사',
 'Determiner': '관형사',
 'Eomi': '어미',
 'Exclamation': '감탄사',
 'Josa': '조사',
 'Noun': '명사',
 'Number': '수사',
 'Pronoun': '대여사',
 'Symbol': '기호',
 'Unk': '인식불가',
 'Verb': '동사'
}

def to_simple_tag(tag, tagmap=None):
    """
    Arguments
    ---------
    tag : str
        Original tag
    tagmap : dict of (str, str)
        Tag mapper. If None, use default tagmap

    Returns
    -------
    simple_tag : str
        Simplified tag

    Usage
    -----
        >>> to_simple_tag('NNG')
        $ 'Noun'

        >>> to_simple_tag('NNG', {'NNG': 'N'})
        $ 'N'
    """
    if tagmap is None:
        tagmap = default_tagmap
    return tagmap.get(tag, 'Unk')

def to_simple_morphtags(morphtags, tagmap=None):
    """
    Arguments
    ---------
    morphtags : list of tuple
        Each tuple consists of (morph, tag)
    tagmap : dict of (str, str)
        Tag mapper. If None, use default tagmap

    Returns
    -------
    morphtags : list of tuple
        List of (morph, simplified_tag)

    Usage
    -----
    """
    return [(morph, to_simple_tag(tag, tagmap)) for morph, tag in morphtags]
