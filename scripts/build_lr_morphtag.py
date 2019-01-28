import argparse

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner.simplifier import eojeol_morphtags_sentence_to_lr
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
            sent_ = eojeol_morphtags_sentence_to_lr(sent, separate_xsv=False)
            if len(sent_) != len(sent_):
                n_exceptions += 1
                continue

            sent_ = [eojeol_to_strf(l, r, l_tag, r_tag) for l, r, l_tag, r_tag in sent_]
            for (eojeol, morphtags), lr in zip(sent, sent_):
                morphtags_strf = ' '.join(['{}/{}'.format(m,t) for m,t in morphtags])
                f.write('{}\t{}\t{}\n'.format(eojeol, morphtags_strf, lr))
            f.write('\n')

        except Exception as e:
            n_exceptions += 1
            #print('\nException: sent # {}'.format(i))
            #print(e)
            #print()
            #break

    print('\rbuilding was done. (%d sents, %d exceptions)' % (i + 1, n_exceptions))

if __name__ == '__main__':
    main()