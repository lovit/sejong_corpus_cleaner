# 세종 말뭉치 정제를 위한 utils

국립국어원에서 배포한 세종 말뭉치로부터 학습에 필요한 부분만을 취하기 위한 utils 입니다. 세종 말뭉치 데이터는 재배포가 제한되어 있기 때문에 원 데이터에서부터 필요한 정보를 추출하는 함수를 작성하였습니다.

## 디렉토리 구조

README 의 예시 코드는 아래의 폴더 구조를 전제합니다. script 폴더 안에서 작업한 코드 예시 입니다.

    |- sejong_corpus_cleaner
    |- data # 데이터 폴더
        |- raw
            |- colloquial  # 구어 말뭉치, 200 개 파일
                |- 5CT_0013.txt
                |- 5CT_0014.txt
                |- 5CT_0015.txt
                |- ...
                |- 9CT_0012.txt
                |- 9CT_0013.txt
            |- written # 문어 말뭉치, 279 개 파일
                |- BTAA0001.txt
                |- BTAA0002.txt
                |- ...
                |- BTJO0446.txt
                |- BTJO0447.txt
        |- clean # 정제된 세종 말뭉치 폴더
    |- scripts #코드 폴더
    |- README.md


## 스크립트 사용법

세종 말뭉치의 원 파일에는 여러 메타 정보 및 오류가 포함되어 있습니다. 이들을 제거한 뒤, (어절, 형태소열) 단위로 기록된 정제된 말뭉치를 만들기 위해서는 `scripts` 디렉토리의 `build_corpus.py` 파일을 이용할 수 있습니다.

세종 말뭉치를 정제하기 위해서는 다음을 실행합니다.

```
cd scripts
python build_corpus.py  --corpus_type sejong
```

세종 말뭉치의 품사 체계가 아닌, 복합형태소가 하나의 형태소로 축약된 L+[R] 형식의 말뭉치를 만들기 위해서는 다음의 스크립트를 실행합니다. 각 타입에 대한 설명은 아래를 참고하세요.

```
python build_corpus.py  --corpus_type type1
python build_corpus.py  --corpus_type type2
python build_corpus.py  --corpus_type type3
```

말뭉치를 만들 때 사용할 수 있는 옵션은 다음과 같습니다.

| Argument | Type | Default value | Help |
| --- | --- | --- | --- |
| input_dir | str | '../data/raw/' | Raw Sejong corpus directory |
| output_dir | str | '../data/clean/' | Processed corpus directory |
| input_file_type | str | 'all' | Input Sejong corpus type, choices=['all', 'written', 'colloquial'] |
| corpus_type | str | 'sejong' | Corpus type, choices=['sejong', 'type1', 'type2', 'type3'] |
| num_sents | int | -1 | Maximum number of sentences |

테스트 용으로 Type 2 형식으로 100 문장의 말뭉치를 만들기 위해서는 다음을 실행합니다.

```
python build_corpus.py  --corpus_type type2 --num_sents 100
```

(어절, 형태소열) 빈도를 테이블로 생성할 수 있습니다.

```
python build_counter.py --corpus_type type1
```

다음의 폴더에 파일이 생성됩니다. (어절, 형태소열, 빈도수) 가 tap 으로 구분됩니다.

```
cd data/clean
cat counter_type1_pair.txt
```

```
등	등/Noun + None	20
있다	있/Verb + 다/Eomi	19
있는	있/Verb + 는/Eomi	16
...
```

형태소의 빈도수만 계산하고 싶을 때는 `only_morphemes` 을 활성화 합니다.

```
cd scripts
python build_counter.py --corpus_type type1 --only_morphemes
```

```
cd data/clean
cat counter_type1_morpheme.txt
```

```
ㄴ/Eomi	73
는/Eomi	71
이/Josa	67
...
```

이 역시 다음의 옵션을 이용할 수 있습니다.

