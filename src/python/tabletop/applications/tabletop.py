from . import Application

import argparse
import pathlib

from tabletop.controller import TermController

class TabletopTerminalApplication(Application):

    Parser = argparse.ArgumentParser("tabletop")
    Parser.add_argument("-s", "--session", dest="sessions", nargs="+", type=pathlib.Path, required=False, default=list())

    def __init__(self, args):
        self.args = args
        self.factory = self.get_factory()
        model = self.factory.Get_Model()
        for session in self.args.sessions:
            model.load_session(session)
        command_loader = self.factory.Get_CommandLoader()
        config = self.factory.Get_Config()
        self.controller = TermController(model, command_loader, **config)

    def get_factory(self):
        import pathfinder2e
        return pathfinder2e.Factory()

    def __call__(self):
        self.controller()
