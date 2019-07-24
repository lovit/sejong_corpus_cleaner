import os


sep = os.path.sep

def is_colloquial_file(path):
    """
    Argument
    --------
    path : str
        File path
    """
    path = os.path.abspath(path)
    filename = path.split(sep)[-1]
    return '_' in filename
