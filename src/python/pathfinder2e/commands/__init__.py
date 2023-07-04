import abc
import argparse

from tabletop.commands import TermCommand

# Import all commands present in this directory

def load():
    import pathlib
    import importlib
    path = pathlib.Path(__file__).parent
    cmd_modules = [ f for f in path.glob("*.py") if str(f) != __file__ ]
    for module in cmd_modules:
        modname = module.stem
        importlib.import_module(f".{modname}", __package__)
        modobj = globals().get(modname)
        for attr in dir(modobj):
            obj = getattr(modobj, attr)
            if isinstance(obj, type) and issubclass(obj, TermCommand) and obj != TermCommand:
                globals()[attr] = obj



load()
del load
del TermCommand
