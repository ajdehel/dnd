import abc
import random
import collections

####################################################################################################

class Outcome:
    """Simplifies collection of the results of random dice selections."""

    def __init__(self):
        self._segments = dict()

    def append(self, operand, used, unused=list(), modifier=1, annotation=""):
        self._segments[str(operand)] = {
            "used": used, "unused": unused, "modifier": int(modifier), "annotation": annotation}

    def __str__(self):
        return " + ".join(self._segment_strings()) if self._segments else ""

    def _segment_strings(self):
        for segment in self._segments.values():
            segment_total = sum(segment['used'])
            used_str = "+".join(( str(v) for v in segment['used'] )) if segment['used'] else ""
            unused_str = "/" + ",".join(( str(v) for v in segment['unused'] )) if segment['unused'] else ""
            values_str = f"({used_str}{unused_str})" if used_str or unused_str else ""
            annotation_str = f"[{segment['annotation']}]" if segment['annotation'] else ""
            yield f"{segment_total}{annotation_str}{values_str}"

    def __len__(self):
        return len(self._segments)

    @property
    def total(self):
        return 0 + sum(( sum(d["used"])*d["modifier"] for d in self._segments.values() ))

####################################################################################################

class Operand(abc.ABC):

    def SubclassFactory(*, constant=None, sides=None, fstring=None, **kwargs):
        if constant:
            return Constant(constant, **kwargs)
        if sides:
            return Roll(sides, fstring, **kwargs) if fstring else Dice(sides, **kwargs)

    def __init__(self, annotation="", modifier=1):
        self.annotation = annotation
        self.modifier = int(modifier)

    def __call__(self, outcome=None, modifier=None):
        used, unused = self._get_values()
        modifier = int(modifier) if modifier else self.modifier
        if outcome is not None:
            outcome.append(str(self), used, unused, modifier, self.annotation)
        return sum(used) * modifier

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def _get_values(self):
        pass


#===================================================================================================

class Constant(Operand):

    def __init__(self, value, annotation=None):
        super().__init__(annotation)
        self.value = int(value)

    def _get_values(self):
        return (self.value,), tuple()

    def __str__(self):
        annotation_str = f"[{self.annotation}]" if self.annotation else ""
        return f"{self.value}{annotation_str}"

#===================================================================================================

class Dice(Operand):
    """Simplifies the sample space for a die and add ability to repeat."""

    def __init__(self, sides, repeat=1, annotation=None):
        super().__init__(annotation)
        self._sides = int(sides)
        self._repeat = int(repeat)
        self._range = range(1, self._sides+1)

    def _get_values(self):
        values = tuple(sorted(( random.choice(self._range) for x in range(self._repeat) )))
        return values, tuple()

    def __str__(self):
        num_str = "" if 1 == self._repeat else self._repeat
        annotation_str = f"[{self.annotation}]" if self.annotation else ""
        return f"{num_str}d{self._sides}{annotation_str}"

#===================================================================================================

class Roll(Operand):
    """Combines Dice with the ability to filter their outcomes."""

    def __init__(self, sides, fstring, repeat=1, fcount=1, annotation=None, modifier=1):
        super().__init__(annotation)
        self._dice = Dice(int(sides), int(repeat))
        self._filter = Filter.Get(fstring, int(fcount))
        self.annotation = annotation

    def _get_values(self, outcome=None):
        used, _ = self._dice._get_values()
        return self._filter(used)

    def __str__(self):
        annotation_str = f"[{self.annotation}]" if self.annotation else ""
        return f"{self._dice}{self._filter}{annotation_str}"

#===================================================================================================

class Formula:
    """Combine rolls into a single outcome."""

    @classmethod
    def To_Postfix(cls, infix_list):
        """Convert a list representing an infix expression to a postfix one."""
        stack = collections.deque()
        postfix = list()
        for op in infix_list:
            if isinstance(op, Operator):
                while stack and op.precedence <= stack[-1].precedence:
                    postfix.append(stack.pop())
                stack.append(op)
            else:
                postfix.append(op)
        while stack:
            postfix.append(stack.pop())
        return postfix

    def __init__(self, infix_list, annotation=None):
        self._infix = infix_list
        self._postfix = self.To_Postfix(self._infix)

    def __call__(self, outcome=None):
        return self.evaluate_postfix(self._postfix, outcome)

    @staticmethod
    def evaluate_postfix(postfix, outcome):
        operands = list()
        for op in postfix:
            if isinstance(op, Operator):
                rhs = operands.pop()
                lhs = operands.pop()
                operands.append(op(lhs, rhs))
            else:
                value = op(outcome)
                operands.append(value)
        return operands[0]

    def __str__(self):
        infix_str = ' '.join([str(op) for op in self._infix])
        annotation_str = f"[{self.annotation}]" if self.annotation else ""
        return "({infix_str}){annotation_str}"

####################################################################################################

class Filter:

    _Dict = dict()

    class _Decorator:
        """Simple class Decorator to simplify Filter.Register()"""

        def __init__(self, fstring):
            self._fstring = fstring
            self._ffunc = None

        def __call__(self, func):
            Filter._Dict[self._fstring] = func
            return func

    @classmethod
    def Register(cls, fstring):
        """Decorator to make external function accessible via Filter class."""
        """  Registered functions can be looked up by fstring in Filter.Get()"""
        return cls._Decorator(fstring)

    @classmethod
    def Get(cls, fstring, fcount):
        return cls(fstring, cls._Dict[fstring], fcount)

    #-----------------------------------------------------------------------------------------------

    def __init__(self, fstring, ffunc, fcount):
        self._fstring = fstring
        self._ffunc= ffunc
        self._fcount = fcount

    def __call__(self, values):
        return self._ffunc(values, self._fcount)

    def __str__(self):
        count_str = "" if 1 == self._fcount else self._fcount
        return f"{self._fstring}{count_str}"

@Filter.Register("dl")
def drop_lowest(values, count):
    values = sorted(values)
    return tuple(values[count:]), tuple(values[:count])

@Filter.Register("dh")
def drop_highest(values, count):
    values = sorted(values)
    return tuple(values[:0-count]), tuple(values[0-count:])

@Filter.Register("kl")
def keep_lowest(values, count):
    values = sorted(values)
    return tuple(values[:count]), tuple(values[count:])

@Filter.Register("kh")
def keep_highest(values, count):
    values = sorted(values)
    return tuple(values[0-count:]), tuple(values[:0-count])

####################################################################################################

class Operator:

    _Dict = dict()

    @classmethod
    def Capture(cls, opstring, precedence):
        """Decorator to envelope operation function into Operator class."""
        """  A captured function can be retrieved via opstring by calls to Get()"""
        operator = cls(opstring, precedence)
        cls._Dict[opstring] = operator
        return operator._decorate

    @classmethod
    def Get(cls, *, operator):
        return cls._Dict[operator]

    def __init__(self, opstring, precedence):
        self._opstring = opstring
        self.precedence = precedence
        self._func = None

    def _decorate(self, func):
        self._func = func
        return self

    def __call__(self, lhs, rhs):
        return self._func(lhs, rhs)

    def __eq__(lhself, rhs):
        return lhself._opstring == rhs._opstring

    def __str__(self):
        return self._opstring

@Operator.Capture("+", 0)
def add(lhs, rhs):
    return lhs + rhs

@Operator.Capture("-", 0)
def sub(lhs, rhs):
    return lhs - rhs

@Operator.Capture("*", 1)
def mul(lhs, rhs):
    return lhs * rhs

@Operator.Capture("/", 1)
def div(lhs, rhs):
    return lhs // rhs

