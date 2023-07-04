import functools
import json
import math

from . import system

from abc import ABC, abstractmethod

####################################################################################################
#   Sheets                                                                                         #
####################################################################################################

class Pathfinder2eSheet(ABC):

    @staticmethod
    def SubclassFactory(dict_data):
        if "info" in dict_data and "tags" in dict_data:
            return MonsterPf2ToolsSheet(dict_data)
        if "success" in dict_data and "build" in dict_data:
            return Pathbuilder2eSheet(dict_data)

    @staticmethod
    def ability_score_to_modifier(score):
        roundfunc = math.floor if score >= 10 else math.ceil
        return roundfunc((score - 10) / 2)

    @staticmethod
    def ability_modifier_to_score(modifier):
        return (modifier * 2) + 10

    def __init__(self, dict_data):
        self._contents = dict_data

    def __hash__(self):
        return hash(f"{self.name}{self.level}")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def level(self):
        pass

    @functools.cached_property
    def traits(self):
        return tuple(( trait.replace(" ","_").upper() for trait in self._traits ))

    @abstractmethod
    def get_ability_score(self, ability):
        pass

    @abstractmethod
    def get_ability_modifier(self, ability):
        pass

    @abstractmethod
    def get_bonus(self, prof):
        pass

    def get_dc(self, prof):
        return 10 + self.get_bonus(prof)

#===================================================================================================

class Pathbuilder2eSheet(Pathfinder2eSheet):

    @property
    def name(self):
        return self._contents['build']["name"].replace(" - ",".").replace(" ","-")

    @property
    def level(self):
        return self._contents['build']['level']

    @property
    def _traits(self):
        build_dict = self._contents['build']
        traits = [ build_dict['alignment'],
            system.Size(int(build_dict['size'])).name,
            build_dict['ancestry'], build_dict['heritage'],
            "humanoid" ]
        return traits

    @functools.cache
    def get_ability_score(self, ability):
        return self._contents['build']['abilities'][ability.value[0:3]]

    @functools.cache
    def get_ability_modifier(self, ability):
        return self.ability_score_to_modifier(self.get_ability_score(ability))

    @functools.singledispatchmethod
    @functools.cache
    def get_bonus(self, prof):
        prof_bonus = self._contents['build']['proficiencies'][prof.value]
        level_bonus = self.level if prof_bonus > 0 else 0
        return level_bonus + prof_bonus

    @get_bonus.register(system.Skill)
    @get_bonus.register(system.Save)
    def _(self, prof):
        prof_bonus = self._contents['build']['proficiencies'][prof.value]
        mod_bonus = self.get_ability_modifier(system.get_ability(prof))
        level_bonus = self.level if prof_bonus > 0 else 0
        return level_bonus + prof_bonus + mod_bonus

    def get_dc(self, prof):
        return 10 + self.get_bonus(prof)

#===================================================================================================

class MonsterPf2ToolsSheet(Pathfinder2eSheet):

    @functools.cached_property
    def name(self):
        return self._contents["name"].replace(" - ",".").replace(" ","-")

    @property
    def level(self):
        return self._contents["level"]

    @functools.cached_property
    def _traits(self):
        return self._contents["traits"].split(", ")

    def _get_value(self, enum_key):
        val = self._contents[enum_key.value]["value"]
        return int(val) if val else 0

    @functools.cache
    def get_ability_score(self, ability):
        return self.ability_modifier_to_score(self.get_ability_modifier(ability))

    @functools.cache
    def get_ability_modifier(self, ability):
        return self._get_value(ability)

    @functools.singledispatchmethod
    @functools.cache
    def get_bonus(self, prof):
        return self._get_value(prof)

    def get_dc(self, prof):
        return 10 + self.get_bonus(prof)

####################################################################################################
#   Groups                                                                                         #
####################################################################################################

