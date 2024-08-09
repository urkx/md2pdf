from block import BlockData
from dataclasses import dataclass
from ctypes import c_uint16, c_uint8

class Uncompressed(BlockData):
    """Uncompressed block data.
    """
    def __init__(self, data_size: c_uint16, data: bytearray):
        """
        Args:
            data_size (int): 2 bytes
            comp_data_size: 2 bytes. 1s complement of data
            data (bytearray): uncompressed data
        """
        self.data_size = data_size
        self.comp_data_size = ~data_size
        self.data = data

@dataclass
class DynHuffmanTable:
    """Dynamic Huffman table

        Args:
            num_literal_codes (int): 5 bits. Number of literal codes
            num_distance_codes (int): 5 bits. Number of distance codes
            num_huffman_codes (int): 4 bits. Number of Huffman codes for the code sizes
            code_sizes (list[int]): The code sizes
            literal_huff_stream (bytearray): Huffman encoded stream of the Huffman codes for the literals
            distances_huff_stream (bytearray): Huffman encoded stream of the Huffman codes for the distances
    """
    num_literal_codes: c_uint8
    num_distance_codes: c_uint8
    num_huffman_codes: c_uint8
    code_sizes: list[c_uint8] = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
    literal_huff_stream: bytearray
    distances_huff_stream: bytearray

class HuffmanCompressed(BlockData):
    """Huffman compressed block data
    """
    def __init__(self, dyn_huff_table: DynHuffmanTable, encoded_bit_stream: bytearray, end_of_stream: any):
        self.dyn_huff_table = dyn_huff_table
        self.encoded_bit_stream = encoded_bit_stream
        self.end_of_stream = end_of_stream
        
