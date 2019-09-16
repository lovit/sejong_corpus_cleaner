from collections import namedtuple
from bs4 import BeautifulSoup
import os

from .utils import unicode_sentence
from .format_checker import check_sejong_tagset


sep = os.path.sep


class MorphTag(namedtuple('MorphTag', 'morph tag')):
    """
    Attributes
    ----------
    morph : str
        Morpheme
    tag : str
        Tag

    Usage
    -----
        >>> morphtag = MorphTag('프랑스', 'NNP')
        >>> print(morphtag)
        $ 프랑스/NNP
    """
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s/%s' % (self.morph, self.tag)


class Sentence:
    """
    Attributes
    ----------
    eojeols : list of str
        List of eojeol
    morphtags : list of list of MorphTag
        Its length is same to tat of eojeols

    Usage
    -----
        >>> eojeols = ('프랑스의',
             '세계적인',
             '의상',
             '디자이너',
             '엠마누엘',
             '웅가로가',
             '실내',
             '장식용',
             '직물',
             '디자이너로',
             '나섰다.')
        >>> morphtags = [[프랑스/NNP, 의/JKG],
             [세계/NNG, 적/XSN, 이/VCP, ㄴ/ETM],
             [의상/NNG],
             [디자이너/NNG],
             [엠마누엘/NNP],
             [웅가로/NNP, 가/JKS],
             [실내/NNG],
             [장식/NNG, 용/XSN],
             [직물/NNG],
             [디자이너/NNG, 로/JKB],
             [나서/VV, 었/EP, 다/EF, ./SF]] # Each item is list of MorphTag

        >>> sentence = Sentence(eojeols, morphtags)
        >>> len(sentence)
        $ 11

        >>> sentence[1]
        $ ('세계적인', [세계/NNG, 적/XSN, 이/VCP, ㄴ/ETM])

        >>> print(sentence)
        $ 프랑스의	프랑스/NNP + 의/JKG
          세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
          의상 	 의상/NNG
          디자이너	디자이너/NNG
          엠마누엘	엠마누엘/NNP
          웅가로가	웅가로/NNP + 가/JKS
          실내	 실내/NNG
          장식용	장식/NNG + 용/XSN
          직물	 직물/NNG
          디자이너로	디자이너/NNG + 로/JKB
          나섰다.	 나서/VV + 었/EP + 다/EF + ./SF

        >>> sentence.get_morphtags()
        $ [[프랑스/NNP, 의/JKG],
           [세계/NNG, 적/XSN, 이/VCP, ㄴ/ETM],
           ...

        >>> sentence.get_morphtags(flatten=True)
        $ [프랑스/NNP,
           의/JKG,
           세계/NNG,
           적/XSN,
           이/VCP,
           ㄴ/ETM,
           ...
    """
    def __init__(self, list_of_eojeol, list_of_morphtags):

        assert len(list_of_eojeol) == len(list_of_morphtags)

        def exist_empty_item(seq):
            return len([item for item in seq if len(item) == 0]) > 0

        if exist_empty_item(list_of_eojeol) or exist_empty_item(list_of_morphtags):
            raise ValueError('Exist empty item in sequence')

        self.eojeols = list_of_eojeol
        self.morphtags = list_of_morphtags

    def __iter__(self):
        for eojeol, morphtags in zip(self.eojeols, self.morphtags):
            yield eojeol, morphtags

    def __len__(self):
        return len(self.eojeols)

    def __getitem__(self, index):
        return self.eojeols[index], self.morphtags[index]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        morphtags_strf = [' + '.join(str(mt) for mt in mts) for mts in self.morphtags]
        strf = '\n'.join(
            '%s\t%s' % (eojeol, morphtags) for eojeol, morphtags in zip(self.eojeols, morphtags_strf))
        return strf

    def get_morphtags(self, flatten=False):
        if not flatten:
            return self.morphtags
        return [mt for mts in self.morphtags for mt in mts]


