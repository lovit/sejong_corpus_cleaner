import os
import subprocess


def check_encoding(paths):
    """
    Argument
    --------
    paths : str or list of str
        File path

    Returns
    -------
    """
    if isinstance(paths, str):
        paths = [paths]

    # OSX
    if os.environ['_system_name'] == 'OSX':
        encodings = [subprocess.getstatusoutput("file -I %s" % path)[1] for path in list_of_paths]
    # Ubuntu
    else:
        encodings = [subprocess.getstatusoutput("file %s" % path)[1] for path in list_of_paths]
    return encodings

unicode_mapper = {
  'ᆨ': 'ㄱ', # 4520
  'ᆩ': 'ㄲ', # 4521
  'ᆪ': 'ㄳ', # 4522
  'ᆫ': 'ㄴ', # 4523
  'ᆬ': 'ㄵ', # 4524
  'ᆭ': 'ㄶ', # 4525
  'ᆮ': 'ㄷ', # 4526
  'ᆯ': 'ㄹ', # 4527
  'ᆰ': 'ㄺ', # 4528
  'ᆱ': 'ㄻ', # 4529
  'ᆲ': 'ㄼ', # 4530
  'ᆳ': 'ㄽ', # 4531
  'ᆴ': 'ㄾ', # 4532
  'ᆵ': 'ㄿ', # 4533
  'ᆶ': 'ㅀ', # 4534
  'ᆷ': 'ㅁ', # 4535
  'ᆸ': 'ㅂ', # 4536
  'ᆹ': 'ㅄ', # 4537
  'ᆺ': 'ㅅ', # 4538
  'ᆻ': 'ㅆ', # 4539
  'ᆼ': 'ㅇ', # 4540
  'ᆽ': 'ㅈ', # 4541
  'ᆾ': 'ㅊ', # 4542
  'ᆿ': 'ㅋ', # 4543
  'ᇀ': 'ㅌ', # 4544
  'ᇁ': 'ㅍ', # 4545
  'ᇂ': 'ㅎ', # 4546
  'ᄀ': 'ㄱ', # 4352
  'ᄁ': 'ㄲ', # 4353
  'ᄂ': 'ㄴ', # 4354
  'ᄃ': 'ㄷ', # 4355
  'ᄄ': 'ㄸ', # 4356
  'ᄅ': 'ㄹ', # 4357
  'ᄆ': 'ㅁ', # 4358
  'ᄇ': 'ㅂ', # 4359
  'ᄈ': 'ㅃ', # 4360
  'ᄉ': 'ㅅ', # 4361
  'ᄊ': 'ㅆ', # 4362
  'ᄋ': 'ㅇ', # 4363
  'ᄌ': 'ㅈ', # 4364
  'ᄍ': 'ㅉ', # 4365
  'ᄎ': 'ㅊ', # 4366
  'ᄏ': 'ㅋ', # 4367
  'ᄐ': 'ㅌ', # 4368
  'ᄑ': 'ㅍ', # 4369
  'ᄒ': 'ㅎ', # 4370
}

def unicode_character(c):
    return unicode_mapper.get(c, c)

def unicode_sentence(sent):
    return ''.join(unicode_character(c) for c in sent)
