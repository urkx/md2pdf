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
