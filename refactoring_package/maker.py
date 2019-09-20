from collections import defaultdict
from .lr import to_lr, preprocess0, preprocess1


def make_lr_eomi_to_sejong_converter(sents, noun_xsv_as_verb):
    """
    Arguments
    ---------
    sentences : list of Sentence or Sentences
        Iterable object consists with Sentence instance
    noun_xsv_as_verb : Boolean
        Option for L-R format transformation.
        If True, it considers Noun + XSV as verb.
        For example,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작하/Verb + 다/Eomi"

        Else it consider XSV + Eomi as surfacial form of verb,

            $ "시작/NNG + 하/XSV + 다/EP" -> "시작/Noun + 하다/Verb"

    Returns
    ------
    rules : list of tuple
        (l, sejong format morphemes, count)
        For example,

            ...
            ((음에/Eomi, (음/ETN, 에/JKB)), 19),
            ((겠다고/Eomi, (겠/EP, 다/EC, 고/JKQ)), 19),
            ((으세요/Eomi, (으시/EP, 어요/EF)), 19),
            ((었느냐고/Eomi, (었/EP, 느냐고/EC)), 19),
            ...
    """
    counter = make_counter(sents, convert_lr=False, eojeol_morpheme_pair=True)
    sorted_counter = sorted(counter.items(), key=lambda x:-x[1])
    converter = defaultdict(int)
    num_exceptions, count_exceptions = 0, 0
    for (eojeol, morphtags), count in sorted_counter:
        try:
            eojeol, l, r, morphtags, b = to_lr(eojeol, morphtags, noun_xsv_as_verb)[0]
        except:
            num_exceptions += 1
            count_exceptions += count
            continue
        if r is None or r.tag != 'Eomi':
            continue
        converter[(r, tuple(morphtags[b+1:]))] += count

    perc = 100 * count_exceptions / sum(counter.values())
    args = (len(converter), num_exceptions, '%.3f' % perc)
    print('Create {} rules with {} ({} %) errors'.format(*args))
    return sorted(converter.items(), key=lambda x:-x[1])

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
        num_exceptions = 0
        count_exceptions = 0
        counter_ = defaultdict(int)
        for (eojeol, morphtags), count in counter.items():
            try:
                results = to_lr(eojeol, morphtags, noun_xsv_as_verb, xsv_as_root, debug=False)
                for eojeol_, l, r in results:
                    key = (eojeol_, (l, r))
                    counter_[key] += count
            except Exception as e:
                num_exceptions += 1
                count_exceptions += count
                if show_exception_cases:
                    print('L-R format converting error in (eojeol={}, morphtags={})'.format(eojeol, morphtags))
                    print(e, end='\n\n')
                continue
        counter = counter_

        count_total = sum(counter.values())
        args = (len(counter_), num_exceptions, '%.3f' % (100 * count_exceptions / count_total) )
        print('Found {} (eojeol, morphtags) pairs with {} ({} %) L-R transformation exception cases'.format(*args))

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
