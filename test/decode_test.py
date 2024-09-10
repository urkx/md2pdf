import unittest
from md2pdf.decode import lzw, huffman, lz77
from md2pdf.decode.deflate.block import BlockHeader, BlockType, Block

class TestLZWDecode(unittest.TestCase):
    def test_encode(self):
        _lzw = lzw.LZWDecode()
        self.assertEqual(_lzw.encode(bytearray('tres tristes tigres tragaban trigo en un trigal', 'ASCII')), 
                         [116, 114, 101, 115, 32, 257, 105, 115, 116, 259, 261, 105, 103, 258, 260, 257, 97, 103, 97, 98, 97, 110, 261, 114, 268, 111, 32, 101, 278, 117, 278, 262, 274, 108],
                         "Encoding failed")
        
    def test_decoding(self):
        _lzw = lzw.LZWDecode()
        test = _lzw.encode(bytearray('tres tristes tigres tragaban trigo en un trigal', 'ASCII'))
        self.assertEqual(_lzw.decode(test),
                         "tres tristes tigres tragaban trigo en un trigal",
                         "Decoding failed")
        
class TestHuffmanDecode(unittest.TestCase):
    def test_encode(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        want = '10001111011110101100011111111101001101111010110011110000111101111010110001100100000101000001110010110001111110000100110111011100101010101100101100011111100000101011'
        huff = huffman.Huffman(test)
        huff.load_freq_map()
        huff.build_tree()
        c = huff.code()
        self.assertEqual(c,
                         want,
                         "Encoding failed")
        
    def test_decode(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        huff = huffman.Huffman(test)
        c = huff.code()
        d = huff.decode(c)
        self.assertEqual(d,
                         test,
                         "Decoding failed")

class TestLZ77(unittest.TestCase):
    def test_codec(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        lz = lz77.LZ77(test, 6)
        c = lz.code()
        self.assertEqual(test, lz.decode(c), "LZ77 co-dec failed")

class TestDeflateBlockDynCompression(unittest.TestCase):
    def test_block_processing(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        want = '0011000111010000100101010010110110001101011100111110000100011001010011101001010110110101111100011001110101101111100111011111011111000000010010'
        b = Block(BlockHeader(False, BlockType.DYN_COMPRESSION), test)
        res = b.process()
        self.assertEqual(want, res, "Deflate block processing failed")
        
if __name__ == "__main__":
    unittest.main()