import unittest
from shunYard import toPostFix

# All tests will be added to this file!

class TestShuntingYard(unittest.TestCase):
    def test_basic_example(self):
        infix = "a+b"
        expected = "ab+"
        actual = toPostFix(infix)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    # print(toPostFix)
    unittest.main()
