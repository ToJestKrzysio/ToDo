from functools import lru_cache
from os.path import isfile


@lru_cache
def load_file(name: str) -> str:
    """ Loads content of the file. """
    if not isfile(name):
        raise FileNotFoundError(f"File '{name}' does not exist.")
    with open(name, "r") as file_:
        return file_.read()
