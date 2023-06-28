import unittest

import dice.rolling as rolling

class Test_empty(unittest.TestCase):

    def setUp(self):
        self.outcome = rolling.Outcome()

    def test__str(self):
        self.assertEqual("", str(self.outcome))

    def test__total(self):
        self.assertEqual(0, self.outcome.total)
