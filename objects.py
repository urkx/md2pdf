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

    def value(self) -> str:
        res = '<<'

        for x in self.val.items():
            res += x[0].value()
            res += ' '
            res += x[1].value()
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
    def __init__(self, d: Dictionary, s: str, number: int, gen: int) -> None:
        self.d = d
        self.s = s
        self.number = number
        self.gen = gen
    
    def value(self) -> str:
        res = ''
        res += self.d.value()
        res += '\n'
        res += 'stream'
        res += self.s
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
print(io.value())

