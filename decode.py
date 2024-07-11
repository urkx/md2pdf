import base64

class ASCIIHexDecode:
    '''
        Decodes data that has been encoded in ASCII hexadecimal form
    '''
    def __init__(self):
        pass

    @staticmethod
    def encode(data: str) -> str:
        '''
            returns a string containing ASCII Hex bytes
        '''
        return data.encode('ASCII').hex()

    @staticmethod
    def decode(data: str) -> str:
        '''
            data must be string containing ASCII Hex bytes
        '''
        return bytearray.fromhex(data).decode('ASCII')

class ASCII85Decode:
    '''
        Decodes data that has been encoded in ASCII base-85
    '''
    def __init__(self):
        pass
    
    @staticmethod
    def encode(data: bytes) -> bytes:
        return base64.a85encode(data)

    @staticmethod
    def decode(data: bytes) -> bytes:
        return base64.a85decode(data)
    
class LZWDecode:
    def __init__(self):
        '''
            d: Dictionary.  Initally loaded with 256 values (256 8-bit characters).
            t: Dictionary initial size.
            b: Number of bits used
        '''
        self.t = 256
        self.b = 8
        self.b = self.b + 1 # Used all 8-bit possible characters
        

    def encode(self, data: bytearray) -> list:
        '''
            LZW Encoding process.

            Parameters:
            data: ASCII-encoded bytes to encode

            Returns:
            list: List containing the bytes to which input data has been encoded.
        '''
        dictionary = {}
        for i in range(self.t):
            dictionary[chr(i)] = i
        dictionary['EOF'] = self.t
        idx = len(dictionary)

        res = []
        secuencia = ""
        for d in data:
            aux = secuencia + chr(d)
            if aux in dictionary:
                secuencia = aux
            else:
                res.append(dictionary[secuencia])
                dictionary[aux] = idx
                idx = idx + 1
                secuencia = "" + chr(d)
        if secuencia != '':
            res.append(dictionary[secuencia])
        return res

    def decode(self, data: list) -> str:
        '''
            LZW Decoding process.

            Parameters:
            data: LZW-encoded bytes list to decode

            Returns:
            str: Original string decoded
        '''
        dictionary = {}
        for i in range(self.t):
            dictionary[i] = chr(i)
        dictionary[self.t] = 'EOF'
        idx = len(dictionary)
        
        cadena = chr(data.pop(0))
        descomp = cadena
        for d in data:
            subpalabra = ""
            if d in dictionary:
                subpalabra = dictionary[d]
            elif d == idx:
                subpalabra = cadena + cadena[0:1]
            descomp = descomp + subpalabra
            dictionary[idx] = cadena + subpalabra[0:1]
            idx = idx + 1
            cadena = subpalabra   
        return descomp

class FlateDecode:
    '''
        Decompress data using deflate algorithm (RFC 1951).
        Ref: https://datatracker.ietf.org/doc/html/rfc1951

    '''
    class LZ77:
        '''
            TODO: Implement LZ77 algorithm
        '''
        def __init__(self):
            pass

    class Huffman:
        '''
            TODO: Implement Huffman encoding
        '''
        def __init__(self):
            self.freq_map = {}

        def load_freq_map(self, data: str) -> None:
            '''
                Creates a map of frequencies for the characters of the input.

                Input:
                String to encode
            '''
            for c in data:
                if c not in self.freq_map:
                    self.freq_map[c] = 1
                else:
                    self.freq_map[c] = self.freq_map[c] + 1
        class Node:
            '''
                Internal Huffman node.

                Params:
                    - label: label to identify the node
                    - freq: frequency of the node
                    - left: left child of the node. Can be str or other Node
                    - right: right child of the node. Can be str or other Node
            '''
            def __init__(self, label: str, freq: int, left=None, right=None):
                self.label = label
                self.freq = freq
                self.left = left
                self.right = right

            def __str__(self) -> str:
                return f'{self.label}: {self.left} - {self.right}'
            
            def __repr__(self) -> str:
                return f'{self.label}: {self.left} - {self.right}'

        def build_tree(self):
            '''
                Creates the Huffman tree from the frequencies map.
                The result is the frequencies map containing only one entry, the root node, and its frequency.

                TODO: optimize minimums search.
            '''
            while len(self.freq_map) > 1:
                a = None
                af = 0
                b = None
                bf = 0
                
                # Search first min
                for entry in self.freq_map.items():
                    if af != 0 and entry[1] < af:
                        af = entry[1]
                        a = entry[0]
                    elif af == 0:
                        af = entry[1]
                        a = entry[0]
                # Search second min
                for entry in self.freq_map.items():
                    if entry[0] != a:
                        if bf != 0 and entry[1] <= bf:
                            bf = entry[1]
                            b = entry[0]
                        elif bf == 0:
                            bf = entry[1]
                            b = entry[0]
                
                self.freq_map.pop(a) # Removes the node a entry from the map
                self.freq_map.pop(b) # Removes the node b entry from the map

                a_label = ""
                b_label = ""
                if type(a) == self.Node:
                    a_label = a.label
                elif type(a) == str:
                    a_label = a
                    a = self.Node(a, af)

                if type(b) == self.Node:
                    b_label = b.label
                elif type(b) == str:
                    b_label = b
                    b = self.Node(b, bf)
                
                self.freq_map[self.Node(a_label+b_label, af+bf, a, b)] = af+bf

        def process_node(self, node: Node, val: str, huff: str):
            newVal = val + huff
            if(node.left):
                self.process_node(node.left, newVal, '0')
            if(node.right):
                self.process_node(node.right, newVal, '1')

            if(not node.left and not node.right):
                print(f"{node.label} -> {newVal}")
        
        def create_codes(self):
            root = [x for x in self.freq_map.items()][0][0]
            self.process_node(root, '', '')
                

class Utils:
    '''
        Static utils methods
    '''
    def __init__(self):
        pass    
    
    @staticmethod
    def str_to_binstr(data: str) -> str:
        '''
            Returns binary representation of ASCII data
        
            Parameters:
            data (str): Input data

            Returns:
            str: Binary representation of data
        '''
        return ' '.join(map(bin, bytearray(data, 'ASCII')))
    
    @staticmethod
    def char_to_bin(data: str) -> str:
        '''
            Returns 8-bit binary representation of a character
        '''
        return f'{ord(data):08b}'

t = 'hola'
te = ASCII85Decode.encode(bytes(t, 'ASCII'))
td = ASCII85Decode.decode(te)

# print(te)
# print(td.decode('ASCII'))
# print(Utils.char_to_bin('a'))

lzw = LZWDecode()
enc = lzw.encode(bytearray('tres tristes tigres tragaban trigo en un trigal', 'ASCII'))
# print(enc)
# print(lzw.decode(enc))

huff = FlateDecode.Huffman()
huff.load_freq_map('tres tristes tigres tragaban trigo en un trigal')
huff.build_tree()
huff.create_codes()