| Argument | Type | Default value | Help |
| --- | --- | --- | --- |
| input_dir | str | '../data/raw/' | Raw Sejong corpus directory |
| output_dir | str | '../data/clean/' | Processed corpus directory |
| input_file_type | str | 'all' | Input Sejong corpus type, choices=['all', 'written', 'colloquial'] |
| corpus_type | str | 'sejong' | Corpus type, choices=['sejong', 'type1', 'type2', 'type3'] |
| num_sents | int | -1 | Maximum number of sentences |
| only_morphemes | str | False | store_true, Count only morphemes |


## 패키지 사용법

### 세종 말뭉치 파일 주소 가져오기

위의 디렉토리 구조로 데이터를 저장해 두었다면 다음의 함수를 이용하여 세종 말뭉치 파일의 주소를 가져올 수 있습니다.

```python
from sejong_corpus_cleaner import get_data_path

paths = get_data_paths()
paths = get_data_paths(corpus_types='written') # 문어체 말뭉치만 가져올 경우
paths = get_data_paths(corpus_types='colloquial') # 구어체 말뭉치만 가져올 경우

print(paths)
```

```
[
 ...
 '~/sejong_corpus_cleaner/data/raw/written/BTAA0001.txt',
 '~/sejong_corpus_cleaner/data/raw/written/BTAA0002.txt',
 '~/sejong_corpus_cleaner/data/raw/written/BTAA0003.txt'
 ...
]
```

### 파일 인코딩 확인하기

세종 말뭉치의 파일 인코딩은 utf-16 입니다. 파일의 인코딩을 확인하기 위하여 **check_encoding** 를 이용할 수 있습니다. check_encoding 에는 list of str 형식의 파일 주소들을 입력합니다. 각 파일의 encoding 이 return 됩니다. Ubuntu OS 의 terminal command 인 file 함수를 이용합니다. Window OS 를 지원하지 않습니다. 하지만 말뭉치 정제를 위해서 이 함수가 반드시 실행되어야 하는 것은 아닙니다. 파일 인코딩 확인용 함수입니다.

```python
from sejong_corpus_cleaner import check_encoding

check_encoding(paths)
```

```
[
  '../data/raw/colloquial/5CT_0013.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators',
  '../data/raw/colloquial/5CT_0014.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators',
]
```

### 하나의 파일을 list of Sentence 형식으로 로딩하기

세종 말뭉치의 구어 데이터와 문어 데이터는 포멧이 다릅니다. 하지만 세종 말뭉치 파일의 이름을 변경하지 않았다면 `load_a_sejong_file` 함수는 말뭉치 종류에 관계없이 이를 list of `Sentence` 형태로 읽어옵니다. 세종 말뭉치에는 형태소의 기록 형식이 지켜지지 않거나 빈 어절과 같은 오류들이 존재합니다. load_a_file 함수는 로딩 시 Sentence 로 변환하지 못한 오류의 개수를 `n_errors` 로 return 합니다.

```python
from refactoring_package import load_a_sejong_file

sents, n_errors = load_a_file(paths[0])
```

`Sentence` 는 한 문장을 (어절, 형태소열) 의 리스트 단위로 저장한 클래스입니다. 한 문장은 어절 단위로 이들을 구성하는 형태소를 ` + ` 로 나누어 표시합니다.

```python
print(sents[0])
```

```
세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
의상	의상/NNG
디자이너	디자이너/NNG
엠마누엘	엠마누엘/NNP
웅가로가	웅가로/NNP + 가/JKS
실내	실내/NNG
장식용	장식/NNG + 용/XSN
직물	직물/NNG
디자이너로	디자이너/NNG + 로/JKB
나섰다.	나서/VV + 었/EP + 다/EF + ./SF
```

Sentence 는 slicing 과 iteration 이 가능합니다.

```python
print(sents[0][0]) # ('프랑스의', [프랑스/NNP, 의/JKG])
```

```python
for eojeol, morphtags in sents[0]:
    print('{} has {} morphemes'.format(eojeol, len(morphtags)))
```

