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
print(enc)
print(lzw.decode(enc))
