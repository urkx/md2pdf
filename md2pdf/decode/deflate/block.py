from dataclasses import dataclass
from enum import Enum

class BlockType(Enum):
    UNCOMPRESSED    = 0
    FIX_COMPRESSION = 1
    DYN_COMPRESSION = 2
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
    def __init__(self, header: BlockHeader, data: BlockData):
        self.header = header
        self.data = data

    def process(self):
        pass