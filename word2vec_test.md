## Word2Vec 테스트

Gensim == 3.6.0 의 Word2Vec 을 이용하여 Type 2 형식의 말뭉치로부터 형태소의 벡터값을 학습합니다.

```python
from gensim.models import Word2Vec
from sejong_corpus_cleaner import Sentences

class TrainCorpus:
    def __init__(self, sents):
        self.sents = sents
    def __iter__(self):
        print('begin')
        for sent in self.sents:
            morphemes = sent.get_morphtags(flatten=True)
            morphemes = [str(m) for m in morphemes]
            yield morphemes
        print('end')

train_corpus = TrainCorpus(Sentences('../data/clean/corpus_type2_all.txt', processed=True))
word2vec = Word2Vec(train_corpus, min_count=10)
```

```python
word2vec.wv.most_similar('대학/Noun', topn=5)

[('대학원/Noun', 0.7880821228027344),
 ('고등학교/Noun', 0.7145887613296509),
 ('학교/Noun', 0.6997007131576538),
 ('학원/Noun', 0.6961156129837036),
 ('중학교/Noun', 0.6852348446846008)]
```

```python
word2vec.wv.most_similar('아름답/Adjective', topn=5)

[('신비하/Adjective', 0.7579469680786133),
 ('우아하/Adjective', 0.7402693033218384),
 ('멋지/Adjective', 0.7361856698989868),
 ('여성스럽/Adjective', 0.7252703309059143),
 ('화려하/Adjective', 0.7235508561134338)]
```

```python
word2vec.wv.most_similar('ㄴ데/Eomi', topn=5)
[('ㄴ데요/Eomi', 0.7969660758972168),
 ('ㄹ세/Eomi', 0.7687995433807373),
 ('라서/Eomi', 0.7653181552886963),
 ('지요/Eomi', 0.7362310886383057),
 ('니까요/Eomi', 0.7309263944625854)]
```

```python
word2vec.wv.most_similar('았는데/Eomi', topn=5)

[('았지만/Eomi', 0.8387665748596191),
 ('았으나/Eomi', 0.8343114852905273),
 ('았고/Eomi', 0.8146823644638062),
 ('았어/Eomi', 0.8040876984596252),
 ('았었는데/Eomi', 0.801535427570343)]
```

```python
word2vec.wv.most_similar('그리고/Adverb', topn=5)

[('왜냐하면/Adverb', 0.6152447462081909),
 ('그러나/Adverb', 0.5601612329483032),
 ('그러므로/Adverb', 0.5578808784484863),
 ('이를테면/Adverb', 0.5548497438430786),
 ('그리하여/Adverb', 0.5488671064376831)]
```

```python
word2vec.wv.most_similar('그/Determiner', topn=5)

[('이/Determiner', 0.6893772482872009),
 ('그런/Determiner', 0.5744611620903015),
 ('그것/Pronoun', 0.5284191966056824),
 ('그러하/Adjective', 0.5235767364501953),
 ('이런/Determiner', 0.5121667385101318)]
```

```python
word2vec.wv.most_similar('첫째/Numeral')

[('둘째/Numeral', 0.8010367155075073),
 ('셋째/Numeral', 0.7484560012817383),
 ('넷째/Numeral', 0.6973210573196411),
 ('다섯째/Numeral', 0.6762571334838867),
 ('학습자/Noun', 0.6170148849487305)]
```
