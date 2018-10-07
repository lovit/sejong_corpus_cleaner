import subprocess
from bs4 import BeautifulSoup

def check_encoding(list_of_paths):
    list_of_encodings = [subprocess.getstatusoutput("file %s" % path)[1]
        for path in list_of_paths]
    return list_of_encodings

def load_written_text_as_sentences(filepath, encoding='utf-8', header=None):

    if not header:
        header = filepath.split('/')[-1][:-4]

    with open(filepath, encoding='utf-16') as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')

    sentences = soup.find_all('p')
    sentences = [sent.text.strip() for sent in sentences]
    sentences = [sent for sent in sentences if sent[:len(header)] == header]

    def remove_header(sent):
        return '\n'.join(eojeol.split('\t', 1)[-1] for eojeol in sent.split('\n'))

    sentences = [remove_header(sent) for sent in sentences]

    return sentences

def load_spoken_text_as_sentences(filepath, encoding='utf-8', header=None):

    if not header:
        header = filepath.split('/')[-1][:-4]

    with open(filepath, encoding='utf-16') as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml')

    sentences = str(soup.find('text'))
    sentences = [sent.split('\t',1)[-1] for sent in sentences.split('\n')]

    soup = BeautifulSoup('\n'.join(sentences), 'lxml')
    sentences = [sent.text.strip() for sent in soup.find_all('s')]

    return sentences