import abc
import functools
import shlex

####################################################################################################
#   Abstract Classes
####################################################################################################

class TermCommand:

    #=====================================================================================
    #   Abstract Members
    #=====================================================================================

    @abc.abstractmethod
    def handle(self, args):
        pass

    @abc.abstractmethod
    def autocomplete(self, text, line, begidx, endidx):
        pass

    #=====================================================================================
    #   Concrete Members
    #=====================================================================================

    def __init__(self, model):
        self.model = model

    def __call__(self, line):
        args = self.parse(line)
        return self.handle(args)

    def helpme(self):
        return self.Parser.print_help()

    def parse(self, line):
        tokens = self.splitline(line)
        return self.Parser.parse_args(tokens)

    @property
    def name(self):
        return str(self.__class__.__qualname__)

    @staticmethod
    def splitline(line):
        return shlex.split(line)

    def model_complete(self, text, line, begidx, endidx):
        args = self.splitline(line)
        target = args[-1]
        if 1 == len(args):
            return list(self.model)
        return list(self.model.search(target))

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

    def system_complete(self, text, line, begidx, endidx):
        pass

    #=====================================================================================
    #   Decorators
    #=====================================================================================

    def get_do_method(self):
        @functools.wraps(self.handle)
        def wrapper(_, line):
            return self(line)
        return wrapper

    def get_complete_method(self):
        @functools.wraps(self.autocomplete)
        def wrapper(_, text, line, begidx, endidx):
            return self.autocomplete(text, line, begidx, endidx)
        return wrapper

    def get_helpme_method(self):
        @functools.wraps(self.helpme)
        def wrapper(_):
            return self.helpme()
        return wrapper

####################################################################################################
#   Command Loader
####################################################################################################

class CommandLoader:

    def __init__(self, *command_modules, model=None):
        self.commands = list()
        for command_module in command_modules:
            self._get_commands(command_module)
        self.model = model

    def _get_commands(self, module):
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, TermCommand):
                self.commands.append(obj)

    def link(self, model):
        yield from ( command(model) for command in self)

    def __iter__(self):
        yield from self.commands

