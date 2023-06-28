from . import Application
import dice.rolling

import argparse

class Roll(Application):

    Parser = argparse.ArgumentParser("roll")
    Parser.add_argument("formula", type=str)
    Parser.add_argument("-v", dest="verbosity", action="count")
    Parser.add_argument("-n", dest="count", type=int, default=1)

    def __init__(self, args):
        self.args = args
        self.dice_obj = dice.get_dice(self.args.formula)

    def __call__(self):
        for _ in range(self.args.count):
            outcome = dice.rolling.Outcome()
            total = self.dice_obj(outcome)
            print(outcome)

