import abc
import unittest

import dice.rolling as rolling

class AbstractTest_Operand(abc.ABC):

    @abc.abstractmethod
    def setUp(self):
        pass

    @unittest.expectedFailure
    def test__get_values__return_unpacking(self):
        return_value = self.basic._get_values()
        with self.assertRaises(TypeError):
            used, unused = return_value

    def test__get_values__return_tuples(self):
        used, unused = self.basic._get_values()
        self.assertIsInstance(used, tuple)
        self.assertIsInstance(unused, tuple)

    def test__call__return_type(self):
        total = self.basic()
        self.assertIsInstance(total, int)
        total = self.basic(outcome=rolling.Outcome())
        self.assertIsInstance(total, int)
        total = self.basic(modifier=2)
        self.assertIsInstance(total, int)

    def test__call__outcome(self):
        outcome = rolling.Outcome()
        total = self.basic(outcome=outcome)
        self.assertEqual(1, len(outcome))

    def test__str__not_null(self):
        self.assertNotEqual("", str(self.basic))

