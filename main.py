from models.url import URL
from utils.utils import load


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        load(URL("file://./tests/default.txt"))
    elif len(sys.argv) == 2:
        load(URL(sys.argv[1]))
