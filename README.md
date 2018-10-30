# 세종 말뭉치 정제를 위한 utils

국립국어원에서 배포한 세종 말뭉치로부터 학습에 필요한 부분만을 취하기 위한 utils 입니다. 세종 말뭉치 데이터는 재배포가 제한되어 있기 때문에 원 데이터에서부터 필요한 정보를 추출하는 함수를 작성하였습니다.

## Usage

### Directory

README 의 예시 코드는 아래의 폴더 구조를 전제합니다. script 폴더 안에서 작업한 코드 예시 입니다.

    |- sejong_corpus_cleaner # package folder
        |- processed_data
        |- rawtext_loader
        |- simplifier
        |- ...
    |- data # 데이터 폴더
        |- raw
            |- colloquial  # 구어 말뭉치, 200 개 파일
                |- 5CT_0013.txt;
                |- 5CT_0014.txt;
                |- 5CT_0015.txt;
                |- ...
                |- 9CT_0012.txt;
                |- 9CT_0013.txt;
            |- written # 문어 말뭉치, 279 개 파일
                |- BTAA0001.txt;
                |- BTAA0002.txt;
                |- ...
                |- BTJO0446.txt;
                |- BTJO0447.txt;
        |- clean
    |- script #코드 폴더
    |- README.md;

### Check encoding

세종 말뭉치의 파일 인코딩은 utf-16 입니다. 파일의 인코딩을 확인하기 위하여 **check_encoding** 를 이용할 수 있습니다. check_encoding 에는 list of str 형식의 파일 주소들을 입력합니다. 각 파일의 encoding 이 return 됩니다. Ubuntu OS 의 terminal command 인 file 함수를 이용합니다. Window OS 를 지원하지 않습니다.

    from sejong_corpus_cleaner import check_encoding

    check_encoding([
        '../data/raw/colloquial/5CT_0013.txt',
        '../data/raw/colloquial/5CT_0014.txt'
    ])

    ../data/raw/colloquial/5CT_0013.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators
    ../data/raw/colloquial/5CT_0014.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators

### Loading raw texts as eojeol-morphemes

세종 말뭉치의 구어 데이터와 문어 데이터는 포멧이 다릅니다. **load_colloquial_text_as_eojeol_morphtag** 는 구어 데이터를 sentences 형식으로 파싱하는 함수이며, **load_written_text_as_eojeol_morphtag** 는 문어 데이터를 sentences 형식으로 파싱하는 함수입니다. 둘 모두 list of str 의 형식으로 문장을 return 합니다.

    from sejong_corpus_cleaner.rawtext_loader import load_colloquial_text_as_eojeol_morphtag
    from sejong_corpus_cleaner.rawtext_loader import load_written_text_as_eojeol_morphtag

    colloquial = load_colloquial_text_as_eojeol_morphtag('../data/raw/colloquial/5CT_0013.txt')
    written = load_written_text_as_eojeol_morphtag('../data/raw/written/BTAA0001.txt')

list of str 에 포함된 str 은 한 문장이며, 각 어절이 줄바꿈 기호인 '\n' 로 구분되어 있습니다. 각 어절은 '어절\t분석결과' 처럼 탭 (tap) 기호로 구분되어 있습니다.

    print(colloquial[0])

    뭐	뭐/NP
    타고	타/VV + 고/EC
    가?	가/VV + ㅏ/EF + ?/SF

    print(written[0])

    프랑스의	프랑스/NNP + 의/JKG
    세계적인	세계/NNG + 적/XSN + 이/VCP + ᆫ/ETM
    의상	의상/NNG
    디자이너	디자이너/NNG
    엠마누엘	엠마누엘/NNP
    웅가로가	웅가로/NNP + 가/JKS
    실내	실내/NNG
    장식용	장식/NNG + 용/XSN
    직물	직물/NNG
    디자이너로	디자이너/NNG + 로/JKB
    나섰다.	나서/VV + 었/EP + 다/EF + ./SF

