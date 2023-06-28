import unittest

import dice.parsing as parsing

class TestDiceParser_DictPruning(unittest.TestCase):
    """Only tests to ensure unused formula parts are not in dict."""

    def setUp(self):
        self.r_d6     = parsing.DiceParser.Parse("d6")
        self.r_1d6    = parsing.DiceParser.Parse("1d6")
        self.r_d6dl   = parsing.DiceParser.Parse("d6dl")
        self.r_d6dl1  = parsing.DiceParser.Parse("d6dl1")
        self.r_1d6dl1 = parsing.DiceParser.Parse("1d6dl")
        self.all = [self.r_d6, self.r_1d6, self.r_d6dl, self.r_d6dl1, self.r_1d6dl1]
        self.expected_no_repeat = [self.r_d6, self.r_d6dl, self.r_d6dl1]
        self.expected_no_filter = [self.r_d6, self.r_1d6]
        self.expected_no_fcount = [self.r_d6, self.r_1d6, self.r_d6dl]

    def test_always_included(self):
        for roll in self.all:
            with self.subTest(roll=str(roll)):
                self.assertIn("type", self.r_d6)
                self.assertIn("sides", self.r_d6)

    def test_no_repeat(self):
        for roll in self.expected_no_repeat:
            with self.subTest(observed=str(roll)):
                self.assertNotIn("repeat", roll)

    def test_no_fstring(self):
        for roll in self.expected_no_filter:
            with self.subTest(observed=str(roll)):
                self.assertNotIn("fstring", roll)

    def test_no_fcount(self):
        for roll in self.expected_no_fcount:
            with self.subTest(observed=str(roll)):
                self.assertNotIn("fcount", roll)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class TestDiceParser_Filters(unittest.TestCase):

    def setUp(self):
        self.filters = ["dl", "dh", "kl", "kh"]
        self.bad_filters = ["da", "dz", "ka", "kz", "aa", "az", "za", "zz"]

    def test_expected_filters(self):
        for fstring in self.filters:
            with self.subTest(fstring=fstring):
                observed = parsing.DiceParser.Parse(f"2d20{fstring}1")
                self.assertEqual(fstring, observed["fstring"])

    def test_bad_filters(self):
        for fstring in self.bad_filters:
            with self.subTest(fstring=fstring):
                observed = parsing.DiceParser.Parse(f"2d20{fstring}1")
                self.assertNotIn("fstring", observed)
                self.assertNotIn("fcount", observed)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class TestDiceParser_MalformedFormulae(unittest.TestCase):

    def test_no_sides(self):
        no_repeat_formulae = ["d", "2d", "2ddl", "2ddh", "2ddl1", "2ddh1", "2dkl"]
        for formula in no_repeat_formulae:
            with self.subTest(formula=formula):
                with self.assertRaises(ValueError):
                    parsing.DiceParser.Parse(formula)



