from collections import defaultdict
from .lr import to_lr


def make_eojeol_morphemes_table(table_file_path, data_dir=None,
    convert_lr=False, xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def make_counter(sentences, eojeol_morpheme_pair=True, convert_lr=False,
    noun_xsv_as_verb=False, xsv_as_root=False, show_exception_cases=False):
    """
    Arguments
    ---------
    sentences : list of Sentence or Sentences
        Iterable object consists with Sentence instance
    eojeol_morpheme_pair : Boolean
        If True, the key of counter is ("eojeol", ("morph/tag", "morph/tag", ...))
        Else, the key of counter is "morph/tag"
        Default is True
    convert_lr : Boolean
        If True, it transforms morphtags to L-R format
        Else, it uses sejong corpus tag structure.
    noun_xsv_as_verb : Boolean
        Option for L-R format transformation.
        If True, it considers Noun + XSV as verb.
        For example,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작하/Verb + 다/Eomi"

        Else it consider XSV + Eomi as surfacial form of verb,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    xsv_as_root : Boolean
        Option for L-R format transformation.
        It executes only when noun_xsv_as_verb is False
        If True, it considers XSV as root of verb

            $ "시작/NNG + 하/XSV + 다/EP" -> ["시작/Noun", "하/Verb + 다/Eomi"]

        Else

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    show_exception_cases : Boolean
        If True, it shows exception cases for debugging.

    Returns
    -------
    counter : {key:frequency}
    """

    counter = defaultdict(int)
    for sent in sentences:
        for eojeol, morphtags in sent:
            key = (eojeol, tuple(morphtags))
            counter[key] += 1

    if convert_lr:
        n_transform_exceptions = 0
        # TODO : xsv_as_root option
        counter_ = defaultdict(int)
        for (eojeol, morphtags), count in counter.items():
            try:
                eojeol_, l, r = to_lr(eojeol, morphtags, noun_xsv_as_verb, debug=False)[0]
                key = (eojeol_, (l, r))
                counter_[key] += count
            except Exception as e:
                n_transform_exceptions += 1
                if show_exception_cases:
                    print('L-R format converting error in (eojeol={}, morphtags={})'.format(eojeol, morphtags))
                    print(e, end='\n\n')
                continue
        counter = counter_

        print('Found {} (eojeol, morphtags) pairs with {} L-R transformation exception cases'.format(
            len(counter_), n_transform_exceptions))

    if not eojeol_morpheme_pair:
        morph_counter = defaultdict(int)
        for (eojeol, morphemes), count in counter.items():
            for morph in morphemes:
                morph_counter[morph] += count
        return dict(morph_counter)

    return dict(counter)

def make_morpheme_table(table_file_path, data_dir=None,
    convert_lr=False, noun_xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented

def make_lr_corpus(corpus_file_path, data_dir=None,
    noun_xsv_as_verb=False, corpus_types=None):

    paths = prepare_data_paths(corpus_types, data_dir)
    raise NotImplemented
