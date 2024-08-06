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
    
    @staticmethod
    def dem322():
        '''
            Example of the algorithm described in section 3.2.2
            https://datatracker.ietf.org/doc/html/rfc1951#section-3

            Dynamic Huffman codes generation(?)
            In zlib code: trees.c -> gen_codes
        '''
        # ABCDEFGH -> (3, 3, 3, 3, 3, 2, 4, 4)
        SAMPLES = 8
        tree_len = [3, 3, 3, 3, 3, 2, 4, 4]
        tree_code = []
        # Step 1
        bl_count = {}
        bl_count[1] = 0
        bl_count[2] = 1
        bl_count[3] = 5
        bl_count[4] = 2

        # Step 2
        next_code = {}
        code = 0
        bl_count[0] = 0
        for bits in range(1, 5):
            code = (code + bl_count[bits-1]) << 1
            next_code[bits] = code
        print(next_code)
        # Step 3
        for n in range(0, SAMPLES):
            l = tree_len[n]
            if l != 0:
                tree_code.append(next_code[l])
                next_code[l] = next_code[l] + 1

        print(tree_code)