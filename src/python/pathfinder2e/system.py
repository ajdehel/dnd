import enum

class StrEnum(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

class Size(enum.Enum):
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    GARGANTUAN = 5

class Ability(StrEnum):
    STRENGTH = enum.auto()
    DEXTERITY = enum.auto()
    CONSTITUTION = enum.auto()
    INTELLIGENCE = enum.auto()
    WISDOM = enum.auto()
    CHARISMA = enum.auto()

class Proficiency(StrEnum):
    CLASSDC = enum.auto()
    PERCEPTION = enum.auto()
    LORE = enum.auto()

class Skill(StrEnum):
    ACROBATICS = enum.auto()
    ARCANA = enum.auto()
    ATHLETICS = enum.auto()
    CRAFTING = enum.auto()
    DECEPTION = enum.auto()
    DIPLOMACY = enum.auto()
    INTIMIDATION = enum.auto()
    MEDICINE = enum.auto()
    NATURE = enum.auto()
    OCCULTISM = enum.auto()
    PERFORMANCE = enum.auto()
    RELIGION = enum.auto()
    SOCIETY = enum.auto()
    STEALTH = enum.auto()
    SURVIVAL = enum.auto()
    THIEVERY = enum.auto()

class Save(StrEnum):
    FORTITUDE = enum.auto()
    REFLEX = enum.auto()
    WILL = enum.auto()

class ArmorType(StrEnum):
    HEAVY = enum.auto()
    MEDIUM = enum.auto()
    LIGHT = enum.auto()
    UNARMORED = enum.auto()

class WeaponType(StrEnum):
    ADVANCED = enum.auto()
    MARTIAL = enum.auto()
    SIMPLE = enum.auto()
    UNARMED = enum.auto()

class CastingTradition(StrEnum):
    ARCANE = enum.auto()
    DIVINE = enum.auto()
    OCCULT = enum.auto()
    PRIMAL = enum.auto()


STRENGTH_PROFICIENCIES = set((Skill.ATHLETICS,))
DEXTERITY_PROFICIENCIES = set((Save.REFLEX, Skill.ACROBATICS, Skill.STEALTH, Skill.THIEVERY))
CONSTITUTION_PROFICIENCIES = set((Save.FORTITUDE,))
INTELLIGENCE_PROFICIENCIES = set((Skill.ARCANA, Skill.CRAFTING, Skill.OCCULTISM, Skill.SOCIETY, Proficiency.LORE))
WISDOM_PROFICIENCIES = set((Proficiency.PERCEPTION, Save.WILL, Skill.MEDICINE, Skill.NATURE, Skill.RELIGION, Skill.SURVIVAL))
CHARISMA_PROFICIENCIES = set((Skill.DECEPTION, Skill.DIPLOMACY, Skill.INTIMIDATION, Skill.PERFORMANCE))

def get_ability(proficiency):
    ability_dict = {
        Ability.STRENGTH: STRENGTH_PROFICIENCIES,
        Ability.DEXTERITY: DEXTERITY_PROFICIENCIES,
        Ability.CONSTITUTION: CONSTITUTION_PROFICIENCIES,
        Ability.INTELLIGENCE: INTELLIGENCE_PROFICIENCIES,
        Ability.WISDOM: WISDOM_PROFICIENCIES,
        Ability.CHARISMA: CHARISMA_PROFICIENCIES}
    for ability, proficiencies in ability_dict.items():
        if proficiency in proficiencies:
            return ability
    return None
