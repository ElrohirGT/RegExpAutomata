import unittest
from shunYard import toPostFix
from regexpToAFN import toAFN

# All tests will be added to this file!

class TestShuntingYard(unittest.TestCase):
    def test_basic_example(self):
        infix = "a+b"
        expected = "ab+"
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        infix = "_+a*b"
        expected = "a*_+b"
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

class TestRegexToAFN(unittest.TestCase):
    def test_basic_regexp(self):
        postfix = "ab+"
        expected = """0 a 1
0 b 1
---
1"""
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        postfix = "a*_+b"
        expected = """0 _ 1
0 _ 2
1 _ 3
1 _ 4
2 _ 5
3 a 6
4 b 7
5 _ 8
6 _ 3
7 _ 8
---
8"""
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    # print(toPostFix)
    unittest.main()
