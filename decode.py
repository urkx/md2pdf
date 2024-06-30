import base64

class ASCIIHexDecode:
    '''
        Decodes data that has been encoded in ASCII hexadecimal form
    '''
    def __init__(self):
        pass

    def encode(data: str) -> str:
        '''
            returns a string containing ASCII Hex bytes
        '''
        return data.encode('ASCII').hex()


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

    def encode(data: bytes) -> bytes:
        return base64.a85encode(data)

    def decode(data: bytes) -> bytes:
        return base64.a85decode(data)
    

t = 'hola'
te = ASCII85Decode.encode(bytes(t, 'ASCII'))
td = ASCII85Decode.decode(te)

print(te)
print(td.decode('ASCII'))