**load_texts_as_eojeol_morphtag** 함수는 여러 파일을 읽어 nested list 형식의 문장들을 return 합니다. 각 문장은 list of tuple 형식으로 [(단어, 품사), (단어, 품사), ... ] 형태입니다.  문어와 구어에 따라 is_colloquial 을 True, False 로 설정합니다.

    from glob import glob
    from sejong_corpus_cleaner.rawtext_loader import load_texts_as_eojeol_morphtag

    paths = glob('../data/raw/colloquial/*.txt')
    eojeol_morphtag = load_texts_as_eojeol_morphtag(paths, is_colloquial=True)

    paths = glob('../data/raw/written/*.txt')
    eojeol_morphtag = load_texts_as_eojeol_morphtag(paths, is_colloquial=False)

### 세종 말뭉치의 품사 체계를 이용하는 형태소 분석용 데이터셋 만들기

**load_texts_as_corpus** 함수는 세종 말뭉치의 원 데이터 (raw data) 를 띄어쓰기로 구분된 '형태소/품사'열의 list of str 로 변형합니다. 세종 말뭉치의 구어와 문어 데이터는 loading 함수가 다르기 때문에 데이터의 종류에 따라 is_colloquial 을 True, False 로 설정해야 합니다.

    from sejong_corpus_cleaner.rawtext_loader import load_texts_as_corpus

    paths = ['../data/raw/colloquial/5CT_0013.txt', '../data/raw/colloquial/5CT_0014.txt']
    data = load_texts_as_corpus(paths, is_colloquial= True)

    [('뭐', 'NP'), ('타', 'VV'), ('고', 'EC'), ('가', 'VV'), ('ㅏ', 'EF'), ('?/SF', '')],
     ('지하철', 'NNG'), ('./SF', '')],
     ('기차', 'NNG'), ('?/SF', '')],
     ('아침', 'NNG'), ('에', 'JKB'), ('몇', 'MM'), ('시', 'NNB'), ('에', 'JKB'), ...],
     ...
    ]

    paths = ['../data/raw/written/BTAA0001.txt', '../data/raw/written/BTAA0003.txt']
    data = load_texts_as_corpus(paths, is_colloquial= False)

    [('프랑스', 'NNP'), ('의', 'JKG'), ('세계', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ᆫ', 'ETM'), ('의상', 'NNG'), ('디자이너', 'NNG'), ('엠마누엘', 'NNP'), ...],
     ('웅가로', 'NNP'), ('는', 'JX'), ('침실', 'NNG'), ('과', 'JC'), ('식당', 'NNG'), (',/SP', '('욕실'),', 'NNG'), ('에서', 'JKB'), ('사용', 'NNG'), ...],
     ('목욕', 'NNG'), ('가운', 'NNG'), ('부터', 'JX'), ('탁자보', 'NNG'), (',/SP', '('냅킨'),', 'NNG'), (',/SP', '('앞치마'),', 'NNG'), ('까지', 'JX'), ('그', 'NP'), ...],
     ...
    ]

**load_texts_as_eojeol_morphtag_table** 함수는 세종 말뭉치의 원 데이터 (raw data) 로부터 어절을 구성하는 형태소와 해당 어절의 빈도수를 pandas.DataFrame 의 형태로 제공합니다. 이 역시 구어와 문어 데이터에 따라 is_colloquial 을 다르게 설정해야 합니다.

    from sejong_corpus_cleaner.rawtext_loader import load_texts_as_eojeol_morphtag_table

    paths = ['../data/raw/written/BTAA0001.txt', '../data/raw/written/BTAA0003.txt']
    table = load_texts_as_eojeol_morphtag_table(paths, is_colloquial=False)

table 은 pandas.DataFrame 의 형태로, 아래와 같습니다. Is_compound 는 해당 어절이 두 개 이상의 형태소로 구성되어 있는지를 표시하는 column 이며, 각 형태소는 띄어쓰기로 구분됩니다.

| | Eojeol | morphtags | Count | Is_compound |
| --- | --- | --- |  --- | --- |
| 0 | 등 | 등/NNB | 175 | False |
| 1 | 있다. | 있/VX 다/EF ./SF | 142 | True |
| 2 | 수 | 수/NNB | 135 | False |
| 3 | 있는 | 있/VX 는/ETM | 91 | True |

### 형태소 품사 체계 단순화