```
프랑스의 has 2 morphemes
세계적인 has 4 morphemes
의상 has 1 morphemes
디자이너 has 1 morphemes
엠마누엘 has 1 morphemes
웅가로가 has 2 morphemes
실내 has 1 morphemes
장식용 has 2 morphemes
직물 has 1 morphemes
디자이너로 has 2 morphemes
나섰다. has 4 morphemes
```

Slicing 한 sentence 는 (eojeol, list of MorphTag) 형식입니다. `MorphTag` 는 namedtuple 로 각 형태소의 글자와 품사를 각각 `morph` 와 `tag` 로 지니고 있습니다.

```python
eojeol, morphtags = sents[0][0]

print(morphtags[0].morph) # 프랑스
print(morphtags[0].tag) # NNP
```

### 하나 혹은 여러 개의 파일을 Sentences 형식으로 로딩하기

때로는 형태소 빈도수 계산처럼 문장 단위로 작업을 수행할 때도 있습니다. 이때는 모든 문장을 읽어둘 필요가 없기 때문에 `Sentences` 를 이용할 수 있습니다. Sentences 에는 하나의 파일 혹은 여러 개의 파일 리스트를 입력할 수 있습니다.

```python
from sejong_corpus_cleaner import Sentences

sents = Sentences(paths)
sents = Sentences(paths[0], verbose=False)
```

위의 디렉토리 구조를 지킨 상태에서 **모든 세종 말뭉치 파일**을 이용하려면 paths 를 입력하지 않아도 됩니다.

```python
sents = Sentences()
```

Sentences 는 generator of Sentence 형식이기 때문에 iteration 은 지원하지만 slicing 은 지원하지 않습니다. 그러나 `__len__` 은 지원합니다.

```python
len(sents) # 1127
```

`verbose` 를 True 로 설정하면 iteration 과정을 출력합니다. 기본값은 True 입니다.

```python
sents = Sentences(paths, verbose=True)
for sent in sents:
    # do something
```

```
Iterating 11458 sents with 11 errors from 7 / 10 files
```

테스트 등의 이유로 샘플 문장만 살펴볼 때에는 `num_sents` 를 이용합니다. 최대로 읽을 문장의 개수를 설정하면 더 이상 iteration 하지 않습니다. 기본값은 -1 로, 모든 문장을 yield 합니다.

```python
sents = [sent for sent in Sentences(paths, num_sents=100)]
len(sents) # 100
```

### 세종 말뭉치를 (어절, 형태소열) 형식으로 저장하기

세종 말뭉치의 원 파일에는 각 어절과 형태소 외에도 여러 메타 정보가 포함되어 있습니다. 하지만 모델 학습에 필요한 정보는 주로 아래와 같은 각 어절과 그에 해당하는 형태소열입니다.

```
프랑스의	프랑스/NNP + 의/JKG
세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
의상	의상/NNG
...
```

Sentences 형식으로 읽어들인 세종말뭉치를 `write_sentences` 함수를 이용하여 기록하면 위에 출력된 형식으로 말뭉치가 생성됩니다.

```python
from sejong_corpus_cleaner import write_sentences

write_sentences(sents, 'sejong_corpus.txt')
```

### 정제된 데이터를 읽어오기

세종 말뭉치의 원 파일이 아닌, 위의 과정을 통하여 정제된 파일은 `load_a_sentences_file` 을 이용하여 list of Sentence 로 읽을 수 있습니다.

```python
from sejong_corpus_cleaner import load_a_sentences_file

sents = load_a_sentences_file('sejong_corpus.txt')
```

혹은 Sentences 를 이용할 수도 있습니다. 이때는 generator of Sentence 형식입니다.

```python
sents = Sentences('sejong_corpus.txt', processed=True)
```

### 형태소 품사 체계 단순화

세종 말뭉치는 43 개의 형태소 품사로 구성된 품사 체계를 이용합니다. 이를 한국어의 5 언 9 품사의 품사 체계로 단순화 하였습니다. 단, 용언에 해당하는 동사 (Verb) 와 형용사 (Adjective) 는 용언의 어간 (stem) 에 해당합니다. 용언의 어미 (Eomi) 는 5언 9 품사 체계에 포함되지 않는 형태소이지만, 이 역시 따로 품사로 남겨뒀습니다.

