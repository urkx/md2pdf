from enum import Enum
from typing import Union
from dataclasses import dataclass
from block import Block
from ctypes import c_uint8

class CompressionLevel(Enum):
    FASTEST = 0
    FAST    = 1
    DEFAULT = 2
    SLOWEST = 3

@dataclass
class DataHeader:
    compression_method: c_uint8 = 8     # 4 bits
    compression_info: c_uint8           # 4 bits. contains the base-2 logarithm of the LZ77 window size minus 8
    check_bits: c_uint8                 # 5 bits
    preset_dictionary: bool             # 1 bit
    compression_level: CompressionLevel # 2 bits

@dataclass
class CompressedData:
    block: list[Block]

class Checksum:
    pass

class Deflate:
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

        Found resume: https://github.com/libyal/assorted/blob/main/documentation/Deflate%20(zlib)%20compressed%20data%20format.asciidoc
    '''
    def __init__(self, data_header: DataHeader, compressed_data: CompressedData, checksum: Checksum):
        self.data_header = data_header
        self.compressed_data = compressed_data
        self.checksum = checksum

    def test(self):
        lz = self.LZ77("Tres tristes tigres tragaban trigo en un trigal", 5)
        matches = lz.code()
        pass
