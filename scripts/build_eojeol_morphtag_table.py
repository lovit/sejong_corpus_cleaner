import argparse
from glob import glob

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner.rawtext_loader import load_texts_as_eojeol_morphtag_table

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rawdata_directory', type=str, default='../data/raw/')
    parser.add_argument('--cleandata_directory', type=str, default='../data/clean/')

    args = parser.parse_args()
    rawdata_directory = args.rawdata_directory
    cleandata_directory = args.cleandata_directory

    input_paths = sorted(glob('%s/colloquial/*.txt' % rawdata_directory))
    output_path = '%s/eojeol_morphtag_table_colloquial.txt' % cleandata_directory
    create(input_paths, output_path, is_colloquial=True)

    input_paths = sorted(glob('%s/written/*.txt' % rawdata_directory))
    output_path = '%s/eojeol_morphtag_table_written.txt' % cleandata_directory
    create(input_paths, output_path, is_colloquial=False)

def create(input_paths, output_path, is_colloquial):
    print('with %d texts' % len(input_paths))
    table = load_texts_as_eojeol_morphtag_table(input_paths, is_colloquial=is_colloquial)
    table.to_csv(output_path)
    print('result in %s' % output_path, end='\n\n')

if __name__ == '__main__':
    main()