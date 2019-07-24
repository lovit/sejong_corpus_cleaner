__author__ = 'lovit'

from .loader import extract_sentences
from .simple_tag import to_simple_tag
from .simple_tag import to_simple_morphtags
from .utils import check_encoding
from .utils import select_morphtags

__all__ = [
    'extract_sentence', 'to_simple_tag', 'to_simple_morphtags',
    'check_encoding', 'select_morphtags'
]