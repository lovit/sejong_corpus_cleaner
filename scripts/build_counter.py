import argparse

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner import get_data_paths
from sejong_corpus_cleaner import make_counter
from sejong_corpus_cleaner import Sentences

def pair_to_str(pair_key):
    eojeol, morphemes = pair_key
    return '{}\t{}'.format(eojeol, ' + '.join(str(m) for m in morphemes))

def morphtag_to_str(key):
    return str(key)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='../data/raw/', help='Raw Sejong corpus directory')
    parser.add_argument('--output_dir', type=str, default='../data/clean/', help='Processed corpus directory')
    parser.add_argument('--input_file_type', type=str, default='all',
        choices=['all', 'written', 'colloquial'], help='Input Sejong corpus types')
    parser.add_argument('--corpus_type', type=str, default='sejong',
        choices=['sejong', 'type1', 'type2', 'type3'], help='Corpus type')
    parser.add_argument('--only_morphemes', dest='only_morphemes', action='store_true', help='Count only morphemes')
    parser.add_argument('--num_sents', type=int, default=-1, help='Maximum number of sentences')

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    input_file_type = args.input_file_type
    if input_file_type == 'all':
        input_file_type = None
    corpus_type = args.corpus_type
    eojeol_morpheme_pair = not args.only_morphemes
    num_sents = args.num_sents

    paths = get_data_paths(input_file_type, input_dir)
    if not paths:
        raise ValueError('Check your input directory')

    sents = Sentences(paths, num_sents=num_sents)

    suffix = '' if num_sents < 0 else '_{}'.format(num_sents)
    suffix += '_pair' if eojeol_morpheme_pair else '_morpheme'
    if input_file_type is None:
        input_file_type = 'all'
    suffix += '_{}'.format(input_file_type)
    path = '{}/counter_{}{}.txt'.format(output_dir, corpus_type, suffix)

    if corpus_type == 'sejong':
        counter = make_counter(sents, eojeol_morpheme_pair)
    elif corpus_type == 'type1':
        counter = make_counter(sents, eojeol_morpheme_pair, convert_lr=True)
    elif corpus_type == 'type2':
        counter = make_counter(sents, eojeol_morpheme_pair, convert_lr=True, noun_xsv_as_verb=True)
    elif corpus_type == 'type3':
        counter = make_counter(sents, eojeol_morpheme_pair, convert_lr=True, xsv_as_root=True)

    to_key = pair_to_str if eojeol_morpheme_pair else morphtag_to_str
    with open(path, 'w', encoding='utf-8') as f:
        for key, count in sorted(counter.items(), key=lambda x:-x[1]):
            if key is None:
                continue
            key = to_key(key)
            f.write('{}\t{}\n'.format(key, count))

    print('Saved counter to {}'.format(path))

if __name__ == '__main__':
    main()
