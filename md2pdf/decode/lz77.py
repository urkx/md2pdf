from dataclasses import dataclass

class LZ77:
        '''
            LZ77 implementation as explained in Microsoft documentation.
            https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wusp/fb98aa28-5cd7-407f-8869-a6cef1ff1ccb


            Params:
                - data: data to encode.
                - win_size: size of search buffer
        '''
        def __init__(self, data: str, win_size: int):
            self.data = data
            self.win_size = win_size

        @dataclass
        class Pair:
            """
                Distance,length pair data
            """
            distance: int
            length: int

            def __repr__(self) -> str:
                return f"[ {self.distance}, {self.length} ]"

        class Triplet:
            '''
                Triplet stored in the output
            '''
            def __init__(self, distance: int, length: int, char: str):
                self.distance = distance
                self.length = length
                self.char = char

            def __repr__(self) -> str:
                return f"[ {self.distance}, {self.length}, {self.char} ]"
            
        def search_longets_match(self, search_buffer: str, sp: int, lp: int, wp: int) -> tuple[list[Triplet], Triplet | None]:
            '''
                Search for the longest match in the search buffer for the lookahead buffer.

                Params:
                    - search_buffer: Buffer where to find the matches.
                    - sp: Begin of the search_buffer in the original data.
                    - lp: Lookahead buffer pointer.
                    - wp: Pointer to byte processing
            '''
            match_list = []
            actual_match = None
            m = ''
            matching = False
            x =  sp
            while x < len(search_buffer):
                if search_buffer[x] == self.data[lp]:
                        m = m + search_buffer[x]
                        if actual_match is None:
                            actual_match = self.Triplet(wp - x, len(m), '')
                        else:
                            actual_match.length = len(m)
                        lp = lp + 1
                        if lp >= len(self.data): lp = len(self.data) - 1
                        if not matching: matching = True
                        x = x + 1
                elif matching:
                        lp = wp
                        match_list.append(actual_match)
                        m = ''
                        matching = False
                        actual_match = None
                else:
                    x = x + 1
            return match_list, actual_match

        def code(self) -> list[Pair | str]:
            '''
                Encodes data using LZ77 algorithm.
                Return a list of :py:class:`Triplet`
            '''
            buffered_output = []
            # wp -> sliding window pointer
            # sp -> search pointer
            # lp -> lookahead pointer
            wp = 0
            while wp < len(self.data):
                '''
                    STEP 1: Create search buffer
                '''
                sp = 0
                lp = wp
                search_buffer = ''
                if wp > self.win_size: sp = wp - self.win_size
                search_buffer = self.data[sp:wp]
                '''
                    STEP 2: Search longest match
                '''
                match_list, actual_match = self.search_longets_match(search_buffer, sp, lp, wp)
                '''
                    STEP 3: 
                        If matches found, use the one with longest length (L) and increase WP + L.
                        Else, output actual byte and increase WP + 1
                '''
                dwp = 1
                if actual_match is None and len(match_list) == 0: 
                    match_list.append(self.Triplet(0, 0, self.data[wp])) # if not match found, character is the pointed by wp
                elif actual_match is not None:
                    match_list.append(actual_match)
                    dwp = actual_match.length
                match_list.sort(key=lambda x: x.length, reverse=True) # order matches by longest length
                buffered_output.append(match_list[0])
                if match_list[0].length > 0: dwp = match_list[0].length
                wp = wp + dwp
            output = [x.char if x.char != '' else self.Pair(distance=x.distance, length=x.length) for x in buffered_output]
            return output
        
        def decode(self, input: list[Pair | str]) -> str:
            '''
                Params:
                - Input: List of :py:class:`Triplet` to decode
            '''
            output = ''
            for i in input:
                if type(i) == str:
                    output = output + i
                else:
                    d, l = i.distance, i.length
                    actual_pointer = len(output)
                    new_data = output[actual_pointer - d: (actual_pointer - d) + l]
                    output = output + new_data
            return output
