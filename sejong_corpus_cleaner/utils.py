import subprocess


def check_encoding(list_of_paths):
    list_of_encodings = [subprocess.getstatusoutput("file %s" % path)[1]
        for path in list_of_paths]
    return list_of_encodings

def write_sentences(sentences, path):
    with open(path, 'w', encoding='utf-8') as f:
        for sent in sentences:
            f.write('%s\n' % sent)

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