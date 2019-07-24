from bs4 import BeautifulSoup
import os


sep = os.path.sep

def is_colloquial_file(path):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    flag : Booolean
        Weather the file at path is colloquial corpus or not
    """
    path = os.path.abspath(path)
    filename = path.split(sep)[-1]
    return '_' in filename

def read_txt_as_soup(path, encoding='utf-16'):
    """
    Argument
    --------
    path : str
        File path

    Returns
    -------
    soup : BeautifulSoup
        XML formed document
    """
    try:
        with open(path, encoding=encoding) as f:
            text = f.read()
            soup = BeautifulSoup(text, 'lxml')
            return soup
    except:
        raise ValueError('Failed to read txt: {}'.format(path))