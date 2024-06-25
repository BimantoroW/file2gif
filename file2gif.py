import sys
from encoder import Encoder
from decoder import Decoder

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('bro')
    
    if sys.argv[1] == '-d':
        path = sys.argv[2]
        dec = Decoder()
        dec.decode(path)
    else:
        path = sys.argv[1]
        size = sys.argv[2]
        size = size.split('x')
        size = (int(size[0]), int(size[1]))
        enc = Encoder(size)
        enc.encode(path)