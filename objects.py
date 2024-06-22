class PdfObject():
    def value(self) -> str:
        pass

class Integer(PdfObject):
    def __init__(self, val: int) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'{self.val}'

class String(PdfObject):
    def __init__(self, val: str) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'({self.val})'
    
class Name(PdfObject):
    def __init__(self, val: str) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'/{self.val}'
    
class Array(PdfObject):
    def __init__(self, val: list) -> None:
        self.val = val
    
    def value(self) -> str:
        res = ''
        for x in self.val:
            res += x
            res += ' '
        res = res[:-1]
        return f'[{res}]'
    
class Dictionary(PdfObject):
    def __init__(self, val: dict) -> None:
        self.val = val
    
    def getDictItemValue(self, item):
        if type(item) == type(PdfObject):
            return item.value()
        if type(item) == type(str):
            return item
        else:
            return str(item)

    def value(self) -> str:
        res = '<<'

        for x in self.val.items():
            res += self.getDictItemValue(x[0])
            res += ' '
            res += self.getDictItemValue(x[1])
            res += '\n'

        res += '>>'
        return res

class IndirectObject:
    def __init__(self, number: int, gen: int, obj: PdfObject) -> None:
        self.number = number
        self.gen = gen
        self.obj = obj

    def value(self) -> str:
        res = f'{self.number} {self.gen} obj\n'
        res += self.obj.value()
        res += '\n'
        res += 'endobj'
        return res


class Stream:
    class StreamDictionary(Dictionary):
        def __init__(self, l: int) -> None:
            super().__init__({'/Length': l})

    def __init__(self, d: StreamDictionary, s: str) -> None:
        if '/Length' not in d.val:
            raise Exception('Stream Length must exist in stream dictionary')
        if d.val['/Length'] != len(s):
            raise Exception('Stream data length not match with Length value')
        self.d = d
        self.s = s
    
    def value(self) -> str:
        res = ''
        res += self.d.value()
        res += '\n'
        res += 'stream'
        res += '\n'
        res += self.s
        res += '\n'
        res += 'endstream'

        return res

t = Name('Type')
tv = Name('Example')
st = Name('Subtype')
stv = Name('Dictionary example')
v = Name('Version')
vv = Integer(12)

d = Dictionary({t: tv, st: stv, v: vv})
io = IndirectObject(10, 0, d)

streamDict = Stream.StreamDictionary(2)
stream = Stream(streamDict, "AA")
indirectStream = IndirectObject(1, 0, stream)

print(indirectStream.value())

