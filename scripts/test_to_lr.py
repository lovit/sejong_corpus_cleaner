import sys
sys.path.insert(0, '../')

from sejong_corpus_cleaner.simplifier import eojeol_poses_to_lr

def main():
    test_sets = [
        ('봤는데,', [['보', 'VV'], ['ㅏㅆ', 'EP'], ['는데', 'EC'], [',', 'SP']], 'Verb'),
        ('통해서', [['통하', 'VV'], ['ㅕ서', 'EC']], 'Verb'),
        ('돼요,', [['되', 'VV'], ['ㅓ요', 'EF'], [',', 'SP']], 'Verb'),
        ('예외적인', [['예외', 'NNG'], ['적', 'XSN'], ['이', 'VCP'], ['ᆫ', 'ETM']], 'Noun'),
        ('지금이라면은,', [['지금', 'MAG'], ['이', 'VCP'], ['라면은', 'EC'], [',', 'SP']], 'Adjective'),
        ('지금이라면은,', [['지금', 'NNG'], ['이', 'VCP'], ['라면은', 'EC'], [',', 'SP']], 'Noun'),
        ('지금도,', [['지금', 'MAG'], ['도', 'JX'], [',', 'SP']], 'Josa'), 
        ('일년', [['일', 'NR'], ['년', 'NNB']], 'Noun'),
        ('보내', [['보내', 'VV'], ['ㅓ', 'EC']], 'Verb'),
        ('따라', [['따르', 'VV'], ['ㅏ', 'EC']], 'Verb'),
        ('했어요', [['하', 'VV'], ['았', 'EP'], ['어요', 'EF']], 'Verb'),
        ('엽기라는', [['엽기', 'NNG'], ['(이)', 'VCP'], ['라는', 'ETM']], 'Noun'),
        ('알려진', [['알리', 'VV'], ['ㅓ', 'EC'], ['지', 'VX'], ['ㄴ', 'ETM']], 'Verb'),
        ('잡혀', [['잡히', 'VV'], ['ㅓ', 'EC']], 'Verb'),
        ('틀려.', [['틀리', 'VA'], ['ㅓ', 'EF'], ['.', 'SF']], 'Adjective'),
        ('나눠져', [['나누', 'VV'], ['ㅓ', 'EC'], ['지', 'VX'], ['ㅓ', 'EC']], 'Verb'),
        ('걸로', [['거', 'NNB'], ['ㄹ로', 'JKB']], 'Noun'),
        ('XX를', [['XX', 'UNC'], ['를', 'JKO']], 'Unk'),
        ('그래요?', [['그래', 'IC'], ['요', 'JX'], ['?', 'SF']], 'Exclamation'),
        ('진짜야?', [['진짜', 'MAG'], ['(이)', 'VCP'], ['야', 'EF'], ['?', 'SF']], 'Adverb'),
        ('오고', [['들어오', 'VV'], ['고', 'EC']], 'Verb'),
        ('어쩌구', [['어찌', 'MAG'], ['하', 'XSV'], ['구', 'EC']], 'Verb'),
        ('대한', [['대하', 'VV'], ['ᆫ', 'ETM']], 'Verb'),
        ('맞이해', [['맞이하', 'VV'], ['여', 'EC']], 'Verb'),
        ('캡까지는', [['캡', 'XPN'], ['까지', 'JX'], ['는', 'JX']], 'Determiner'),
        ('못지', [['못', 'MAG'], ['하', 'XSA'], ['지', 'EC']], 'Adverb'),
        ('다해', [['다', 'MAG'], ['하', 'VV'], ['아', 'EC']], 'Verb'),
        ('됨직한', [['되', 'VV'], ['ㅁ직', 'EC'], ['하', 'XSA'], ['ㄴ', 'ETM']], 'Adjective'),
        ('느낀다"고', [('느끼', 'VV'), ('ㄴ다', 'EC'), ('"', 'SS'), ('고', 'JKQ')], 'Verb'),
        ('생각했어요', [('생각', 'NNP'), ('하', 'XSV'), ('았', 'EP'), ('어요', 'EF')], ''),
        ('생각하다', [('생각', 'NNP'), ('하', 'XSV'), ('다', 'EF')], '')
    ]

    for eojeol, poses, tag in test_sets:
        result0 = eojeol_poses_to_lr(eojeol, poses, separate_xsv=False)
        result1 = eojeol_poses_to_lr(eojeol, poses)
        if result0 == result1:
            print('{}-> {}\nposes = {}'.format(eojeol, result0[0], poses), end='\n\n')
        else:
            print('{}-> {}, {}\nposes = {}'.format(eojeol, result0[0], result1, poses), end='\n\n')

if __name__ == '__main__':
    main()