import os
import subprocess


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

def select_morphtags(sent, flatten=True, remain_not_exists=False):
    """
    Arguments
    ---------
    sent : str
        '\n' separated sentence
        Each item which separated with '\n' is forms EOJEOL\tMORPHTAGS
        For example,

            프랑스의	프랑스/NNP + 의/JKG
            세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
            의상	의상/NNG

    flatten : Boolean
        If True, it returns list of tuple
        Else, it returns nested list
    remain_not_exists:
        If True, it does not remove hidden morphomems
        Default is False

    Returns
    -------
    morphtags : nested list

    Usage
    -----
        >>> path = '../data/raw/written/BTAA0001.txt'
        >>> sents = extract_sentences(path)
        >>> select_morphtags(sents[0], flatten=False)
        $ [[['프랑스', 'NNP'], ['의', 'JKG']],
           [['세계', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ㄴ', 'ETM']],
           [['의상', 'NNG']],
           ...

        >>> select_morphtags(sents[0])
        $ [['프랑스', 'NNP'],
           ['의', 'JKG'],
           ['세계', 'NNG'],
           ['적', 'XSN'],
           ['이', 'VCP'],
           ['ㄴ', 'ETM'],
           ...

        >>> path = '../data/raw/colloquial/5CT_0016.txt'
        >>> sents = extract_sentences(path)
        >>> select_morphtags(sents[0], flatten=False)
        $ [[['걔', 'NP']],
           [['두', 'MM']],
           [['명', 'NNB'], ['이', 'JKS']],
           [['하', 'VV'], ['는', 'ETM']],
           [['거', 'NNB'], ['야', 'EF'], ['.', 'SF']]]

        >>> select_morphtags(sents[0], flatten=False, remain_not_exists=True)
        $ [[['걔', 'NP']],
           [['두', 'MM']],
           [['명', 'NNB'], ['이', 'JKS']],
           [['하', 'VV'], ['는', 'ETM']],
           [['거', 'NNB'], ['(이)', 'VCP'], ['야', 'EF'], ['.', 'SF']]]
    """
    eojeol_morphtags = [e.split('\t') for e in sent.split('\n')]
    eojeols, morphtags = zip(*eojeol_morphtags)
    morphtags = [[mt.rsplit('/',1) for mt in mts.split(' + ')] for mts in morphtags]

    def exists(morphtag):
        return not ('(' in morphtag[0] and ')' in morphtag[0])

    if not remain_not_exists:
        morphtags = [[mt for mt in mts if exists(mt)] for mts in morphtags]

    if flatten:
        morphtags = [mt for mts in morphtags for mt in mts]

    return morphtags

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
    return ''.join(unicode_character(c) for c in sent)
