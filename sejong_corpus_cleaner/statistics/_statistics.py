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

def count_tag_words(corpus):
    """corpus is nested list (like) format

        [[(word, tag), (word, tag), .. ],
         [(word, tag), (word, tag), .. ],
         ...
        ]
    """
    counter = Counter((tag, word) for sent in corpus for word, tag in sent)
    counter_ = defaultdict(lambda: {})
    for (tag, word), count in counter.items():
        counter_[tag][word] = count
    return counter_