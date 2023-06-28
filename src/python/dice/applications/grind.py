from . import Application
import dice

import argparse
import multiprocessing as mp

class Grind(Application):

    Parser = argparse.ArgumentParser("grind")
    Parser.add_argument("dice", type=str, nargs="+")
    Parser.add_argument("-v", dest="verbosity", action="count")
    Parser.add_argument("-n", dest="count", type=int, default=1, required=True)
    Parser.add_argument("-t", dest="threads", type=int, default=1)

    def __init__(self, args):
        self.args = args
        self.formula = None

    def __call__(self):
        dice_str = " ".join(self.args.dice)
        dice_obj = dice.get_dice(dice_str)
        process = self.Process(dice_obj)
        quot = self.args.count // self.args.threads
        assignments = [quot for idx in range(self.args.threads)]
        if rem := self.args.count % self.args.threads:
            print(rem)
            assignments.append(rem)
        print(assignments)
        with mp.Pool(processes=self.args.threads) as pool:
            total = sum(pool.map(process, assignments))
            print(total / self.args.count)

    class Process:

        def __init__(self, dice):
            self.dice = dice

        def __call__(self, num):
            return sum([self.dice() for idx in range(num)])

