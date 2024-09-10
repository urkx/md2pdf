from dataclasses import dataclass
from enum import Enum

from md2pdf.decode import lz77

class BlockType(Enum):
    UNCOMPRESSED    = 0
    FIX_COMPRESSION = 1 # Pre-agreed Huffman tree, defined by Deflate spec
    DYN_COMPRESSION = 2 # Huffman table supplied
    ERROR           = 3

@dataclass
class BlockHeader:
    last_block: bool
    block_type: BlockType

class BlockData:
    """Block data interface
    """
    pass

class Block:
    def __init__(self, header: BlockHeader, raw_data: str):
        self.header = header
        self.raw_data = raw_data

    def process(self) -> list[lz77.LZ77.Pair | str]:
        l = lz77.LZ77(self.raw_data, lz77.LZ77.MAX_WIN_SIZE_DEFLATE)
        return l.code()