| Simplified tag | Sejong corpus tags |
| --- | --- |
| Noun (명사) | NNB, NNG, NNP, XR, XSN |
| Numeral (수사) | NR |
| Pronoun (대명사) | NP |
| Determiner (관형사) | MM, XPN |
| Adverb (부사) | MAG, MAJ |
| Josa (조사) | JC, JKB, JKC, JKG, JKO, JKQ, JKS, JKV, JX |
| Exclamation (감탄사) | IC |
| Adjective (형용사 어근, 형태소) | VA, VCN, VCP, XSA |
| Verb (동사 어근, 형태소) | VV, VX, XSV |
| Eomi (어미, 형태소) | EC, EF, EP, ETM, ETN |
| Unk (인식불능) | NA |
| Symbol (기호) | SE, SF, SH, SL, SN, SO, SP, SS, SW |

```python
from sejong_corpus_cleaner import to_simple_tag

for tag in 'NNB NNG NNP XR XSN NR EC EF JC JKB SH NNNG'.split():
    print('{} -> {}'.format(tag, to_simple_tag(tag)))
```

```
NNB -> Noun
NNG -> Noun
NNP -> Noun
XR -> Noun
XSN -> Noun
NR -> Numeral
EC -> Eomi
EF -> Eomi
JC -> Josa
JKB -> Josa
SH -> Symbol
NNNG -> Unk
```

한 어절을 구성하는 형태소들을 단순한 형태의 품사로 변경하기 위해서는 `to_simple_morphtags` 를 이용합니다.

```python
from sejong_corpus_cleaner import to_simple_morphtags

for eojeol, morphtags in sents[0]:
    simple_morphtags = to_simple_morphtags(morphtags)
    print('{} = {} -> {}'.format(eojeol, morphtags, simple_morphtags))
```

```
프랑스의 = [프랑스/NNP, 의/JKG]  -> [('프랑스', 'Noun'), ('의', 'Josa')]
세계적인 = [세계/NNG, 적/XSN, 이/VCP, ㄴ/ETM]  -> [('세계', 'Noun'), ('적', 'Noun'), ('이', 'Adjective'), ('ㄴ', 'Eomi')]
의상 = [의상/NNG]  -> [('의상', 'Noun')]
디자이너 = [디자이너/NNG]  -> [('디자이너', 'Noun')]
...
```

### 어절 내 여러 개의 단일 형태소를 하나의 복합형태소로 축약한 L-R corpus

세종 말뭉치는 어절 '세계적인'을 다음의 형태소로 구성된 것으로 태깅하였습니다.

```python
print(sents[0][1])
# ('세계적인', [세계/NNG, 적/XSN, 이/VCP, ㄴ/ETM])
```

