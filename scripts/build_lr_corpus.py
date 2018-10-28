import argparse

import sys
sys.path.insert(0, '../')
from sejong_corpus_cleaner.simplifier import eojeol_poses_sentence_to_lr
from sejong_corpus_cleaner.processed_data import EojeolPosesSentence

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleandata_directory', type=str, default='../data/clean/')
    parser.add_argument('--spoken_input_filename', type=str, default='eojeol_poses_spoken.txt')
    parser.add_argument('--written_input_filename', type=str, default='eojeol_poses_written.txt')
    parser.add_argument('--separate_xsv', dest='separate_xsv', action='store_true')

    args = parser.parse_args()
    dirs = args.cleandata_directory
    spoken_input = args.spoken_input_filename
    written_input = args.written_input_filename
    separate_xsv = args.separate_xsv

    suffix = '_sepxsv' if separate_xsv else '_unsepxsv'

    # log_path = '%s/lr_converting_error.txt' % (dirs)
    # fe = open(log_path, 'w', encoding='utf-8')
    # fe.write('# SPOKEN CORPUS\n')

    input_path = '%s/%s' % (dirs, spoken_input)
    corpus_path = '%s/lrcorpus_spoken%s.txt' % (dirs, suffix)
    sentence_path = '%s/lrsentence_spoken.txt' % dirs
    with open(corpus_path, 'w', encoding='utf-8') as fc:
        with open(sentence_path, 'w', encoding='utf-8') as fs:
            create(input_path, corpus_path, sentence_path, fc, fs, separate_xsv)

    # fe.write('# WRITTEN CORPUS\n')

    input_path = '%s/%s' % (dirs, written_input)
    corpus_path = '%s/lrcorpus_written%s.txt' % (dirs, suffix)
    sentence_path = '%s/lrsentence_written.txt' % dirs
    with open(corpus_path, 'w', encoding='utf-8') as fc:
        with open(sentence_path, 'w', encoding='utf-8') as fs:
            create(input_path, corpus_path, sentence_path, fc, fs, separate_xsv)

    # fe.close()

def create(input_path, corpus_path, sentence_path, fc, fs, separate_xsv):

    def eojeol_to_strf(l, r, l_tag, r_tag):
        if not r:
            return '%s/%s' % (l, l_tag)
        return '%s/%s %s/%s' % (l, l_tag, r, r_tag)

    eps = EojeolPosesSentence(input_path)
    n_exceptions = 0

    for i, sent in enumerate(eps):
        if i % 1000 == 0:
            print('\rbuilding %d sents' % i, end='', flush=True)

        try:
            sent_ = eojeol_poses_sentence_to_lr(sent, separate_xsv)

            eojeol_strfs = [eojeol_to_strf(l, r, l_tag, r_tag) for l, r, l_tag, r_tag in sent_]
            for eojeol_strf in eojeol_strfs:
                fs.write('%s\n' % eojeol_strf)
            fs.write('\n')

            sent_strf = ' '.join(eojeol_strfs)
            fc.write('%s\n' % sent_strf)

        except Exception as e:
            n_exceptions += 1
            #print('\nException: sent # {}'.format(i))
            #print(e)
            #print()
            # break

    print('\rbuilding was done. (%d sents, %d exceptions)' % (i + 1, n_exceptions))

if __name__ == '__main__':
    main()