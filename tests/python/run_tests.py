#!/usr/bin/env python3

import argparse
import unittest

if "__main__" == __name__:
    Parser = argparse.ArgumentParser()
    Parser.add_argument("-v", action="count", dest="verbosity", default=1)
    args = Parser.parse_args()
    testsuite = unittest.defaultTestLoader.discover(".", pattern="test*.py")
    unittest.TextTestRunner(verbosity=args.verbosity).run(testsuite)

