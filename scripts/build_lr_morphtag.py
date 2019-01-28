import argparse
import re

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner.simplifier import eojeol_morphtags_to_lr
from sejong_corpus_cleaner.processed_data import EojeolMorphtagSentence

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleandata_directory', type=str, default='../data/clean/')
    parser.add_argument('--colloquial_input_filename', type=str, default='eojeol_morphtag_colloquial.txt')
    parser.add_argument('--written_input_filename', type=str, default='eojeol_morphtag_written.txt')

    args = parser.parse_args()
    dirs = args.cleandata_directory
    colloquial_input = args.colloquial_input_filename
    written_input = args.written_input_filename

    input_path = '%s/%s' % (dirs, colloquial_input)
    output_path = '%s/lr_eojeol_morphtag_colloquial.txt' % dirs
    with open(output_path, 'w', encoding='utf-8') as f:
        create(input_path, f)

    # fe.write('# WRITTEN CORPUS\n')

    input_path = '%s/%s' % (dirs, written_input)
    output_path = '%s/lr_eojeol_morphtag_written.txt' % dirs
    with open(output_path, 'w', encoding='utf-8') as f:
        create(input_path, f)

def only_hangle(s):
    pattern = re.compile('[^가-힣]+')
    return pattern.sub('', s)

def create(input_path, f):

    def eojeol_to_strf(l, r, l_tag, r_tag):
        if not r:
            return '%s/%s' % (l, l_tag)
        return '%s/%s %s/%s' % (l, l_tag, r, r_tag)

    eps = EojeolMorphtagSentence(input_path)
    n_exceptions = 0

    for i, sent in enumerate(eps):
        if i % 1000 == 0:
            print('\rbuilding %d sents' % i, end='', flush=True)

        try:
            for eojeol, morphtags in sent:
                lr_unsep = eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv=False)[0]
                lr_sep = eojeol_morphtags_to_lr(eojeol, morphtags, separate_xsv=True)
                if len(lr_sep) == 2:
                    eojeol = only_hangle(eojeol)
                    lr_sep = (lr_sep[0][0], eojeol[len(lr_sep[0][0]):], lr_sep[0][2], 'Josa')
                else:
                    lr_sep = lr_sep[0]

                morphtags_strf = ' '.join(['{}/{}'.format(m,t) for m,t in morphtags])
                lr_unsep_strf = eojeol_to_strf(*lr_unsep)
                lr_sep_strf = eojeol_to_strf(*lr_sep)
                f.write('{}\t{}\t{}\t{}\n'.format(eojeol, morphtags_strf, lr_unsep_strf, lr_sep_strf))
            f.write('\n')

        except Exception as e:
            n_exceptions += 1
            #print('\nException: sent # {}'.format(i))
            #print(e)
            #print(lr_unsep)
            #print(lr_sep)
            #print()
            #break

    print('\rbuilding was done. (%d sents, %d exceptions)' % (i + 1, n_exceptions))

if __name__ == '__main__':
    main()