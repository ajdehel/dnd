import abc
import cmd
import pathlib
import sys
import traceback

from . import TermCommand

class TermController(cmd.Cmd, abc.ABC):

    def __init__(self, model, command_loader, intro='ttrpg', prompt='(ttrpg)'):
        self.model = model
        self.prompt = prompt
        self.intro = intro
        self.panic = 0
        self._commands = list()
        self.load_commands(command_loader.link(model))
        super().__init__()

    def __call__(self):
        self.cmdloop()

    #=====================================================================================
    #   Cmd overrides
    #=====================================================================================

    def cmdloop(self, intro=None):
        print(self.intro)
        while True:
            try:
                super().cmdloop("")
            except KeyboardInterrupt:
                msg="\nUse exit or quit." if self.panic >= 3 else ""
                print(msg)
                self.panic += 1

    def onecmd(self, arg):
        try:
            super().onecmd(arg)
        except RuntimeError as e:
            print(f"{shlex.split(self.lastcmd)[0]}: {e.args[0]}")
        except Exception:
            traceback.print_exc()
        self.panic = 0

    def emptyline(self):
        return ""

    def completedefault(self, text, line, begidx, endidx):
        args, results = setup_complete(line)
        target = args[-1]
        if len(args) > 1:
            return results
        if 0 == len(args):
            return self.commands
        if 1 == len(args):
            return [ c for c in self.commands if c.startswith(target) ]

    #=====================================================================================
    #   helper methods
    #=====================================================================================

    @property
    def commands(self):
        return [ m[3:] for m in dir(self) if m.__name__.startswith("do_") ]

    #=====================================================================================
    #   Load Commands
    #=====================================================================================

    @classmethod
    def load_commands(cls, commands):
        for command in commands:
            setattr(cls, f"do_{command.name}", command.get_do_method())
            setattr(cls, f"help_{command.name}", command.get_helpme_method())
            setattr(cls, f"complete_{command.name}", command.get_complete_method())

    # exit/quit
    def do_exit(self, arg):
        """Exit the Application."""
        exit(0)

    #===============================================================================================
    # Complete Functions
    def model_complete(self, text, line, begidx, endidx):
        args, results = setup_complete(line)
        target = args[-1]
        if 1 == len(args):
            return [ sheet.name for sheet in self.model.list() ]
        for sheet in self.model.list():
            if sheet.name.startswith(target):
                results.append(sheet.name)
        return results

    def path_complete(self, text, line, begidx, endidx):
        args, results = setup_complete(line)
        pwd = pathlib.Path.cwd()
        target = args[-1]
        if 1 == len(args):
            return [ path.name for path in pwd.iterdir() ]
        path = pathlib.Path(target).expanduser()
        globpath = path.parent
        glob = f"{path.name}*"
        if not text:
            globpath = path
            glob = "*"
        results.extend([format_autocomplete_file(p) for p in globpath.glob(f"{glob}")])
        return results

    #===============================================================================================
    # Aliases
    do_quit = do_exit
