import unittest
from minimizeAFD import minimize_afd
from shunYard import toPostFix
from regexpToAFN import toAFN, newAFN
from AFNToAFD import fromAFNToAFD

# All tests will be added to this file!


class TestShuntingYard(unittest.TestCase):
    def test_basic_example(self):
        infix = "ab"
        expected = "ab."
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        infix = "_+a*b"
        expected = "_a*b.+"
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        infix = "(0+1)*11(0+1)*"
        expected = "01+*1.1.01+*."
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        infix = "a(a+ab*)*"
        expected = "aaab*.+*."
        actual = toPostFix(infix)
        self.assertEqual(actual, expected) 

    def test_class_example(self):
        infix = "a*b*c*"
        expected = "a*b*.c*."
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)
    
    def test_class_example(self):
        infix = "0(0+1+2)*2"
        expected = "001+2+*.2."
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


class TestAFNToAFD(unittest.TestCase):
    def test_and_or_regexp(self):
        afn = newAFN(
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
        expected = {
            "accepted": [frozenset({1, 3, 4, 7}), frozenset({1, 5})],
            "transitions": {
                frozenset({0, 2, 6}): {"a": frozenset({1, 3, 4, 7})},
                frozenset({1, 3, 4, 7}): {"b": frozenset({1, 5})},
                frozenset({1, 5}): {},
            },
        }
        actual = fromAFNToAFD(afn)
        self.assertEqual(actual, expected)

    def test_class_example(self):
        self.maxDiff = None
        afn = newAFN(
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
        actual = fromAFNToAFD(afn)
        expected = {
            "accepted": [frozenset({0, 1, 2, 3, 4, 6, 8, 9}), frozenset({1, 7})],
            "transitions": {
                frozenset({0, 1, 2, 3, 4, 6, 8, 9}): {
                    "a": frozenset({3, 4, 5, 6}),
                    "b": frozenset({1, 7}),
                },
                frozenset({3, 4, 5, 6}): {
                    "a": frozenset({3, 4, 5, 6}),
                    "b": frozenset({1, 7}),
                },
                frozenset({1, 7}): {},
            },
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
