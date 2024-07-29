import unittest
from md2pdf.objects import objects

class TestObjects(unittest.TestCase):
    def test_integer(self):
        o = objects.Integer(1)
        self.assertEqual(o.value(), '1', 'Value of Integer object is wrong')

    def test_string(self):
        o = objects.Integer('A')
        self.assertEqual(o.value(), 'A', 'Value of String object is wrong')

    def test_name(self):
        o = objects.Name('Test')
        self.assertEqual(o.value(), '/Test', 'Value of Name object is wrong')

    def test_array(self):
        o = objects.Array([1, 2, 3])
        self.assertEqual(o.value(), '[1 2 3]', 'Value of Array object is wrong')
    
    def test_dictionary(self):
        t = objects.Name('Type')
        tv = objects.Name('Example')
        st = objects.Name('Subtype')
        stv = objects.Name('Dictionary example')
        v = objects.Name('Version')
        vv = objects.Integer(12)

        d = objects.Dictionary({t: tv, st: stv, v: vv})
        want = '<</Type /Example\n/Subtype /Dictionary example\n/Version 12\n>>'
        self.assertEqual(d.value(), want, 'Value of Dictionary object is wrong')
    
    def test_indirect_object(self):
        t = objects.Name('Type')
        tv = objects.Name('Example')
        st = objects.Name('Subtype')
        stv = objects.Name('Dictionary example')
        v = objects.Name('Version')
        vv = objects.Integer(12)
        d = objects.Dictionary({t: tv, st: stv, v: vv})
        io = objects.IndirectObject(10, 0, d)

        want = '10 0 obj\n<</Type /Example\n/Subtype /Dictionary example\n/Version 12\n>>\nendobj'
        self.assertEqual(io.value(), want, 'Value of Dictionary object is wrong')

    def test_stream(self):
        streamDict = objects.Stream.StreamDictionary(2)
        stream = objects.Stream(streamDict, 'AA')

        want = '<</Length 2\n>>\nstream\nAA\nendstream'
        self.assertEqual(stream.value(), want, 'Value of Stream object is wrong')

if __name__ == '__main__':
    unittest.main()