세종 말뭉치는 43 개의 형태소 품사로 구성된 품사 체계를 이용합니다. 이를 한국어의 5 언 9 품사의 품사 체계로 단순화 하였습니다. 단, 용언에 해당하는 동사 (Verb) 와 형용사 (Adjective) 는 용언의 어간 (stem) 에 해당합니다. 용언의 어미 (Eomi) 는 5언 9 품사 체계에 포함되지 않는 형태소이지만, 이 역시 따로 품사로 남겨뒀습니다.

| Simplified tag | Sejong corpus tags |
| --- | --- |
| Noun (명사) | NNB, NNG, NNP, XR, XSN |
| Number (수사) | NR |
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

    from sejong_corpus_cleaner.simplify import to_simple_tag_sentence

    sent = [
        ('프랑스', 'NNP'), ('의', 'JKG'), ('세계', 'NNG'), ('적', 'XSN'),
        ('이', 'VCP'), ('ᆫ', 'ETM'), ('의상', 'NNG'), ('디자이너', 'NNG'),
        ('엠마누엘', 'NNP'), ('웅가로', 'NNP'), ('가', 'JKS'), ('실내', 'NNG'),
        ('장식', 'NNG'), ('용', 'XSN'), ('직물', 'NNG'), ('디자이너', 'NNG'),
        ('로', 'JKB'), ('나서', 'VV'), ('었', 'EP'), ('다', 'EF'), ('.', 'SF')
    ]

    to_simple_tag_sentence(sent)

    [('프랑스', 'Noun'), ('의', 'Josa'), ('세계', 'Noun'), ('적', 'Noun'),
     ('이', 'Adjective'), ('ᆫ', 'Eomi'), ('의상', 'Noun'), ('디자이너', 'Noun'),
     ('엠마누엘', 'Noun'), ('웅가로', 'Noun'), ('가', 'Josa'), ('실내', 'Noun'),
     ('장식', 'Noun'), ('용', 'Noun'), ('직물', 'Noun'), ('디자이너', 'Noun'),
     ('로', 'Josa'), ('나서', 'Verb'), ('었', 'Eomi'), ('다', 'Eomi'), ('.', 'Symbol')
    ]

### 어절 내 여러 개의 단일 형태소를 하나의 복합형태소로 축약한 L-R corpus

