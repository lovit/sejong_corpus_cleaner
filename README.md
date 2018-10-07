# 세종 말뭉치 정제를 위한 utils

국립국어원에서 배포한 세종말뭉치로부터 학습에 필요한 부분만을 취하기 위한 utils 입니다.

## Usage

### Check encoding

세종말뭉치의 파일 인코딩은 utf-16 입니다. 파일의 인코딩을 확인하기 위하여 check_encoding 를 이용할 수 있습니다. check_encoding 에는 list of str 형식의 파일 주소들을 입력합니다. 각 파일의 encoding 이 return 됩니다. Ubuntu OS 의 terminal command 인 file 함수를 이용합니다. Window OS 를 지원하지 않습니다.

    check_encoding([
        '../data/raw/spoken/5CT_0013.txt',
        '../data/raw/spoken/5CT_0014.txt'
    ])

    ../data/raw/spoken/5CT_0013.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators
    ../data/raw/spoken/5CT_0014.txt: HTML document, Little-endian UTF-16 Unicode text, with CRLF line terminators

### Loading as sentences

세종말뭉치의 구어 데이터와 문어 데이터는 포멧이 다릅니다. load_spoken_text_as_sentences 는 구어 데이터를 sentences 형식으로 파싱하는 함수이며, load_written_text_as_sentences 는 문어 데이터를 sentences 형식으로 파싱하는 함수입니다. 둘 모두 list of str 의 형식으로 문장을 return 합니다.

    from sejong_corpus_cleaner import load_spoken_text_as_sentences
    from sejong_corpus_cleaner import load_written_text_as_sentences

    spoken = load_spoken_text_as_sentences('../data/raw/spoken/5CT_0013.txt')
    written = load_written_text_as_sentences('../data/raw/written/BTAA0001.txt')

list of str 에 포함된 str 은 한 문장이며, 각 어절이 줄바꿈 기호인 '\n' 로 구분되어 있습니다. 각 어절은 '어절\t분석결과' 처럼 탭 (tap) 기호로 구분되어 있습니다.

    print(spoken[0])

    뭐	뭐/NP
    타고	타/VV+고/EC
    가?	가/VV+ㅏ/EF+?/SF

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

## Requirements

BeautifulSoup >= 4.6.0
