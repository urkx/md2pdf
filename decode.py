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
        d = {}
        for i in range(self.t-1):
            d[i] = i
        self.b = self.b + 1 # Used all 8-bit possible characters
        d[self.t] = '#' # End character
        self.d = d
        

    def encode(self, data: bytes) -> bytes:
        print(self.d)
        return data

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

print(te)
print(td.decode('ASCII'))
print(Utils.char_to_bin('a'))

lzw = LZWDecode()
d = lzw.encode(bytes('hola', 'ASCII'))
print(d)
