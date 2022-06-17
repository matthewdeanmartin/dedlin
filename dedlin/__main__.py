import sys

from dedlin.main import go

if __name__ == '__main__':
    file = sys.argv[1:]
    sys.exit(go(str(file)))