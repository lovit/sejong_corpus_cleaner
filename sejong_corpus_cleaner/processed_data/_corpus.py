class Corpus:

    def __init__(self, morpheme_sentence_path, num_sent=-1):
        self.path = morpheme_sentence_path
        self.num_sent = num_sent

    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for i, sent in enumerate(f):
                if self.num_sent > 0 and i > self.num_sent:
                    break
                morph_poss = [tuple(token.rsplit('/', 1)) for token in sent.split()]
                yield morph_poss