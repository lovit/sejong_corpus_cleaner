import subprocess


def check_encoding(list_of_paths):
    list_of_encodings = [subprocess.getstatusoutput("file %s" % path)[1]
        for path in list_of_paths]
    return list_of_encodings

def write_corpus(corpus, path):
    def pos_to_strf(pos):
        return '%s/%s' % pos

    with open(path, 'w', encoding='utf-8') as f:
        for sent in corpus:
            sent_strf = ' '.join(pos_to_strf(pos) for pos in sent)
            f.write('%s\n' % sent_strf)

def separate_word_tag(pos):
    return tuple(pos.rsplit('/', 1))

def separate_eojeol_morphemes(eojeol_morphemes):
    eojeol, morphemes = eojeol_morphemes.split('\t')
    poses = [separate_word_tag(pos) for pos in morphemes.split(' + ')]
    return eojeol, poses

def find_tag_snippets(corpus, tag, count=100, window=2):
    def has_tag(sent, tag):
        return [i for i, wt in enumerate(sent) if wt[1] == tag]

    snippest = []
    for sent in corpus:
        if len(snippest) >= count:
            break
        tag_idxs = has_tag(sent, tag)
        for idx in tag_idxs:
            snippest.append(sent[idx - window : idx + window + 1])
    return snippest[:count]

unicode_mapper = {
  'ᆨ': 'ㄱ',
  'ᆩ': 'ㄲ',
  'ᆪ': 'ㄳ',
  'ᆫ': 'ㄴ',
  'ᆬ': 'ㄵ',
  'ᆭ': 'ㄶ',
  'ᆮ': 'ㄷ',
  'ᆯ': 'ㄹ',
  'ᆰ': 'ㄺ',
  'ᆱ': 'ㄻ',
  'ᆲ': 'ㄼ',
  'ᆳ': 'ㄽ',
  'ᆴ': 'ㄾ',
  'ᆵ': 'ㄿ',
  'ᆶ': 'ㅀ',
  'ᄆ': 'ㅁ', # 4358
  'ᆷ': 'ㅁ', # 4535
  'ᆸ': 'ㅂ',
  'ᆹ': 'ㅄ',
  'ᆺ': 'ㅅ',
  'ᆻ': 'ㅆ',
  'ᆼ': 'ㅇ',
  'ᆽ': 'ㅈ',
  'ᆾ': 'ㅊ',
  'ᆿ': 'ㅋ',
  'ᇀ': 'ㅌ',
  'ᇁ': 'ㅍ',
  'ᇂ': 'ㅎ',
}

def unicode_character(c):
    return unicode_mapper.get(c, c)

def unicode_sentence(sent):
    return ''.join(unicode_character(c) for c in sent)