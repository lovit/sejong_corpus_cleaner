import sys
sys.path.insert(0, '../')
import sejong_corpus_cleaner

import traceback
from sejong_corpus_cleaner.simple_tag import to_simple_tag
from sejong_corpus_cleaner.loader import MorphTag
from sejong_corpus_cleaner.lr import to_lr
from sejong_corpus_cleaner.utils import check_lr_transformation


testset = [
    ('다해', [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']], False, False),
    ('통해서', [['통하', 'VV'], ['ㅕ서', 'EC']], False, False),
    ('느꼈으니', [['느끼', 'VV'], ['었', 'EP'], ['으니', 'EC']], False, False),
    ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ㄴ', 'ETM']], False, False),
    ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ㄴ', 'ETM']], True, False),
    ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ㄴ', 'ETM']], False, True),
    ('반가우면서도', [['반갑', 'VA'], ['면서', 'EC'], ['도', 'JX']], False, False),
    ('거셨을', [('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')], False, False),
    ('훌륭한', [('훌륭', 'XR'), ('하', 'XSA'), ('ㄴ', 'ETM')], False, False),
    ('훌륭한', [('훌륭', 'XR'), ('하', 'XSA'), ('ㄴ', 'ETM')], True, False),
    ('훌륭한', [('훌륭', 'XR'), ('하', 'XSA'), ('ㄴ', 'ETM')], False, True),
    ('생각했어요', [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')], False, False),
    ('생각했어요', [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')], True, False),
    ('생각했어요', [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')], False, True),
    ('생각했어요.', [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF'), ('.', 'SF')], True, True),
    ('난', [('나', 'NNG'), ('ㄴ', 'JX')], False, False),
    ('제2의', [('제', 'XPN'), ('2', 'SN'), ('의', 'JKG')], False, False),
    ('2의', [('2', 'SN'), ('의', 'JKG')], False, False),
    ('하나를', [('하나', 'NR'), ('를', 'JKO')], False, False),
    ('하난', [('하나', 'NR'), ('ㄴ', 'JKO')], False, False),
    ('또다른', [('또', 'MAJ'), ('다른', 'MM')], False, False),
    ('6.25', [('6', 'SN'), ('.', 'SF'), ('25', 'SN')], False, False),
    ('6.25의', [('6', 'SN'), ('.', 'SF'), ('25', 'SN'), ('의', 'JX')], False, False),
    ('6,', [('6', 'SN'), (',', 'SF')], False, False),
    ('IBM에서는', [('IBM', 'SL'), ('에서', 'JKB'), ('는', 'JX')], False, False),
    ('는', [('', 'NNP'), ('는', 'JX'), (',', 'SP')], False, False),
    ('지는', [('지', 'EC'), ('는', 'JX')], False, False),
    ('에는', [('에', 'JKB'), ('는', 'JX')], False, False),
    ('왜냐,', [('왜', 'MAG'), ('냐', 'EF'), (',', 'SP')], False, False),
    ('진짜야?', [('진짜', 'MAG'), ('야', 'EF'), ('?', 'SF')], False, False),
    ('야라는', [('야','IC'), ('라는','ETM')], False, False),
    ('야라니?', [('야','IC'), ('라니','EF'), ('?','SF')], False, False),
    ('여보셔요!"', [('여보','IC'), ('시','EP'), ('어요','EF'), ('!','SF'), ('"','SS')], False, False),
    ('아이오아이노래는', [('아이오아이', 'NNG'), ("노래", "NNG"), ('는', 'JX')], False, False),
    ('지금도', [('지금', 'MAG'), ('도', 'JX')], False, False),
    ('XX를', [('XX', 'UNC'), ('를', 'JKO')], False, False),
    ('그래요', [('그래', 'IC'), ('요', 'JX')], False, False),
    ('했어요', [('하', 'VV'), ('았', 'EP'), ('어요', 'EF')], False, False),
    ('했어요', [('하', 'VV'), ('았', 'EP'), ('어요', 'EF')], True, False),
    ('했어요', [('하', 'VV'), ('았', 'EP'), ('어요', 'EF')], False, True),
    ('다해', [('다', 'MAG'), ('하', 'VV'), ('아', 'EC')], False, False),
    ('통해서', [('통하', 'VV'), ('ㅕ서', 'EC')], False, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], False, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], True, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], False, True),
    ('느꼈으니', [('느끼', 'VV'), ('었', 'EP'), ('으니', 'EC')], False, False),
    ('거셨을', [('걸', 'VV'), ('시', 'EP'), ('었', 'EP'), ('을', 'ETM')], False, False),
    ('반가우면서도', [('반갑', 'VA'), ('면서', 'EC'), ('도', 'JX')], False, False),
    ('노랜', [('노래', 'NNG'), ('ㄴ', 'JX')], False, False),
    ('통해서', [('통하', 'VV'), ('ㅏ서', 'EC')], False, False),
    ('봤는데,', [('보', 'VV'), ('ㅏㅆ', 'EP'), ('는데', 'EC'), (',', 'SP')], False, False),
    ('통해서', [('통하', 'VV'), ('ㅕ서', 'EC')], False, False),
    ('돼요,', [('되', 'VV'), ('ㅓ요', 'EF'), (',', 'SP')], False, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], False, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], True, False),
    ('예외적인', [('예외', 'NNG'), ('적', 'XSN'), ('이', 'VCP'), ('ㄴ', 'ETM')], False, True),
    ('지금이라면은,', [('지금', 'MAG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], False, False),
    ('지금이라면은,', [('지금', 'MAG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], True, False),
    ('지금이라면은,', [('지금', 'MAG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], False, True),
    ('지금이라면은,', [('지금', 'NNG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], False, False),
    ('지금이라면은,', [('지금', 'NNG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], True, False),
    ('지금이라면은,', [('지금', 'NNG'), ('이', 'VCP'), ('라면은', 'EC'), (',', 'SP')], False, True),
    ('지금도,', [('지금', 'MAG'), ('도', 'JX'), (',', 'SP')], False, False),
    ('일년', [('일', 'NR'), ('년', 'NNB')], False, False),
    ('보내', [('보내', 'VV'), ('ㅓ', 'EC')], False, False),
    ('따라', [('따르', 'VV'), ('ㅏ', 'EC')], False, False),
    ('했어요', [('하', 'VV'), ('았', 'EP'), ('어요', 'EF')], False, False),
    ('엽기라는', [('엽기', 'NNG'), ('(이)', 'VCP'), ('라는', 'ETM')], False, False),
    ('엽기라는', [('엽기', 'NNG'), ('(이)', 'VCP'), ('라는', 'ETM')], True, False),
    ('엽기라는', [('엽기', 'NNG'), ('(이)', 'VCP'), ('라는', 'ETM')], False, True),
    ('알려진', [('알리', 'VV'), ('ㅓ', 'EC'), ('지', 'VX'), ('ㄴ', 'ETM')], False, False),
    ('알려진', [('알리', 'VV'), ('ㅓ', 'EC'), ('지', 'VX'), ('ㄴ', 'ETM')], True, False),
    ('알려진', [('알리', 'VV'), ('ㅓ', 'EC'), ('지', 'VX'), ('ㄴ', 'ETM')], False, True),
    ('잡혀', [('잡히', 'VV'), ('ㅓ', 'EC')], False, False),
    ('틀려.', [('틀리', 'VA'), ('ㅓ', 'EF'), ('.', 'SF')], False, False),
    ('나눠져', [('나누', 'VV'), ('ㅓ', 'EC'), ('지', 'VX'), ('ㅓ', 'EC')], False, False),
    ('걸로', [('거', 'NNB'), ('ㄹ로', 'JKB')], False, False),
    ('XX를', [('XX', 'UNC'), ('를', 'JKO')], False, False),
    ('그래요?', [('그래', 'IC'), ('요', 'JX'), ('?', 'SF')], False, False),
    ('진짜야?', [('진짜', 'MAG'), ('(이)', 'VCP'), ('야', 'EF'), ('?', 'SF')], False, False),
    ('오고', [('들어오', 'VV'), ('고', 'EC')], False, False),
    ('어쩌구', [('어찌', 'MAG'), ('하', 'XSV'), ('구', 'EC')], False, False),
    ('어쩌구', [('어찌', 'MAG'), ('하', 'XSV'), ('구', 'EC')], True, False),
    ('어쩌구', [('어찌', 'MAG'), ('하', 'XSV'), ('구', 'EC')], False, True),
    ('대한', [('대하', 'VV'), ('ㄴ', 'ETM')], False, False),
    ('맞이해', [('맞이하', 'VV'), ('여', 'EC')], False, False),
    ('캡까지는', [('캡', 'XPN'), ('까지', 'JX'), ('는', 'JX')], False, False),
    ('못지', [('못', 'MAG'), ('하', 'XSA'), ('지', 'EC')], False, False),
    ('못지', [('못', 'MAG'), ('하', 'XSA'), ('지', 'EC')], True, False),
    ('못지', [('못', 'MAG'), ('하', 'XSA'), ('지', 'EC')], False, True),
    ('다해', [('다', 'MAG'), ('하', 'VV'), ('아', 'EC')], False, False),
    ('다해', [('다', 'MAG'), ('하', 'VV'), ('아', 'EC')], True, False),
    ('다해', [('다', 'MAG'), ('하', 'VV'), ('아', 'EC')], False, True),
    ('됨직한', [('되', 'VV'), ('ㅁ직', 'EC'), ('하', 'XSA'), ('ㄴ', 'ETM')], False, False),
    ('됨직한', [('되', 'VV'), ('ㅁ직', 'EC'), ('하', 'XSA'), ('ㄴ', 'ETM')], True, False),
    ('됨직한', [('되', 'VV'), ('ㅁ직', 'EC'), ('하', 'XSA'), ('ㄴ', 'ETM')], False, True),
    ('느낀다"고', [('느끼', 'VV'), ('ㄴ다', 'EC'), ('"', 'SS'), ('고', 'JKQ')], False, False),
    ('세워져', [('세우', 'VV'), ('어', 'EC'), ('지', 'VX'), ('어', 'EC')], False, False),
    ('세워진', [('세우', 'VV'), ('어', 'EC'), ('지', 'VX'), ('ㄴ', 'EC')], False, False),
    ('세워', [('세우', 'VV'), ('어', 'EC')], False, False),
    ('세웠다.', [('세우', 'VV'), ('어', 'EC'), ('ㅆ다', 'EF'), ('.', 'SF')], False, False),
    ('보여', [('보이', 'VV'), ('어', 'EC')], False, False),
    ('있어서도', [('있', 'VV'), ('어서', 'EC'), ('도', 'JX')], False, False),
    ('밝혀져', [('밝히','VV'), ('어','EC'), ('지','VX'), ('어','EC')], False, False),
    ('뭡니까.', [('무엇','NP'), ('이','VCP'), ('ㅂ니까','EF'), ('.','SF')], False, False),
    ('뭡니까.', [('뭐','NP'), ('이','VCP'), ('ㅂ니까','EF'), ('.','SF')], False, False),
    ('정해져', [('정하','VV'), ('아','EC'), ('지','VX'), ('어','EC')], False, False),
    ('짜여져', [('짜이','VV'), ('어','EC'), ('지','VX'), ('어','EC')], False, False),
    ('스쳐갔다.', [('스치','VV'), ('어','EC'), ('가','VX'), ('았','EP'), ('다','EF'), ('.','SF')], False, False),
    ('사는', [('살', 'VV'), ('는', 'ETM')], False, False),
    ('그걸', [('그것', 'NP'), ('ㄹ', 'JKO')], False, False),
    ('그건', [('그것', 'NP'), ('ㄴ', 'JX')], False, False),
    ('ㄱ행을', [('ㄱ행', 'NNG'), ('을', 'JKO')], False, False),
    ('퍼질고', [('퍼지르', 'VV'), ('고', 'EC')], False, False),
    ('버려야겠다.', [('버리', 'VX'), ('어야', 'EC'), ('하', 'VX'), ('겠', 'EP'), ('다', 'EF'), ('.', 'SF')], False, False), 
    ('줘야겠다.', [('주', 'VV'), ('어야', 'EC'), ('하', 'VX'), ('겠', 'EP'), ('다', 'EF'), ('.', 'SF')], False, False),
    ('어째서', [('어찌', 'MAG'), ('하', 'XSV'), ('아서', 'EC')], False, False),
    ('‘양혜련’과', [("'", 'SS'), ('양혜련', 'NNP'), ("'", 'SS'), ('과', 'JC')], False, False),
    ('당키나', [('당하', 'VA'), ('기', 'ETN'), ('나', 'JX')], False, False),
    ('당치도', [('당하', 'VA'), ('지', 'EC'), ('도', 'JX')], False, False),
    ('제것도', [('저', 'NP'), ('의', 'JKG'), ('것', 'NNB'), ('도', 'JX')], False, False),
    ('어쨌단', [('어찌', 'MAG'), ('하', 'XSV'), ('았', 'EP'), ('단', 'ETM')], False, False),
    ('어쩔래!', [('어찌', 'MAG'), ('하', 'XSV'), ('ㄹ래', 'EF'), ('!', 'SF'), ('', 'SS')], False, False),
    ('이뤄졌는지', [('이루어지', 'VV'), ('었', 'EP'), ('는지', 'EC')], False, False),
    ('내것으로', [('나', 'NP'), ('의', 'JKG'), ('것', 'NNB'), ('으로', 'JKB')], False, False),
    ('제말이', [('저', 'NP'), ('의', 'JKG'), ('말', 'NNG'), ('이', 'JKS')], False, False),
    ('편치', [('편ㅎ', 'VA'), ('지', 'EC')], False, False),
    ('문화다.', [('문화', 'NNG'), ('이', 'VCP'), ('다', 'EF'), ('.', 'SF')], True, False),
    ('이데올로기다.', [('이데올로기', 'NNG'), ('이', 'VCP'), ('다', 'EF')], False, False),
    ('가난한', [('', 'SS'), ('가난', 'NNG'), ('하', 'XSA'), ('ㄴ', 'ETM')], False, False),
    ('"물론이죠."', [('"', 'SS'), ('물론', 'NNG'), ('이', 'VCP'), ('죠', 'EF'), ('.', 'SF'), ('"', 'SS')], False, False),
    ('건지도', [('것', 'NNB'), ('이', 'VCP'), ('ㄴ지', 'EC'), ('도', 'JX')], False, False),
    ('용케', [('용', 'XR'), ('하', 'XSA'), ('게', 'EC')], False, False),
    ('용케', [('용하', 'VA'), ('게', 'EC')], False, False),
    ('생각케', [('생각', 'NNG'), ('하', 'XSV'), ('게', 'EC')], False, False),
    ('사용토록', [('사용', 'NNG'), ('하', 'XSV'), ('도록', 'EC')], False, False),
    ('분석해보자.', [('분석', 'NNG'), ('하', 'XSV'), ('아', 'EC'), ('보', 'VX'), ('자', 'EF'), ('.', 'SF')], False, False),
    ('텐데……', [('터', 'NNB'), ('이', 'VCP'), ('ㄴ데', 'EC'), ('…', 'SE'), ('…', 'SE'), ('', 'SS')], False, False),
    ('영원토록', [('영원', 'NNG'), ('하', 'XSA'), ('도록', 'EC')], False, False),
    ('될텐데', [('되', 'VV'), ('ㄹ', 'ETM'), ('터', 'NNB'), ('이', 'VCP'), ('ㄴ데', 'EC')], False, False),
    ('이뤄진', [('이루어지', 'VV'), ('ㄴ', 'ETM')], False, False),
    ('이룬', [('이루', 'VV'), ('ㄴ', 'ETM')], False, False),
    ('뭘로', [('무엇', 'NP'), ('으로', 'JKB')], False, False),
    ('뭘하는', [('무엇', 'NP'), ('ㄹ', 'JKO'), ('하', 'VV'), ('는', 'ETM')], False, False),
    ('별로야.', [('별로', 'MAG'), ('이', 'VCP'), ('야', 'EF'), ('.', 'SF')], False, False),
    ('함께라면', [('함께', 'MAG'), ('이', 'VCP'), ('라면', 'EC')], False, False),
    ('없어서라고', [('없', 'VA'), ('어서', 'EC'), ('이', 'VCP'), ('라고', 'EC')], False, False),
    ('이뤄진다고', [('이루어지', 'VV'), ('ㄴ다고', 'EC')], False, False),
    ('이뤄진다면', [('이루어지', 'VV'), ('ㄴ다면', 'EC')], False, False),
    ('이뤄져야', [('이루어지', 'VV'), ('어야', 'EC')], False, False),
    ('이뤄져', [('이루어지', 'VV'), ('어', 'EC')], False, False)


]


def pprint_lr(eojeol, morphtags, results, only_result=False):
    def pair_to_strf(e, mts):
        return '{} ({})'.format(e, ' + '.join([str(mt) for mt in mts]))

    def elr_to_strf(e, l, r):
        return '{} ({})'.format(e, l) if r is None else '{} ({} + {})'.format(e, l, r)

    input_strf = pair_to_strf(eojeol, morphtags)
    first_strf = elr_to_strf(*results[0][:3])
    second_strf = '' if len(results) == 1 else elr_to_strf(*results[1][:3])

    flag = check_lr_transformation(*results[0][:3], debug=False)
    flag = '' if flag else '  <--- Failed to convert L-R'
    if second_strf:
        message = '{}\t->\t["{}", "{}"] {}'.format('' if only_result else input_strf, first_strf, second_strf, flag)
    else:
        message = '{}\t->\t["{}"] {}'.format('' if only_result else input_strf, first_strf, flag)
    print(message)

for i_test, (eojeol, morphtags, noun_xsv_as_verb, xsv_as_root) in enumerate(testset):
    if i_test % 5 == 0:
        print()

    try:
        morphtags = [MorphTag(m, t) for m, t in morphtags]
        results = to_lr(eojeol, morphtags, noun_xsv_as_verb=noun_xsv_as_verb, xsv_as_root=xsv_as_root, debug=False)
        pprint_lr(eojeol, morphtags, results, only_result=False)
    except Exception as e:
        print()
        print(traceback.format_exc(), end='\n\n')
        continue