세종 말뭉치는 어절 '세계적인'을 다음의 형태소로 구성된 것으로 태깅하였습니다.

    세계적인 = [('세계', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ᆫ', 'ETM')])

그러나 어절을 의미를 지니는 복합형태소 부분 (L) 과 문법 기능을 하는 복합형태소 부분 (R) 로 구분한다면 다음과 같이 단순화 할 수 있습니다. L-R 구조에 대한 내용은 [soynlp github](https://github.com/lovit/soynlp) 이나 [lovit blogs](https://lovit.github.io) 의 [포스트](https://lovit.github.io/nlp/2018/04/09/cohesion_ltokenizer/) 를 참고하세요.

    세계적인 = ('세계적', '인', 'Noun', 'Josa')

soynlp 에서 작업하는 단어 추출 기법과 세종 말뭉치를 함께 이용하기 위해서는 이처럼 세종 말뭉치를 L-R 구조로 변환할 수 있어야 합니다. soynlp 에서의 단어 추출은 여러 개의 명사로 이뤄진 복합명사를 단일 명사로 인식합니다. 또한 여러 개의 어미로 구성된 용언의 어미들도 하나의 어미로 인식합니다. 세종 말뭉치를 L-R corpus 로 변환하면 soynlp 에 의하여 확장되는 명사와 어미들을 함께 이용할 수 있습니다.

    '주상 + 복합' 은 '주상복합'
    '갔다면 = 가/동사 + ㅆ다면/어미'

또한 어절에 포함되어 있는 기호를 제거하여 단어만 남겨둘 수 있습니다. 아래는 세종 말뭉치 내 세 개 문장이 L-R corpus 형식으로 변환된 예시입니다.

    ## Sejong corpus
    [('프랑스의', [('프랑스', 'NNP'), ('의', 'JKG')]),
     ('세계적인', [('세계', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ᆫ', 'ETM')]),
     ('의상', [('의상', 'NNG')]),
     ('디자이너', [('디자이너', 'NNG')]),
     ('엠마누엘', [('엠마누엘', 'NNP')]),
     ('웅가로가', [('웅가로', 'NNP'), ('가', 'JKS')]),
     ('실내', [('실내', 'NNG')]),
     ('장식용', [('장식', 'NNG'), ('용', 'XSN')]),
     ('직물', [('직물', 'NNG')]),
     ('디자이너로', [('디자이너', 'NNG'), ('로', 'JKB')]),
     ('나섰다.', [('나서', 'VV'), ('었', 'EP'), ('다', 'EF'), ('.', 'SF')])]

    ## LR corpus
    [('프랑스', '의', 'Noun', 'Josa'),
     ('세계적', '인', 'Noun', 'Josa'),
     ('의상', '', 'Noun', ''),
     ('디자이너', '', 'Noun', ''),
     ('엠마누엘', '', 'Noun', ''),
     ('웅가로', '가', 'Noun', 'Josa'),
     ('실내', '', 'Noun', ''),
     ('장식용', '', 'Noun', ''),
     ('직물', '', 'Noun', ''),
     ('디자이너', '로', 'Noun', 'Josa'),
     ('나서', '었다', 'Verb', 'Eomi')]

    --------------------------------------------------

    ## Sejong corpus
    [('웅가로는', [('웅가로', 'NNP'), ('는', 'JX')]),
     ('침실과', [('침실', 'NNG'), ('과', 'JC')]),
     ('식당,', [('식당', 'NNG'), (',', 'SP')]),
     ('욕실에서', [('욕실', 'NNG'), ('에서', 'JKB')]),
     ('사용하는', [('사용', 'NNG'), ('하', 'XSV'), ('는', 'ETM')]),
     ('갖가지', [('갖가지', 'NNG')]),
     ('직물제품을', [('직물', 'NNG'), ('제품', 'NNG'), ('을', 'JKO')]),
     ('디자인해', [('디자인', 'NNG'), ('하', 'XSV'), ('아', 'EC')]),
     ('최근', [('최근', 'NNG')]),
     ('파리의', [('파리', 'NNP'), ('의', 'JKG')]),
     ('갤러리', [('갤러리', 'NNG')]),
     ('라파예트백화점에서', [('라파예트', 'NNP'), ('백화점', 'NNG'), ('에서', 'JKB')]),
     ("'색의", [("'", 'SS'), ('색', 'NNG'), ('의', 'JKG')]),
     ("컬렉션'이라는", [('컬렉션', 'NNG'), ("'", 'SS'), ('이', 'VCP'), ('라는', 'ETM')]),
     ('이름으로', [('이름', 'NNG'), ('으로', 'JKB')]),
     ('전시회를', [('전시회', 'NNG'), ('를', 'JKO')]),
     ('열었다.', [('열', 'VV'), ('었', 'EP'), ('다', 'EF'), ('.', 'SF')])]

    ## LR corpus
    [('웅가로', '는', 'Noun', 'Josa'),
     ('침실', '과', 'Noun', 'Josa'),
     ('식당', '', 'Noun', ''),
     ('욕실', '에서', 'Noun', 'Josa'),
     ('사용', '하는', 'Noun', 'Josa'),
     ('갖가지', '', 'Noun', ''),
     ('직물제품', '을', 'Noun', 'Josa'),
     ('디자인', '하해', 'Noun', 'Josa'),
     ('최근', '', 'Noun', ''),
     ('파리', '의', 'Noun', 'Josa'),
     ('갤러리', '', 'Noun', ''),
     ('라파예트백화점', '에서', 'Noun', 'Josa'),
     ('색', '의', 'Noun', 'Josa'),
     ('컬렉션', '이라는', 'Noun', 'Josa'),
     ('이름', '으로', 'Noun', 'Josa'),
     ('전시회', '를', 'Noun', 'Josa'),
     ('열', '었다', 'Verb', 'Eomi')]

    --------------------------------------------------

    ## Sejong corpus
    [('목욕가운부터', [('목욕', 'NNG'), ('가운', 'NNG'), ('부터', 'JX')]),
     ('탁자보,', [('탁자보', 'NNG'), (',', 'SP')]),
     ('냅킨,', [('냅킨', 'NNG'), (',', 'SP')]),
     ('앞치마까지', [('앞치마', 'NNG'), ('까지', 'JX')]),
     ('그가', [('그', 'NP'), ('가', 'JKS')]),
     ('디자인한', [('디자인', 'NNG'), ('하', 'XSV'), ('ᆫ', 'ETM')]),
     ('작품들에서', [('작품', 'NNG'), ('들', 'XSN'), ('에서', 'JKB')]),
     ('두드러지는', [('두드러지', 'VV'), ('는', 'ETM')]),
     ('것은', [('것', 'NNB'), ('은', 'JX')]),
     ('색의', [('색', 'NNG'), ('의', 'JKG')]),
     ('조화다.', [('조화', 'NNG'), ('이', 'VCP'), ('다', 'EF'), ('.', 'SF')])]

    ## LR corpus
    [('목욕가운', '부터', 'Noun', 'Josa'),
     ('탁자보', '', 'Noun', ''),
     ('냅킨', '', 'Noun', ''),
     ('앞치마', '까지', 'Noun', 'Josa'),
     ('그', '가', 'Pronoun', 'Josa'),
     ('디자인', '한', 'Noun', 'Josa'),
     ('작품들', '에서', 'Noun', 'Josa'),
     ('두드러지', '는', 'Verb', 'Eomi'),
     ('것', '은', 'Noun', 'Josa'),
     ('색', '의', 'Noun', 'Josa'),
     ('조화', '이다', 'Noun', 'Josa')]

위 변환을 위하여 다음의 함수가 이용됩니다.

    from sejong_corpus_cleaner.simplifier import eojeol_morphtag_to_lr

    eojeol = '나눠져'
    morphtag = [['나누', 'VV'], ['ㅓ', 'EC'], ['지', 'VX'], ['ㅓ', 'EC']]

    print(eojeol_morphtag_to_lr(eojeol, morphtag))
    # ('나눠지', '어', 'Verb', 'Eomi')


어절 내 형태소들을 L-R 구조로 변형할 때, 명사 뒤에 위치하는 동사/형용사 전성 어미인 XSV/XSA 와 긍정/부정 지정사인 VCP/VCN 은 명사와 함께 하나의 L 로 볼 수도 있고, 독립된 L 로 볼 수 도 있습니다. 이는 사용자 패러매터로 조절할 수 있습니다. separate_xsv 의 기본값은 True 입니다. '생각했어요'는 '생각하/Verb + 았어요/Eomi' 로 볼 수도 있으며, '생각/Noun + 하/Verb + 았어요/Eomi' 로 볼 수도 있습니다. L-R 은 한 어절에 L 과 R 의 성분이 있다고 가정하므로 후자의 경우는 '(생각/Noun, L), (하/Verb, L), (았어요/Eomi, R)' 로 표현됩니다.

    eojeol = '생각했어요'
    morphtag = [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')]
    eojeol_morphtag_to_lr(eojeol, morphtag, separate_xsv=True)
    # (('생각', '', 'Noun', ''), ('하', '았어요', 'Verb', 'Eomi'))

    eojeol_morphtag_to_lr(eojeol, morphtag, separate_xsv=False)
    # ('생각하', '았어요', 'Verb', 'Eomi')

하나의 어절이 아닌 문장을 변환할 때는 다음의 함수를 이용합니다. 이때에도 separate_xsv 패러매터를 입력할 수 있습니다. 기본값은 True 입니다.

    from sejong_corpus_cleaner.processed_data import EojeolMorphtagSentence
    from sejong_corpus_cleaner.simplifier import eojeol_morphtags_sentence_to_lr

    ems = EojeolMorphtagSentence('../data/clean/eojeol_morphtag_written.txt')
    for sent in ems:
        sent_ = eojeol_morphtags_sentence_to_lr(sent, separate_xsv=True)

## Requirements

- beautifulsoup4 >= 4.6.0
- pandas >= 0.23.4
- lxml >= 3.7.0
