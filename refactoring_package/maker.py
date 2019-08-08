from glob import glob
from .utils import data_dir as default_data_dir


def make_eojeol_morphemes_table(table_file_path, data_dir=None,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def make_morpheme_table(table_file_path, data_dir=None,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def make_lr_corpus(corpus_file_path, data_dir=None,
    xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def check_corpus_type(corpus_types):
    if corpus_types is None:
        corpus_types = ['written', 'colloquial']
    for ctype in corpus_types:
        if not (ctype in {'written', 'colloquial'}):
            raise ValueError('Corpus type must be "colloquial" or "written" but {}'.format(ctype))
    return corpus_types

def prepare_data_paths(corpus_types=None, data_dir=None):
    corpus_types = check_corpus_type(corpus_types)
    if data_dir is None:
        data_dir = default_data_dir

    paths = []
    for ctype in corpus_types:
        paths += glob(data_dir + ctype + '/*.txt')

    if len(paths) == 0:
        raise ValueError('File not founded from {}'.format(data_dir))
    return paths
