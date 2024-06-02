class Integer:
    def __init__(self, val: int) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'{self.val}'

class String:
    def __init__(self, val: str) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'({self.val})'
    
class Name:
    def __init__(self, val: str) -> None:
        self.val = val
    
    def value(self) -> str:
        return f'/{self.val}'
    
class Array:
    def __init__(self, val: list) -> None:
        self.val = val
    
    def value(self) -> str:
        res = ''
        for x in self.val:
            res += x
            res += ' '
        res = res[:-1]
        return f'[{res}]'
    
class Dictionary:
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


t = Name('Type')
tv = Name('Example')
st = Name('Subtype')
stv = Name('Dictionary example')
v = Name('Version')
vv = Integer(12)

d = Dictionary({t: tv, st: stv, v: vv})
print(d.value())

