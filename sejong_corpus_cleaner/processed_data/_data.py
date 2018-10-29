from .. import separate_eojeol_morphtag

class Corpus:
    def __init__(self, corpus_paths, num_sent=-1):
        if isinstance(corpus_paths, str):
            corpus_paths = [corpus_paths]
        self.paths = corpus_paths
        self.num_sent = num_sent

    def __iter__(self):
        for path in self.paths:            
            with open(path, encoding='utf-8') as f:
                for i, sent in enumerate(f):
                    if self.num_sent > 0 and i > self.num_sent:
                        break
                    morph_poss = [tuple(token.rsplit('/', 1)) for token in sent.split()]
                    yield morph_poss

class EojeolMorphtagSentence:
    def __init__(self, eojeol_morphtag_paths, num_sent=-1):
        if isinstance(eojeol_morphtag_paths, str):
            eojeol_morphtag_paths = [eojeol_morphtag_paths]
        self.paths = eojeol_morphtag_paths
        self.num_sent = num_sent

    def __iter__(self):
        num_sent = 0
        for path in self.paths:
            if self.num_sent > 0 and num_sent >= self.num_sent:
                break
            with open(path, encoding='utf-8') as f:
                eojeol_morphtag = []
                for line in f:
                    if self.num_sent > 0 and num_sent >= self.num_sent:
                        break
                    line = line.strip()
                    if not line:
                        num_sent += 1
                        yield eojeol_morphtag
                        eojeol_morphtag = []
                        continue
                    eojeol_morphtag.append(separate_eojeol_morphtag(line))