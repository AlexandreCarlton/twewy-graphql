from dataclasses import dataclass
from enum import Enum
import re
from typing import Dict, List, Optional

import mwparserfromhell as mw

# TODO: Need:
# Noise
#   pin drops (noise -> pin)
# Threads
# shops (Shop List)?
# Days (to get noise locations)

HTML_COMMENT = re.compile("<!--.*?-->")

class TemplateBox:
    """Abstract class to facilitate value extraction from templates."""

    def _get_value(self, name: str, func=str) -> Optional[str]:
        if self._template.has(name):
            value = str(self._template.get(name).value)
            value = re.sub(HTML_COMMENT, "", value)
            return func(value.strip())
        return None


# TODO: Should be in a fandom package - for parsing this.
@dataclass
class PinBox(TemplateBox):
    """
    A wrapper around the 'Pin box' template that exposes and sanitises
    special fields.
    """

    def __init__(self, template: mw.nodes.template.Template):
        self._template = template

    def __str__(self) -> str:
        return f'Pin {self.number:03}'

    @property
    def number(self) -> int:
        return int(self._template.get('Number').value.strip())

    @property
    def name(self) -> str:
        return self._template.get('Name').value.strip()

    @property
    def brand(self) -> str:
        return self._template.get('Brand').value.strip()

    @property
    def bpp_yields(self) -> Optional[int]:
        return self._pp_yields('BPP')

    @property
    def sdpp_yields(self) -> Optional[int]:
        return self._pp_yields('SDPP')

    @property
    def mpp_yields(self) -> Optional[int]:
        return self._pp_yields('MPP')

    def _pp_yields(self, type) -> Optional[int]:
        yields = self._get_value(f'{type} yields')
        if yields is None or yields == 'M':
            return None
        return int(yields)

@dataclass
class Resistance(object):

    positive: int
    negative: int

class Difficulty(Enum):

    ULTIMATE = 'U'
    HARD = 'H'
    NORMAL = 'N'
    EASY = 'E'

@dataclass
class NoiseInfobox(TemplateBox):
    """
    A wrapper around the 'Infobox Noise' templates that exposes and sanitises
    special fields.
    """

    def __init__(self, template: mw.nodes.template.Template):
        self._template = template

    def __str__(self) -> str:
        return f'Noise {self.number:03}'

    @property
    def number(self) -> int:
        return self._get_value('nbr', int)

    @property
    def name(self) -> str:
        return self._get_value('name')

    @property
    def hit_points(self) -> int:
        return self._get_value('hp', int)

    @property
    def attack(self) -> int:
        return self._get_value('attack', int)

    @property
    def pin_points(self) -> int:
        return self._get_value('pp', int)

    @property
    def experience(self) -> int:
        return self._get_value('exp', int)

    @property
    def drops(self) -> Dict[Difficulty, int]: # int is the pin number
        # look at pindrops
        # We have to split by <br>, then grab the '''U''' (may not be in that text) and the wikilink.
        return {}
