import unittest
from . import AbstractTest_Operand

import dice.rolling as rolling

class Test_Constant(unittest.TestCase,AbstractTest_Operand):

    def setUp(self):
        self.basic = rolling.Constant(5)
