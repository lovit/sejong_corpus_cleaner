def make_eojeol_morphemes_table(table_file_path,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    corpus_types = check_corpus_type(corpus_types)
    raise NotImplemented

def make_morpheme_table(table_file_path,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    corpus_types = check_corpus_type(corpus_types)
    raise NotImplemented

def make_lr_corpus(corpus_file_path, xsv_as_verb=False, corpus_types=None):
    corpus_types = check_corpus_type(corpus_types)
    raise NotImplemented

def check_corpus_type(corpus_types):
    if corpus_types is None:
        corpus_types = ['colloquial', 'written']
    for ctype in corpus_types:
        if not (ctype in {'colloquial', 'written'}):
            raise ValueError('Corpus type must be "colloquial" or "written" but {}'.format(ctype))
    return corpus_types
