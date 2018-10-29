from collections import Counter
from collections import defaultdict

def count_tags(corpus):
    """corpus is nested list (like) format

        [[(word, tag), (word, tag), .. ],
         [(word, tag), (word, tag), .. ],
         ...
        ]
    """
    return Counter(tag for sent in corpus for _, tag in sent)

def count_tag_morphs(corpus):
    """corpus is nested list (like) format

        [[(word, tag), (word, tag), .. ],
         [(word, tag), (word, tag), .. ],
         ...
        ]
    """
    counter = Counter((tag, morph) for sent in corpus for morph, tag in sent)
    counter_ = defaultdict(lambda: {})
    for (tag, morph), count in counter.items():
        counter_[tag][morph] = count
    return counter_