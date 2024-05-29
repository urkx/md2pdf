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
        f = open(self.filename, 'a')
        f.write(self.header.version)
        b = b + len(bytes(self.header.version, 'utf-8'))
        for x in self.body.objects:
            f.write(x)
            b = b + len(bytes(x, 'utf-8'))
        f.write('xref')
        for x in self.xref.table:
            f.write(x.first_object + ' ' + x.num_entries)
            for y in x.entries:
                f.write(y)
        f.write('trailer')
        f.write('<<')
        for k in self.trailer.entries:
            f.write('/' + k + ' ' + self.trailer.entries[k])
        f.write('>>')
        f.write('startxref')
        f.write(str(b))
        f.write("%%EOF")
        f.close

class PDFReader:
    def __init__(self, name: str):
        self.name = name

    def read(self):
        f = open(self.name, 'rb')
        l = f.readlines()
        for line in l:
            print(line)
        
header = Header('%PDF-1.1')
body = Body(['(hola)'])
xref = Xref([XrefSubsection('0', '1', ['0000000000 65535 f \r\n'])])
trailer = Trailer({'Size': '1', 'Root': '2 0 R'})
pdf = PDF(header, body, xref, trailer, 'test.pdf')

pdf.create()

reader = PDFReader('probe.pdf')
reader.read()
