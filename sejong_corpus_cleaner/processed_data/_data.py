from .. import separate_eojeol_poses

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

class EojeolPoses:
    def __init__(self, eojeol_poses_paths, num_eojeol=-1):
        if isinstance(eojeol_poses_paths, str):
            eojeol_poses_paths = [eojeol_poses_paths]
        self.paths = eojeol_poses_paths
        self.num_eojeol = num_eojeol

    def __iter__(self):
        num_eojeol = 0
        for path in self.paths:
            with open(path, encoding='utf-8') as f:
                for line in f:
                    if (self.num_eojeol > 0) and (num_eojeol >= self.num_eojeol):
                        break
                    line = line.strip()
                    if not line:
                        continue
                    num_eojeol += 1
                    yield separate_eojeol_poses(line)