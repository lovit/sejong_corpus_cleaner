from collections import defaultdict
from glob import glob
from .loader import load_a_file
from .lr import to_lr
from .utils import data_dir as default_data_dir


def make_eojeol_morphemes_table(table_file_path, data_dir=None,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def load_counter(file_paths, eojeol_morpheme_pair=True, convert_lr=False, xsv_as_verb=False, xsv_as_root=False):
    """
    Arguments
    ---------
    file_paths : list of str
        Sejong corpus file paths
    eojeol_morpheme_pair : Boolean
        If True, the key of counter is ("eojeol", ("morph/tag", "morph/tag", ...))
        Else, the key of counter is "morph/tag"
        Default is True
    convert_lr : Boolean
        If True, it transforms morphtags to L-R format
        Else, it uses sejong corpus tag structure.
    xsv_as_verb : Boolean
        Option for L-R format transformation.
        If True, it considers Noun + XSV as verb.
        For example,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작하/Verb + 다/Eomi"

        Else it consider XSV + Eomi as surfacial form of verb,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    xsv_as_root : Boolean
        Option for L-R format transformation.
        It executes only when xsv_as_verb is False
        If True, it considers XSV as root of verb

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하/Verb + 다/Eomi"

        Else

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    Returns
    -------
    counter : {key:frequency}
    """

    counter = defaultdict(int)
    n_sents_ = 0
    n_errors_ = 0

    for path in file_paths:
        sents, n_errors = load_a_file(path, remain_dummy_morpheme=False)
        n_sents_ += len(sents)
        n_errors_ += n_errors
        for sent in sents:
            for eojeol, morphtags in sent:
                key = (eojeol, tuple(morphtags))
                counter[key] += 1
    print('Loaded {} sents with {} errors from {} files'.format(n_sents_, n_errors_, len(file_paths)))

    # TODO: L-R converting
    if convert_lr:
        # TODO : xsv_as_root option
        counter_ = defaultdict(int)
        for (eojeol, morphtags), count in counter.items():
            try:
                eojeol_, l, r = to_lr(eojeol, morphtags, xsv_as_verb=xsv_as_verb, debug=False)
                key = (eojeol_, l, r)
                counter_[key] += count
            except Exception as e:
                print('L-R format converting error in (eojeol={}, morphtags={})'.format(eojeol, morphtags))
                print(e, end='\n\n')
                continue

        counter = counter_

    if not eojeol_morpheme_pair:
        morph_counter = defaultdict(int)
        for (eojeol, morphemes), count in counter.items():
            for morph in morphemes:
                morph_counter[morph] += count
        return dict(morph_counter)

    return dict(counter)

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
