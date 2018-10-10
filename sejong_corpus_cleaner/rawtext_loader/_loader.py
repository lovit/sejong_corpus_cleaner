from collections import defaultdict
from bs4 import BeautifulSoup
from pandas import DataFrame

from .. import separate_word_tag
from .. import separate_eojeol_morphemes

def load_texts_as_eojeol_morphemes(filepaths, encoding='utf-16', is_spoken=True):

    if is_spoken:
        loader = load_spoken_text_as_eojeol_morphemes
    else:
        loader = load_written_text_as_eojeol_morphemes

    sentences = []
    for path in filepaths:
        sentences += loader(path, encoding)
    return sentences

def load_written_text_as_eojeol_morphemes(filepath, encoding='utf-16', header=None):

    if not header:
        header = filepath.split('/')[-1][:-4]

    with open(filepath, encoding=encoding) as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')

    sentences = soup.find_all('p')
    sentences = [sent.text.strip() for sent in sentences]
    sentences = [sent for sent in sentences if sent[:len(header)] == header]

    def remove_header(sent):
        sent_ = [eojeol.split('\t', 1)[-1].strip() for eojeol in sent.split('\n') if eojeol.count('\t') == 2]
        sent_ = [eojeol for eojeol in sent_ if eojeol]
        return '\n'.join(sent_)

    sentences = [remove_header(sent).strip() for sent in sentences]
    sentences = [sent for sent in sentences if sent]
    sentences = [sent for sent in sentences if _is_right_form_of_sentence(sent)]
    sentences = [unify_morphemes_separator(sent) for sent in sentences]

    return sentences

def load_spoken_text_as_eojeol_morphemes(filepath, encoding='utf-16', header=None):

    if not header:
        header = filepath.split('/')[-1][:-4]

    with open(filepath, encoding=encoding) as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')

    sentences = str(soup.find('text'))
    sentences = [sent.split('\t',1)[-1] for sent in sentences.split('\n')]

    soup = BeautifulSoup('\n'.join(sentences), 'lxml')
    sentences = [sent.text.strip() for sent in soup.find_all('s')]
    sentences = [sent for sent in sentences if sent]
    sentences = [sent for sent in sentences if _is_right_form_of_sentence(sent)]
    sentences = [unify_morphemes_separator(sent) for sent in sentences]

    return sentences

def unify_morphemes_separator(sent):
    # because spoken & written have difference format
    def unify(token):
        if not (' + ' in token):
            token = token.replace('+', ' + ')
            token = token.replace('+ /', '+/')
        return token

    return '\n'.join([unify(token) for token in sent.split('\n') if token])

def _is_right_form_of_sentence(sent):
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

def load_texts_as_corpus(paths, is_spoken=True):
    if is_spoken:
        loader = load_spoken_text_as_eojeol_morphemes
    else:
        loader = load_written_text_as_eojeol_morphemes

    def sent_to_poses(sent):
        return [pos for token in sent.split('\n')
                    for pos in separate_eojeol_morphemes(token)[1]]

    sentences_ = []
    for path in paths:
        sentences = loader(path)
        sentences = [sent_to_poses(sent) for sent in sentences]
        sentences_ += sentences

    return sentences_

def load_texts_as_eojeol_morphemes_table(paths, is_spoken=True, return_as_dict=False):
    if is_spoken:
        loader = load_spoken_text_as_eojeol_morphemes
    else:
        loader = load_written_text_as_eojeol_morphemes

    counter = defaultdict(int)
    for path in paths:
        sentences = loader(path)
        for sent in sentences:
            for eojeol_morphemes in sent.split('\n'):
                try:
                    eojeol, morphemes = eojeol_morphemes.split('\t')
                    morphemes = morphemes.replace(' + ', ' ')
                    counter[(eojeol, morphemes)] += 1
                except:
                    continue

    if return_as_dict:
        return dict(counter)
    return _to_data_frame(counter)

def _to_data_frame(counter):
    def is_compound(morphemes):
        return morphemes.count(' ') > 0

    df = DataFrame(
        [(eojeol, morphemes, count, is_compound(morphemes)) for (eojeol, morphemes), count in
         sorted(counter.items(), key=lambda x:(-x[1], x[0][0]))],
        columns = 'Eojeol morphemes Count Is_compound'.split()
    )
    return df
