tagmap = {
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
 'NR': 'Number',
 'SE': 'Symbol',
 'SF': 'Symbol',
 'SH': 'Symbol',
 'SL': 'Symbol',
 'SN': 'Symbol',
 'SO': 'Symbol',
 'SP': 'Symbol',
 'SS': 'Symbol',
 'SW': 'Symbol',
 'VA': 'Adjective',
 'VCN': 'Adjective', # 아니
 'VCP': 'Adjective', # 이
 'VV': 'Adverb',
 'VX': 'Verb',
 'XPN': 'Determiner', # 과/XPN+부가, 폐/XPN+휴지
 'XR': 'Noun', # 강렬, 간편, 비슷 # XR + XSV/XSA 는 동/형용사가 됨
 'XSA': 'Adjective', # 같, 답, 되, 하
 'XSN': 'Eomi', # 반영구+적/XSN, 대만+산/XSN # XSN 앞이 반드시 명사인지 확인해야 함
 'XSV': 'Verb' # 당하, 시키
 }

def simplify_tag(tag):
    return tagmap.get(tag, 'Unk')