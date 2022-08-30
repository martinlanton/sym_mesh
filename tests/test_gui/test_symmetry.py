import unittest
from tests.fixtures import common


class TestSymmetry(common.BaseTest):
    def test_symmetry_no_base(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
