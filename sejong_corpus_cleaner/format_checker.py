sejong_tagset = {
    "NNB", "NNG", "NNP", "XR", "XSN", "NR", "NP", "MM", "XPN", "MAG",
    "MAJ", "JC", "JKB", "JKC", "JKG", "JKO", "JKQ", "JKS", "JKV", "JX",
    "IC", "VA", "VCN", "VCP", "XSA", "VV", "VX", "XSV", "EC", "EF",
    "EP", "ETM", "ETN", "NA", "SE", "SF", "SH", "SL", "SN", "SO",
    "SP", "SS", "SW"
}

def check_sejong_tagset(sentence):
    """
    Argument
    --------
    sentence : Sentence

    Returns
    -------
    flag : Boolean
        It returns True if there exists un-defined tag in the sentence
    """
    for _, morphtags in sentence:
        for morphtag in morphtags:
            if not (morphtag.tag in sejong_tagset):
                return False
    return True
