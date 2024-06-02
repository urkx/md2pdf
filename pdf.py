class Header:
    def __init__(self, version: str):
        self.version = version

class Body:
    def __init__(self, objects: list):
        self.objects = objects

class Xref:
    def __init__(self, table: list):
        self.table = table

class XrefSubsection:
    def __init__(self, first_object: str, num_entries: str, entries: list):
        self.first_object = first_object
        self.num_entries = num_entries
        self.entries = entries
        
class Trailer:
    def __init__(self, entries: dict):
        self.entries = entries

class PDF:
    def __init__(self, header: Header, body: Body, xref: Xref, trailer: Trailer, filename: str):
        self.header = header
        self.body = body
        self.xref = xref
        self.trailer = trailer
        self.filename = filename

    def create(self):
        b = 0
        f = open(self.filename, 'ab')
        f.write(bytes(self.header.version, 'utf-8') + b'\n')
        b = b + len(bytes(self.header.version, 'utf-8'))
        for x in self.body.objects:
            f.write(bytes(x, 'utf-8') + b'\n')
            b = b + len(bytes(x, 'utf-8'))
        f.write(b'xref' + b'\n')
        for x in self.xref.table:
            f.write(bytes(x.first_object, 'utf-8') + b' ' + bytes(x.num_entries, 'utf-8') + b'\n')
            for y in x.entries:
                f.write(bytes(y, 'utf-8') + b'\n')
        f.write(b'trailer' + b'\n')
        f.write(b'<<')
        for k in self.trailer.entries:
            f.write(b'/' + bytes(k, 'utf-8') + b' ' + bytes(self.trailer.entries[k], 'utf-8'))
        f.write(b'\n')
        f.write(b'>>' + b'\n')
        f.write(b'startxref' + b'\n')
        f.write(bytes(str(b), 'utf-8') + b'\n')
        f.write(b"%%EOF" + b'\n')
        f.close

class PDFReader:
    def __init__(self, name: str):
        self.name = name

    def read(self):
        f = open(self.name, 'rb')
        l = f.readlines()
        for line in l:
            print(line)

import os

try:
    os.remove('test.pdf')
except Exception:
    pass

header = Header('%PDF-1.1')
body = Body(['(hola)'])
xref = Xref([XrefSubsection('0', '1', ['0000000000 65535 f \r\n'])])
trailer = Trailer({'Size': '1', 'Root': '1 0 R'})
pdf = PDF(header, body, xref, trailer, 'test.pdf')

pdf.create()

reader = PDFReader('probe.pdf')
reader.read()

print('=====================================')
print('=====================================')
print('=====================================')

reader = PDFReader('test.pdf')
reader.read()