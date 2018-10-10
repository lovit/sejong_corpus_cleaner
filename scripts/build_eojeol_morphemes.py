import argparse
from glob import glob

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner.rawtext_loader import load_texts_as_eojeol_morphemes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rawdata_directory', type=str, default='../data/raw/')
    parser.add_argument('--cleandata_directory', type=str, default='../data/clean/')

    args = parser.parse_args()
    rawdata_directory = args.rawdata_directory
    cleandata_directory = args.cleandata_directory

    input_paths = sorted(glob('%s/spoken/*.txt' % rawdata_directory))
    output_path = '%s/eojeol_morphemes_spoken.txt' % cleandata_directory
    create(input_paths, output_path, is_spoken=True)

    input_paths = sorted(glob('%s/written/*.txt' % rawdata_directory))
    output_path = '%s/eojeol_morphemes_written.txt' % cleandata_directory
    create(input_paths, output_path, is_spoken=False)

def create(input_paths, output_path, is_spoken):
    print('with %d texts' % len(input_paths))
    eojeol_morphemes = load_texts_as_eojeol_morphemes(input_paths, is_spoken=is_spoken)
    with open(output_path, 'w', encoding='utf-8') as f:
        for sent in eojeol_morphemes:
            f.write('%s\n\n' % sent)
    print('result in %s' % output_path, end='\n\n')

if __name__ == '__main__':
    main()