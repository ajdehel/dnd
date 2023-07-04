from .models import Pathfinder2eModel
from . import commands

from tabletop.commands import CommandLoader

class Factory:

    @classmethod
    def Get_Model(cls):
        return Pathfinder2eModel()

    @classmethod
    def Get_CommandLoader(cls):
        return CommandLoader(commands)

    def Get_Config(cls):
        return dict()
