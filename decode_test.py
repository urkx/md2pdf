import unittest
import decode

class TestLZWDecode(unittest.TestCase):
    def test_encode(self):
        lzw = decode.LZWDecode()
        self.assertEqual(lzw.encode(bytearray('tres tristes tigres tragaban trigo en un trigal', 'ASCII')), 
                         [116, 114, 101, 115, 32, 257, 105, 115, 116, 259, 261, 105, 103, 258, 260, 257, 97, 103, 97, 98, 97, 110, 261, 114, 268, 111, 32, 101, 278, 117, 278, 262, 274, 108],
                         "Encoding failed")
        
    def test_decoding(self):
        lzw = decode.LZWDecode()
        test = lzw.encode(bytearray('tres tristes tigres tragaban trigo en un trigal', 'ASCII'))
        self.assertEqual(lzw.decode(test),
                         "tres tristes tigres tragaban trigo en un trigal",
                         "Decoding failed")
        
class TestHuffmanDecode(unittest.TestCase):
    def test_encode(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        want = '10001111011110101100011111111101001101111010110011110000111101111010110001100100000101000001110010110001111110000100110111011100101010101100101100011111100000101011'
        huff = decode.FlateDecode.Huffman(test)
        huff.load_freq_map()
        huff.build_tree()
        c = huff.code()
        self.assertEqual(c,
                         want,
                         "Encoding failed")
        
    def test_decode(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        huff = decode.FlateDecode.Huffman(test)
        c = huff.code()
        d = huff.decode(c)
        self.assertEqual(d,
                         test,
                         "Decoding failed")

class TestLZ77(unittest.TestCase):
    def test_codec(self):
        test = 'tres tristes tigres tragaban trigo en un trigal'
        lz = decode.FlateDecode.LZ77(test, 6)
        c = lz.code()
        self.assertEqual(test, lz.decode(c), "LZ77 co-dec failed")
        
if __name__ == "__main__":
    unittest.main()