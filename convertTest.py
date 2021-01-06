from transistor_counter import convert
import unittest


class TestConvertMethods(unittest.TestCase):

    def test_convert(self):
        self.assertEqual(convert("4'hb"), "1011")
        self.assertEqual(convert("7'h24"),"0100100")
        self.assertEqual(convert("4'h1"),"0001")
        self.assertEqual(convert("8'hff"),"11111111")
        self.assertEqual(convert("4'o11"),"1001")
        self.assertEqual(convert("8'o53"),"00101011")
        self.assertEqual(convert("4'b0110"),"0110")

if __name__ == '__main__':
    unittest.main()
