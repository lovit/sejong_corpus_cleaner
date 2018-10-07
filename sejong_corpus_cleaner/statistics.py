from collections import Counter

def count_tags(corpus):
    """corpus is nested list (like) format

        [[(word, tag), (word, tag), .. ],
         [(word, tag), (word, tag), .. ],
         ...
        ]
    """
    return Counter(tag for sent in corpus for _, tag in sent)