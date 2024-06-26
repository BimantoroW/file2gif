import sys
from encoder import Encoder
from decoder import Decoder

DEFAULT_SIZE = (1000, 1000)

def help():
    print(f'Usage: py {sys.argv[0]} [-d] file [widthXheight]')

if __name__ == '__main__':
    if ((len(sys.argv) < 2 or len(sys.argv) > 3)
        or (sys.argv[1] == '--help' or sys.argv[1] == '-h')):
        help()
        exit(0)
    
    if sys.argv[1] == '-d':
        path = sys.argv[2]
        dec = Decoder()
        dec.decode(path)
    else:
        path = sys.argv[1]
        if len(sys.argv) == 3:
            size = sys.argv[2]
            size = size.split('X') 
            size = (int(size[0]), int(size[1]))
        else:
            size = DEFAULT_SIZE
        enc = Encoder(path, size)
        enc.encode()