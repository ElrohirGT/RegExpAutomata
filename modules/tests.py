import unittest
from shunYard import toPostFix
from regexpToAFN import toAFN, newAFN

# All tests will be added to this file!


class TestShuntingYard(unittest.TestCase):
    def test_basic_example(self):
        infix = "ab"
        expected = "ab."
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        infix = "_+a*b"
        expected = "a*_+b"
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)


class TestRegexToAFN(unittest.TestCase):
    def test_basic_regexp(self):
        postfix = "ab."
        expected = newAFN([{"a": [1]}, {"_": [2]}, {"b": [3]}, {}], 3)
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

    def test_or_regexp(self):
        postfix = "ab+"
        expected = newAFN(
            [{"_": [1, 4]}, {"a": [2]}, {"_": 3}, {}, {"b": [5]}, {"_": 3}], 3
        )
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


if __name__ == "__main__":
    # print(toPostFix)
    unittest.main()
