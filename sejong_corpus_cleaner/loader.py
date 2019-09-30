from collections import namedtuple
from bs4 import BeautifulSoup
from glob import glob
import os

from .format_checker import check_sejong_tagset
from .utils import unicode_sentence
from .utils import data_dir as default_data_dir


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

        def preprocessing(list_of_eojeol, list_of_morphtags):
            eojeols_ = []
            morphtags_ = []
            for eojeol, morphtags in zip(list_of_eojeol, list_of_morphtags):
                if (not eojeol) and ((not morphtags) or (morphtags[0] is None)):
                    continue
                if eojeol and (morphtags and morphtags[0] is not None):
                    eojeols_.append(eojeol)
                    morphtags_.append(morphtags)
                else:
                    raise ValueError('Exist empty item in sequence\neojeols = {}\nmorphtags = {}'.format(
                        list_of_eojeol, list_of_morphtags))
            return eojeols_, morphtags_

        self.eojeols, self.morphtags = preprocessing(list_of_eojeol, list_of_morphtags)

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
        strf += '\n'
        return strf

    def get_morphtags(self, flatten=False):
        if not flatten:
            return self.morphtags
        return [mt for mts in self.morphtags for mt in mts]


class Sentences:
    """
    Arguments
    ---------
    file_paths : list or str
        Sejong corpus file paths
    verbose : Boolean
        If True, it shows progress of iteration
    processed : Boolean
        If False, it loads raw Sejong corpus file
        Else, it loads processed corpus file
    num_sents : int
        Maximum number of sentences
        If the value is negative, it loads all sentences
    """
    def __init__(self, file_paths=None, verbose=True, processed=False, num_sents=-1):
        if file_paths is None:
            file_paths = get_data_paths()
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        self.file_paths = file_paths
        self.verbose = verbose
        self.processed = processed
        self.num_sents = num_sents

    def __iter__(self):
        n_sents_, n_errors_, n_iters = 0, 0, 0
        for i, path in enumerate(self.file_paths):
            if self.num_sents > 0 and self.num_sents <= n_iters:
                break

            if not self.processed:
                sents, n_errors = load_a_sejong_file(path,
                    remain_dummy_morpheme=False, num_sents=self.num_sents)
                n_sents_ += len(sents)
                n_errors_ += n_errors
            else:
                sents = load_a_sentences_file(path, num_sents=self.num_sents)
                n_sents_ += len(sents)

            for sent in sents:
                yield sent
                n_iters += 1
                if self.num_sents > 0 and self.num_sents <= n_iters:
                    break

            if self.verbose:
                args = (n_sents_, n_errors_, i+1, len(self.file_paths))
                print('\rIterating {} sents + {} errors from {} / {} files'.format(*args), end='')
        if self.verbose:
            args = (n_sents_, n_errors_, len(self.file_paths), ' '*20)
            print('\rIterated {} sents + {} errors from {} files{}'.format(*args))

    def __len__(self):
        i = -1
        for i, _ in enumerate(self.__iter__()):
            continue
        return i + 1


def check_corpus_type(corpus_types):
    """
    Argument
    --------
    corpus_types : str or None
        Available : ['written', 'colloquial']

    Returns
    -------
    flag : Boolean
        Return True if corpus types is one of ['written', 'colloquial', None]
    """
    if corpus_types is None:
        corpus_types = ['written', 'colloquial']
    if isinstance(corpus_types, str):
        corpus_types = [corpus_types]
    for ctype in corpus_types:
        if not (ctype in {'written', 'colloquial'}):
            raise ValueError('Corpus type must be "colloquial" or "written" but {}'.format(ctype))
    return corpus_types

def get_data_paths(corpus_types=None, data_dir=None):
    """
    Arguments
    ---------
    corpus_types : str or None
        Available : ['written', 'colloquial']
    data_dir : str or None
        Data directory

    Returns
    -------
    paths : list of str
        File paths
    """
    corpus_types = check_corpus_type(corpus_types)
    if data_dir is None:
        data_dir = default_data_dir

    paths = []
    for ctype in corpus_types:
        paths += sorted(glob(data_dir + ctype + '/*.txt'))

    if len(paths) == 0:
        raise ValueError('File not founded from {}'.format(data_dir))
    return paths

def load_a_sentences_file(path, num_sents=-1):
    """
    Arguments
    ---------
    path : str
        Sentences format file path
    num_sents : int
        Maximum number of sentences
        If the value is negative, it loads all sentences

    Returns
    -------
    sents : list of Sentence
    """
    sents = []
    with open(path, encoding='utf-8') as f:
        eojeols = []
        list_of_morphtags = []
        for line in f:
            if num_sents > 0 and len(sents) >= num_sents:
                eojeols = []
                break
            line = line.strip()
            if not line and eojeols:
                sent = Sentence(eojeols, list_of_morphtags)
                sents.append(sent)
                eojeols = []
                list_of_morphtags = []
                continue
            if not line:
                continue
            eojeol, morphtags = line.split('\t')
            morphtags = [MorphTag(*mt.rsplit('/', 1)) for mt in morphtags.split(' + ')]
            eojeols.append(eojeol)
            list_of_morphtags.append(morphtags)
    if eojeols:
        sent = Sentence(eojeols, list_of_morphtags)
        sents.append(sent)
    return sents

def load_a_sejong_file(path, remain_dummy_morpheme=False, debug=False, num_sents=-1):
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
    num_sents : int
        Maximum number of sentences
        If the value is negative, it loads all sentences

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
        $ sentences, n_errors = load_a_sejong_file(path)
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
        if num_sents > 0 and len(sentences_) >= num_sents:
            break
        try:
            sent = as_sentence_instance(sent, remain_dummy_morpheme)
            if check_sejong_tagset(sent):
                sentences_.append(sent)
            else:
                if debug:
                    print('Found wrong sejong tag from {} th sent'.format(i))
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

def load_count_table(path, sep='\t'):
    """
    Arguments
    ---------
    path : str
        Table file path
    sep : str
        Separator
    """

    def cast(row):
        key = row[:-1]
        if len(key) == 1:
            key = key[0]
        elif len(key) == 2:
            eojeol, morphtags = key
            morphtags = [mt.rsplit('/', 1) for mt in morphtags.split(" + ")]
            morphtags = [MorphTag(morph, tag) for morph, tag in morphtags]
            key = (eojeol, morphtags)
        else:
            raise ValueError('Check table format')
        count = int(row[-1])
        return (key, count)

    with open(path, encoding='utf-8') as f:
        rows = [row.strip() for row in f]
    rows = [row.split(sep) for row in rows if row]
    rows_ = []
    for row in rows:
        try:
            rows_.append(cast(row))
        except Exception as e:
            print('Exception while casting row = {}'.format(row))
            raise ValueError(e)
    return rows_
