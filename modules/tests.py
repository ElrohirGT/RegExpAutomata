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
        expected = "a*b._+"
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
            [{"_": [2, 4]}, {}, {"a": [3]}, {"_": [1]}, {"b": [5]}, {"_": [1]}], 1
        )
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

    def test_0_or_more_regepx(self):
        postfix = "a*"
        expected = newAFN([{"_": [1, 2]}, {}, {"a": [3]}, {"_": [1, 2]}], 1)
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

    def test_and_or_regexp(self):
        postfix = "ab.a+"
        expected = newAFN(
            [
                {"_": [2, 6]},
                {},
                {"a": [3]},
                {"_": [4]},
                {"b": [5]},
                {"_": [1]},
                {"a": [7]},
                {"_": [1]},
            ],
            1,
        )
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        self.maxDiff = None
        postfix = "a*b._+"
        expected = newAFN(
            [
                {"_": [2, 8]},
                {},
                {"_": [3, 4]},
                {"_": [6]},
                {"a": [5]},
                {"_": [3, 4]},
                {"b": [7]},
                {"_": [1]},
                {"_": [9]},
                {"_": [1]},
            ],
            1,
        )
        actual = toAFN(postfix)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
