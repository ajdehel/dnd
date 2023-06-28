import unittest
from . import AbstractTest_Operand

import dice.rolling as rolling

class Test_Dice(unittest.TestCase,AbstractTest_Operand):

    def setUp(self):
        self.basic = rolling.Dice(6)