그러나 어절을 의미를 지니는 복합형태소 부분 (L) 과 문법 기능을 하는 복합형태소 부분 (R) 로 구분한다면 다음과 같이 단순화 할 수 있습니다. L-R 구조에 대한 내용은 [soynlp github](https://github.com/lovit/soynlp) 이나 [lovit blogs](https://lovit.github.io) 의 [포스트](https://lovit.github.io/nlp/2018/04/09/cohesion_ltokenizer/) 를 참고하세요.

```
세계적인 = '세계적/Noun' + '인/Adjective'
```

그런데 '세계적인' 은 세 가지 타입으로 정리될 수 있습니다. 첫째는 VCP 이후를 하나의 형용사로 고려하는 것입니다. 이때의 형용사는 원형이 아닌 표현형이 됩니다. 이를 type 1 이라 합니다.

```
세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM  ->  세계적/Noun + 인/Adjective
```

둘째는 명사와 VCP 을 합쳐서 형용사화 하는 것입니다. 이를 type 2 이라 합니다.

```
세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM  ->  세계적이/Adjective + ㄴ/Eomi
```

셋째는 VCP 이후를 새로운 어절의 용언으로 고려하여 이를 L + [R] 로 분해하는 것입니다. 한국어 형태소 중 명사를 형용사나 동사로 전성하는 어미들은 각각 용언의 어간이기도 합니다 (-되, -이, -하 등). 이를 type 3 이라 합니다.

```
세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM  ->  ["세계적/Noun", "이/Adjective + ㄴ/Eomi"]
```

`make_lr_corpus` 함수는 세종 말뭉치의 품사 체계를 따르는 Sentences 를 L+[R] 형식의 말뭉치로 변환합니다. 각 type 별로 세종 말뭉치를 변환하기 위해서는 make_lr_corpus 에 옵션을 다르게 설정해야 합니다.

```
sents_lr_format = make_lr_corpus(sents)
```

아래의 세종 말뭉치의 한 문장을 각 타입별로 변형하면 아래와 같습니다.

```python
sents = [sent for sent in sents]
sents[0]
```

```
프랑스의	프랑스/NNP + 의/JKG
세계적인	세계/NNG + 적/XSN + 이/VCP + ㄴ/ETM
의상	의상/NNG
디자이너	디자이너/NNG
엠마누엘	엠마누엘/NNP
웅가로가	웅가로/NNP + 가/JKS
실내	실내/NNG
장식용	장식/NNG + 용/XSN
직물	직물/NNG
디자이너로	디자이너/NNG + 로/JKB
나섰다.	나서/VV + 었/EP + 다/EF + ./SF
```

기본 설정은 `type 1` 입니다. 말뭉치 형태를 변형하며 발생하는 오류의 개수가 출력됩니다.

```python
sent_lr = make_lr_corpus(sents[:10], noun_xsv_as_verb=False)[0]
print(sent_lr)
```

```
Transform Sejong corpus to L-R format with 0 exceptions from 10 sents

프랑스의	프랑스/Noun + 의/Josa
세계적인	세계적/Noun + 인/Adjective
의상	의상/Noun
디자이너	디자이너/Noun
엠마누엘	엠마누엘/Noun
웅가로가	웅가로/Noun + 가/Josa
실내	실내/Noun
장식용	장식용/Noun
직물	직물/Noun
디자이너로	디자이너/Noun + 로/Josa
나섰다	나서/Verb + 었다/Eomi
```

`type 2` 는 `noun_xsv_as_verb` 를 True 로 설정합니다.

```python
make_lr_corpus(sents[:10], noun_xsv_as_verb=True)[0]
```

```
프랑스의	프랑스/Noun + 의/Josa
세계적인	세계적이/Adjective + ㄴ/Eomi
의상	의상/Noun
디자이너	디자이너/Noun
엠마누엘	엠마누엘/Noun
웅가로가	웅가로/Noun + 가/Josa
실내	실내/Noun
장식용	장식용/Noun
직물	직물/Noun
디자이너로	디자이너/Noun + 로/Josa
나섰다	나서/Verb + 었다/Eomi
```

`type 3` 는 `xsv_as_root` 를 True 로 설정합니다.

```python
make_lr_corpus(sents[:10], xsv_as_root=True)[0]
```

```
프랑스의	프랑스/Noun + 의/Josa
세계적	세계적/Noun
인	이/Adjective + ㄴ/Eomi
의상	의상/Noun
디자이너	디자이너/Noun
엠마누엘	엠마누엘/Noun
웅가로가	웅가로/Noun + 가/Josa
실내	실내/Noun
장식용	장식용/Noun
직물	직물/Noun
디자이너로	디자이너/Noun + 로/Josa
나섰다	나서/Verb + 었다/Eomi
```

문장 단위로 말뭉치를 변형하며 곧바로 파일에 기록하기 위해서는 `filepath` 에 파일 주소를 입력합니다. 이때는 return 값이 없습니다.

```python
make_lr_corpus(sents, filepath='lr_corpus_type1.txt')
make_lr_corpus(sents, noun_xsv_as_verb=True, filepath='lr_corpus_type2.txt')
make_lr_corpus(sents, xsv_as_root=True, filepath='lr_corpus_type3.txt')
```

생성된 L+[R] 형식의 말뭉치는 Sentences 를 이용하여 로딩할 수 있습니다.

```
corpus_type1 = Sentences('lr_corpus_type1.txt', processed=True)
```

### 어절, 형태소열의 빈도수 계산

(어절, 형태소열) 쌍 혹은 형태소들의 빈도수를 계산하기 위하여 `make_counter` 를 이용할 수 있습니다. {key:count} 형식의 dict 가 return 됩니다.

```python
from sejong_corpus_cleaner import make_counter

counter = make_counter(sents_type1)
sorted(counter.items(), key=lambda x:-x[1])[:5]
```

```
[(('등', (등/Noun,)), 20),
 (('있다', (있/Verb, 다/Eomi)), 19),
 (('있는', (있/Verb, 는/Eomi)), 16),
 (('수', (수/Noun,)), 10),
 (('많이', (많이/Adverb,)), 8)]
```

(어절, 형태소열) 쌍이 아닌 형태소들의 빈도수만 계산하기 위해서는 `eojeol_morpheme_pair` 를 False 로 설정합니다.

```python
counter = make_counter(sents_type1, eojeol_morpheme_pair=False)
sorted(counter.items(), key=lambda x:-x[1])[:5]
```

```
[(이/Josa, 67), (의/Josa, 62), (는/Eomi, 60), (을/Josa, 57), (은/Josa, 51)]
```

세종 말뭉치의 품사 체계를 따르는 Sentences 의 경우, 곧바로 L+[R] 형식으로 변형이 가능하며 각 type 별 옵션도 동일하게 입력할 수 있습니다.

```python
counter = make_counter(sents, convert_lr=True)
counter = make_counter(sents, convert_lr=True, xsv_as_root=True)
```

## 데이터 정제 오류율

세종 말뭉치는 479 개의 파일에 1,021,527 개의 문장이 포함되어 있습니다.

| 작업 | 입력 데이터 크기 | 고유 오류 개수 (빈도수 기준 비율) | 최종 데이터 숫자 |
| --- | --- | --- | --- |
| 원 파일에서 Sentence 형식으로 로딩 | 1,054,912 문장 | 33,385 문장 (3.16 %) | 1,021,527 문장 |
| 세종 말뭉치 문장을 type 1 형식으로 변형 | 1,021,527 문장 | 5,452 문장 (0.210 %) | 1,016,075 문장 |
| 세종 말뭉치 문장을 type 2 형식으로 변형 | 1,021,527 문장 | 6,560 문장 (0.231 %) | 1,014,967 문장 |
| 세종 말뭉치 문장을 type 3 형식으로 변형 | 1,021,527 문장 | 10,126 문장 (0.264 %) | 1,011,401 문장 |
| 세종 말뭉치 어절을 type 1 형식으로 변형 | 1,601,367 (어절, 형태소) 쌍 | 3,330 쌍 (0.051 %) | 1,276,224 쌍 |
| 세종 말뭉치 어절을 type 2 형식으로 변형 | 1,601,367 (어절, 형태소) 쌍 | 3,463 쌍 (0.062 %) | 1,274,358 쌍 |
| 세종 말뭉치 어절을 type 3 형식으로 변형 | 1,601,367 (어절, 형태소) 쌍 | 5,265 쌍 (0.097 %) | 1,049,457 쌍 |


## 코드 내 주요 변수명

| Variable name | meaning |
| --- | --- |
| eojeol | str 로 표현된 어절 |
| morph | str 로 표현된 형태소 혹은 단어 |
| tag | str 로 표현된 품사 |
| morphtag | (morph, tag) |
| morphtags | list of (morph, tag) |
| sentence (or sent, for short) | list of (eojeol, morphtags) |


## Requirements

- beautifulsoup4 >= 4.6.0
- pandas >= 0.23.4
- lxml >= 3.7.0
