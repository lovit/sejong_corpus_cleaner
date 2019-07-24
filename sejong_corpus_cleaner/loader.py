from bs4 import BeautifulSoup
import os

from .utils import unicode_sentence


sep = os.path.sep

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

def extract_sentences(path):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    sentences : list of str
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
    """
    soup = read_txt_as_soup(path)

    if is_colloquial_file(path):
        sentences = from_colloquial(soup)
    else:
        sentences = from_written(soup, path)

    sentences = [unicode_sentence(sent) for sent in sentences]
    sentences = [sent for sent in sentences if sent]
    sentences = [sent for sent in sentences if check_sentence(sent)]
    sentences = [unify_morphemes_separator(sent) for sent in sentences]
    return sentences

def from_colloquial(soup):
    sentences = str(soup.find('text'))
    sentences = [sent.split('\t',1)[-1] for sent in sentences.split('\n')]
    soup = BeautifulSoup('\n'.join(sentences), 'lxml')
    sentences = [sent.text.strip() for sent in soup.find_all('s')]
    return sentences

def from_written(soup, path):
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

def check_sentence(sent):
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
