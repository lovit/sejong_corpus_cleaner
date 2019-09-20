import argparse

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner import get_data_paths
from sejong_corpus_cleaner import make_lr_corpus
from sejong_corpus_cleaner import Sentences
from sejong_corpus_cleaner import write_sentences


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='../data/raw/', help='Raw Sejong corpus directory')
    parser.add_argument('--output_dir', type=str, default='../data/clean/', help='Processed corpus directory')
    parser.add_argument('--input_file_type', type=str, default='all',
        choices=['all', 'written', 'colloquial'], help='Input Sejong corpus types')
    parser.add_argument('--corpus_type', type=str, default='sejong',
        choices=['sejong', 'type1', 'type2', 'type3'], help='Corpus type')
    parser.add_argument('--num_sents', type=int, default=-1, help='Maximum number of sentences')

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    input_file_type = args.input_file_type
    if input_file_type == 'all':
        input_file_type_ = None
    else:
        input_file_type_ = input_file_type
    corpus_type = args.corpus_type
    num_sents = args.num_sents

    paths = get_data_paths(input_file_type_, input_dir)
    if not paths:
        raise ValueError('Check your input directory')

    sents = Sentences(paths, num_sents=num_sents)

    suffix = '_{}{}'.format(input_file_type, '' if num_sents < 0 else '_{}'.format(num_sents))
    path = '{}/corpus_{}{}.txt'.format(output_dir, corpus_type, suffix)

    if corpus_type == 'sejong':
        write_sentences(sents, path)
    elif corpus_type == 'type1':
        make_lr_corpus(sents, filepath=path)
    elif corpus_type == 'type2':
        make_lr_corpus(sents, filepath=path, noun_xsv_as_verb=True)
    elif corpus_type == 'type3':
        make_lr_corpus(sents, filepath=path, xsv_as_root=True)

if __name__ == '__main__':
    main()
