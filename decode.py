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
            Huffman encoding implementation.

            Params:
                - data: data to encode.

            Internal params:
                - data: original data to encode.
                - freq_list: list that contains all uniques characters in data and its frequency ordered by the frequency.
                - trad_map: map that contains all uniques characters in data and its assigned code.
        '''
        def __init__(self, data):
            self.freq_list = []
            self.data = data
            self.trad_map = {}
            self.order_criteria = lambda x: x.freq

        class ListItem:
            '''
                Items that stores freq_list

                Params:
                    - item: value to store
                    - freq: frequency of the item
            '''
            def __init__(self, item, freq):
                self.item = item
                self.freq = freq

            def __str__(self) -> str:
                return f'[{self.item}: {self.freq}]'
            
            def __repr__(self) -> str:
                return f'[{self.item}: {self.freq}]'

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
        

        def load_freq_map(self) -> None:
            '''
                Creates a sorted list of frequencies for the original data.
            '''
            m = {}
            for c in self.data:
                if c not in m:
                    m[c] = 1
                else:
                    m[c] = m[c] + 1

            self.freq_list = [self.ListItem(x[0], x[1]) for x in m.items()]
            # Sort the items list by frequency in ascending order
            self.freq_list = sorted(self.freq_list, key=self.order_criteria)
                
        def build_tree(self):
            '''
                Creates the Huffman tree from the frequencies map.
                The result is the frequencies map containing only one entry, the root node, and its frequency.

                TODO: optimize data structures (Node, ListItem).
            '''
            while len(self.freq_list) > 1:
                # List of items is sorted by frequency in ascending order, so we take the first 2 elements
                a = self.freq_list.pop(0)
                b = self.freq_list.pop(0)

                a_label = ""
                b_label = ""
                af = a.freq
                bf = b.freq

                if type(a.item) == self.Node:
                    a_label = a.item.label
                elif type(a.item) == str:
                    a_label = a.item
                    a = self.Node(a_label, af)

                if type(b.item) == self.Node:
                    b_label = b.item.label
                elif type(b.item) == str:
                    b_label = b.item
                    b = self.Node(b_label, bf)

                newNode = self.Node(a_label+b_label, af+bf, a, b)
                newItem = self.ListItem(newNode, newNode.freq)
                # insert new item in list
                
                self.freq_list.append(newItem)
                # Sort again the list by frequency in ascending order
                self.freq_list = sorted(self.freq_list, key=self.order_criteria)

        def create_codes(self, node: Node, val: str, huff: str, d: dict):
            '''
                Process all the nodes of the tree and generates its codes

                Params:
                    - node: Node to process.
                    - val: code generated previously.
                    - huff: new bit to add to the code. If the new node to process is left, val = 0. Else, val = 1.
                    - d: map to store the codes and its character.
            '''
            newVal = val + huff
            if(node.left):
                if type(node.left) == self.ListItem:
                    self.create_codes(node.left.item, newVal, '0', d)
                elif type(node.left) == self.Node:
                    self.create_codes(node.left, newVal, '0', d)
            if(node.right):
                if type(node.right) == self.ListItem:
                    self.create_codes(node.right.item, newVal, '1', d)
                elif type(node.right) == self.Node:
                    self.create_codes(node.right, newVal, '1', d)

            if(not node.left and not node.right):
                print(f"{node.label} -> {newVal}")
                d[node.label] = newVal
        
        def code(self) -> str:
            '''
                Initialize the trad_map and invokes create_codes.

                Returns encoding of the original data.
            '''
            root = self.freq_list[0]
            self.trad_map = {}
            self.create_codes(root.item, '', '', self.trad_map)
            res = ''
            for c in self.data:
                res = res + self.trad_map[c]
            return res               

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

s = 'tres tristes tigres tragaban trigo en un trigal'
huff = FlateDecode.Huffman(s)
huff.load_freq_map()
huff.build_tree()
print(huff.code())
