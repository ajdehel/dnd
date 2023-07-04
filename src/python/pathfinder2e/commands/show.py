"""List sheets loaded into the model."""
import argparse
import os

from math import floor, ceil

from tabletop.commands import TermCommand

class show(TermCommand):

    Parser = argparse.ArgumentParser("show", exit_on_error=False)
    Parser.add_argument("item", nargs="*")

    def autocomplete(self, text, line, begidx, endidx):
        return self.model_complete(text, line, begidx, endidx)

    def handle(self, args):
        tokens = sorted([ item for item in self.model
                          if not args.item or item in args.item ])
        emit_matrix(tokens)

####################################################################################################
#   Util Functions
####################################################################################################

import os
from math import floor, ceil

def transpose(matrix):
    return map(list, zip(*matrix))

def emit_matrix(tokens, width=os.get_terminal_size().columns):
    max_len = max(map(len, tokens)) + 2
    num_cols = min(width // max_len, len(tokens))
    num_rows = ceil(len(tokens) / num_cols)
    while len(tokens) < num_rows * num_cols:
        tokens.append("")
    matrix = list()
    while tokens:
        matrix.append(tokens[:num_rows])
        tokens = tokens[num_rows:]
    for row in transpose(matrix):
        for cell in row:
            print(f"{cell:{max_len}}", end=" ")
        print()