def load_a_file(path, remain_dummy_morpheme=False, debug=False):
    """
    Argument
    --------
    path : str
        File path
    remain_dummy_morpheme : Boolean
        If True, it remain dummy morphemes
        Else, it removes dummy morphemes
        Default is False
    debug : Boolean
        If True, it shows exception case
        Default is False

    Returns
    -------
    sentences : list of Sentence
        A item in list is tagged sentence.
        For example of written corpus at '../data/raw/written/BTAA0001.txt'

            프랑스의	프랑스/NNP + 의/JKG
            세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
            의상	의상/NNG
            디자이너	디자이너/NNG
            엠마누엘	엠마누엘/NNP
            웅가로가	웅가로/NNP + 가/JKS
            실내	실내/NNG
            장식용	장식/NNG + 용/XSN
            직물	직물/NNG
            디자이너로	디자이너/NNG + 로/JKB
            나섰다.	나서/VV + 었/EP + 다/EF + ./SF

        For example of colloquial corpus at '../data/raw/colloquial/5CT_0016.txt'

            걔	걔/NP
            두	두/MM
            명이	명/NNB + 이/JKS
            하는	하/VV + 는/ETM
            거야.	거/NNB + (이)/VCP + 야/EF + ./SF

    n_errors : int
        Number of failures for parsing text to Sentence

    Usage
    -----
        $ path = '../data/raw/written/BTAA0001.txt'
        $ sentences, n_errors = load_a_file(path)
    """
    soup = read_txt_as_soup(path)

    if is_colloquial_file(path):
        sentences = select_sentence_from_colloquial(soup)
    else:
        sentences = select_sentence_from_written(soup, path)

    sentences = [unicode_sentence(sent) for sent in sentences]
    sentences = [sent for sent in sentences if sent]

    n_errors = len(sentences)
    sentences = [sent for sent in sentences if base_checker(sent)]
    sentences = [unify_morphemes_separator(sent) for sent in sentences]

    n_errors -= len(sentences)
    if debug and n_errors > 0:
        print("Found %d sentences having wrong or empty eojeols" % n_errors)

    sentences_ = []
    for i, sent in enumerate(sentences):
        try:
            sent = as_sentence_instance(sent, remain_dummy_morpheme)
            if check_sejong_tagset(sent):
                sentences_.append(sent)
            else:
                n_errors += 1
                continue
        except Exception as e:
            if debug:
                print('\n\nException message = {}'.format(e))
                print('sentence text : {}'.format(sent))
            n_errors += 1
    return sentences_, n_errors

def as_sentence_instance(sent, remain_dummy_morpheme):
    eojeol_morphtags = [e.split('\t') for e in sent.split('\n')]
    eojeols, morphtags = zip(*eojeol_morphtags)
    morphtags = [[mt.rsplit('/',1) for mt in mts.split(' + ')] for mts in morphtags]

    # remove not exist morphemes
    def is_dummy(morphtag):
        return ('(' in morphtag[0]) and (')' in morphtag[0])

    if not remain_dummy_morpheme:
        morphtags = [[mt for mt in mts if not is_dummy(mt)] for mts in morphtags]

    morphtags = [[MorphTag(m,t) for m,t in mts] for mts in morphtags]
    return Sentence(eojeols, morphtags)

def is_colloquial_file(path):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    flag : Booolean
        Weather the file at path is colloquial corpus or not
    """
    path = os.path.abspath(path)
    filename = path.split(sep)[-1]
    return '_' in filename

def read_txt_as_soup(path, encoding='utf-16'):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    soup : BeautifulSoup
        XML formed document
    """
    try:
        with open(path, encoding=encoding) as f:
            text = f.read()
            soup = BeautifulSoup(text, 'lxml')
            return soup
    except:
        raise ValueError('Failed to read txt: {}'.format(path))

def select_sentence_from_colloquial(soup):
    sentences = str(soup.find('text'))
    sentences = [sent.split('\t',1)[-1] for sent in sentences.split('\n')]
    soup = BeautifulSoup('\n'.join(sentences), 'lxml')
    sentences = [sent.text.strip() for sent in soup.find_all('s')]
    return sentences

def select_sentence_from_written(soup, path):
    def remove_header(sent):
        sent_ = [eojeol.split('\t', 1)[-1].strip() for eojeol in sent.split('\n') if eojeol.count('\t') == 2]
        sent_ = [eojeol for eojeol in sent_ if eojeol]
        return '\n'.join(sent_)

    filename = path.split(sep)[-1][:-4]
    sentences = soup.find_all('p')
    sentences = [sent.text.strip() for sent in sentences]
    sentences = [sent for sent in sentences if sent[:len(filename)] == filename]
    sentences = [remove_header(sent).strip() for sent in sentences]
    return sentences

def base_checker(sent):
    for eojeol in sent.split('\n'):
        # check "따라서\t따라서/Advecb"
        if eojeol.count('\t') != 1:
            return False
        if (not ('/' in eojeol) or
            ('->' in eojeol) or
            # confusing with HTML tags
            ('</SS' in eojeol) or
            ('>/SS' in eojeol) or
            (not eojeol)
           ):
            return False
    return True

def unify_morphemes_separator(sent):
    # because colloquial & written have difference format
    def unify(token):
        if not (' + ' in token):
            token = token.replace('+', ' + ')
            token = token.replace('+ /', '+/')
        return token

    return '\n'.join([unify(token) for token in sent.split('\n') if token])
