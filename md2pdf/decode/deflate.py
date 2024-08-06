from enum import Enum
from typing import Union

class FlateDecode:
    '''
        Decompress data using deflate algorithm (RFC 1951).
        Ref: https://datatracker.ietf.org/doc/html/rfc1951

        From zlib source code (deflate.c -> deflate_slow) block processing is:
        - fill window
        - find match
        - flush block: 
            - build length tree
            - build distance tree
            - build bit lenght tree
            - gen codes
    '''
    def __init__(self):
        pass

    def test(self):
        lz = self.LZ77("Tres tristes tigres tragaban trigo en un trigal", 5)
        matches = lz.code()
        pass
    
    class Btype(Enum):
        NO_COMPRESSION  = 0
        FIX_COMPRESSION = 1
        DYN_COMPRESSION = 2
        ERROR           = 3

    class Block:
        def __init__(self, final: bool, type: Union[Btype.NO]):
            self.final = final