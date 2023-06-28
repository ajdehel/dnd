from . import rolling

import re

####################################################################################################

def get_dice(formula_string):
    return FormulaParser(formula_string).get_formula()

####################################################################################################

class ParserTemplate:

    @classmethod
    def Parse(cls, string):
        match_ = cls.Regex.match(string)
        if match_ is None:
            raise ValueError(string)
        dict_ = match_.groupdict()
        dict_["type"] = cls.Type
        for key in list(dict_):
            if not dict_[key]:
                del dict_[key]
        return dict_

#= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class DiceParser(ParserTemplate):
    """Wrap handling of Dice Rolls in string formulas."""
    Regex = re.compile(r'(?P<repeat>\d*)d(?P<sides>\d+)((?P<fstring>(dl|dh|kl|kh))(?P<fcount>\d*)){0,1}(\[(?P<annotation>.*)\])?')
    Type  = "Operand"

class OperatorParser(ParserTemplate):
    """Wrap handling of Operators in string formulas."""
    Regex = re.compile(r'(?P<operator>[\+\-\*\/\(\)])')
    Type  = "Operator"

    @classmethod
    def Split(cls, string):
        string_ = cls.Regex.split(string)
        return string_

class ConstantParser(ParserTemplate):
    """Wrap handling of Constant Operands in string formulas."""
    Regex = re.compile(r'(?P<constant>\d+)(\[(?P<annotation>.*)\])?')
    Type  = "Operand"

####################################################################################################

class FormulaParser:

    def __init__(self, string_):
        self._string = string_
        string_ = re.sub("\s+", "", string_)
        list_   = OperatorParser.Split(string_)
        self._list = (self._ParseToken(token) for token in list_)

    @staticmethod
    def _ParseToken(token):
        parsers = [DiceParser, OperatorParser, ConstantParser]
        for ParserClass in parsers:
            try:
                dict_ = ParserClass.Parse(token)
                return dict_
            except (AttributeError, ValueError) as ex:
                pass
        else:
            raise RuntimeError(f"Could not parse {token}")

    @staticmethod
    def _Convert(op_dict):
        op_type = op_dict.pop("type")
        if "Operand" == op_type:
            return rolling.Operand.SubclassFactory(**op_dict)
        if "Operator" == op_type:
            return rolling.Operator.Get(**op_dict)

    def get_formula(self):
        infix = [ self._Convert(op_dict) for op_dict in self._list ]
        return rolling.Formula(infix)
