import abc
import unittest

import dice.rolling as rolling

class AbstractTest_FilterFunc(abc.ABC):

    @abc.abstractmethod
    def setUp(self):
        pass

    def test__call(self):
        used, unused = self.func(self.basic_input, self.basic_count)
        self.assertEqual(self.expected_used, used)
        self.assertEqual(self.expected_unused, unused)

class Test_Filter_DropLowest(unittest.TestCase,AbstractTest_FilterFunc):

    def setUp(self):
        self.func = rolling.drop_lowest
        self.basic_input = (4, 6, 5, 1)
        self.basic_count = 2
        self.expected_used = (5, 6)
        self.expected_unused = (1, 4)

class Test_Filter_DropHighest(unittest.TestCase,AbstractTest_FilterFunc):

    def setUp(self):
        self.func = rolling.drop_highest
        self.basic_input = (20, 1)
        self.basic_count = 1
        self.expected_used = (1, )
        self.expected_unused = (20, )

class Test_Filter_KeepLowest(unittest.TestCase,AbstractTest_FilterFunc):

    def setUp(self):
        self.func = rolling.keep_highest
        self.basic_input = (94, 8, 40)
        self.basic_count = 1
        self.expected_used = (94, )
        self.expected_unused = (8, 40)

class Test_Filter_KeepHighest(unittest.TestCase,AbstractTest_FilterFunc):

    def setUp(self):
        self.func = rolling.keep_highest
        self.basic_input = (5, 4, 1, 2, 6, 3, 5, 4, 5, 2, 3, 6, 1, 1, 4, 1)
        self.basic_count = 8
        self.expected_used = (4, 4, 4, 5, 5, 5, 6, 6)
        self.expected_unused = (1, 1, 1, 1, 2, 2, 3, 3)

