## Rules

1. `loader.load_from_raw` 를 실행할 때 해당 파일에서 오류가 있는 문장을 미리 제거한다.
1. `transform` 함수에는 (output file path, tagset) 을 입력하도록 한다. Tagset 은 원형, LR type 1, LR type 2, 사용자 지정, 총 네 가지를 제공한다.
1. Return type 을 정의하여 해당 형식으로 return 한다.
1. output file path 를 입력하면 text 형식으로 저장한다.

## Terms

- eojeol : str 로 표현된 어절
- morph : str 로 표현된 형태소 혹은 단어
- tag : str 로 표현된 품사
- morphtag : (morph, tag)
- morphtags : list of (morph, tag)
- sentence (or sent, for short) : list of (eojeol, morphtags)
