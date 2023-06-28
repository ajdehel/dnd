import unittest
from . import AbstractTest_Operand

import dice.rolling as rolling

class Test_Roll(unittest.TestCase,AbstractTest_Operand):

    def setUp(self):
        self.basic = rolling.Roll(20, 'dl')

