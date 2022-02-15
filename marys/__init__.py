import aiohttp
import pytz
import re
import requests

from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple, UserDict
from datetime import datetime
from dateutil import parser as dateparser
from enum import Enum, auto
from html import escape, unescape
from html.parser import HTMLParser
from typing import Callable, List
from unidecode import unidecode

"""Marys Python library
Copyright 2021–2022 Bill Dengler

Licensed under the Apache License, Version 2.0 (the "Licence");
you may not use this file except in compliance with the Licence.
You may obtain a copy of the Licence at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and
limitations under the Licence.
If the terms of the licence pose serious difficulty for your use, please contact the author.
"""

__version__ = "1.1.0"
tz = pytz.timezone("US/Eastern")
Card = namedtuple("Card", ("title", "content"))
DINING_ENDPOINT = "https://dash.swarthmore.edu/dining_json"
TITLE_SYSTEM = "Menu"
HTTP_HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; python-marys/{__version__}; +https://github.com/codeofdusk/marys)"
}

diet_expr = re.compile("::(.*?)::")


class SSMLDialect(Enum):
    """
    An enumeration of particular varieties of Speech Synthesis Markup Language.
    SSMLDialect.DEFAULT is standard SSML.
    SSMLDialect.AMAZON adds support for custom Amazon Alexa extensions.
    """

    DEFAULT = auto()
    AMAZON = auto()


def _sad_speech(msg: str, dialect: SSMLDialect = SSMLDialect.DEFAULT):
    "Marks the passed-in speech as disappointed where supported by the SSMLDialect."
    if dialect == SSMLDialect.AMAZON:
        return f'<amazon:emotion name="disappointed" intensity="medium">{msg}</amazon:emotion>'
    else:
        return msg


class _HTMLToSSMLConverter(HTMLParser):
    "Internal utility class to assist with HTML -> SSML conversions."

    def __init__(self, *args, **kwargs):
        self.data = ""
        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, *args):
        if tag == "br":
            self.data += '<break strength="weak"/>'

    def handle_endtag(self, tag):
        if tag == "li":
            self.data += '<break strength="weak"/>'

    def handle_data(self, data):
        self.data += data

    def handle_entityref(self, ref):
        if ref == "nbsp":
            # Amazon Alexa (and maybe others) don't like these.
            self.data += " "
        else:
            self.data += f"&{ref};"

    def handle_charref(self, ref):
        return self.handle_entityref(ref)


class MenuBase(ABC):
    "An abstract class specifying the common interface implemented by all externally-facing objects in this library."

    def __str__(self):
        return "\n".join(self.card(html=False))

    @property
    @abstractmethod
    def open(self) -> bool:
        "Returns whether this dining venue is open. If this object contains multiple venues, returns if one of them is open."
        raise NotImplementedError

    @abstractmethod
    def card(self, html: bool = False) -> Card:
        "Returns a Card (title and content) for an object. These are useful in, for example, text displays for voice assistants or titles/contents of message boxes in graphical programs."
        raise NotImplementedError

    @abstractmethod
    def ssml(self, dialect: SSMLDialect = SSMLDialect.DEFAULT) -> str:
        "Returns Speech Synthesis Markup Language (SSML) for an object, for example to be spoken by a voice assistant."
        raise NotImplementedError


class Submenu(MenuBase, dict):
    "The hours and available meals at a given dining venue and time (such as the Sharples dinner menu)."

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container
        self.start = tz.localize(dateparser.parse(self["startdate"]))
        self.end = tz.localize(dateparser.parse(self["enddate"]))
        if "description" in self:
            self["cleaned_description"] = (
                unidecode(unescape(self["description"])).replace("\r\n", "\n").strip()
            )

    def __repr__(self):
        return f"{self.container.venue} {self['title']} {super().__repr__()}"

    @property
    def open(self):
        now = datetime.now(tz)
        return now >= self.start and now < self.end

    def card(self, html=False):
        title = f"{self['title']} ({self.start.strftime('%H:%M')}–{self.end.strftime('%H:%M')})"
        if html:
            content = (
                self["html_description"]
                .strip()
                .replace("<html-blob>", "")
                .replace("</html-blob>", "")
            )
        else:
            content = self["cleaned_description"]
        content = diet_expr.sub("(\\1)", content)
        return Card(title, content)

    def ssml(self, dialect: SSMLDialect = SSMLDialect.DEFAULT):
        tr = f"from {' to '.join(self['short_time'].split(' - '))}"
        res = f"{escape(self['title']).capitalize()} ({tr}) <break strength=\"weak\"/>"
        p = _HTMLToSSMLConverter(convert_charrefs=False)
        p.feed(self["html_description"])
        res += p.data
        return res


class SubmenuContainer(MenuBase, list):
    "A list of Submenu objects for a given dining venue (such as lunch and dinner at Sharples on a given day)."

    def __init__(self, venue, raw_list):
        self._venue = venue
        lst = [Submenu(self, rsm) for rsm in raw_list]
        super().__init__(lst)

    def __repr__(self):
        return f"{self.venue} {super().__repr__()}"

    @property
    def venue(self) -> str:
        "The human-readable name of the dining venue to which this object refers."
        API_TO_FRIENDLY = {
            "sharples": "Sharples Dining Hall",
            "essies": "Essie Mae's",
            "kohlberg": "Kohlberg coffee bar",
            "science_center": "Science Center coffee bar",
        }
        if self._venue in API_TO_FRIENDLY:
            return API_TO_FRIENDLY[self._venue]
        else:
            return self._venue

    @property
    def open(self):
        return any((i.open for i in self))

    def card(self, html=False):
        content = ""
        for sm in self:
            card = sm.card(html=html)
            if html:
                text = f"<h3>{card.title}</h3><p>{card.content}</p>\n"
            else:
                text = f"{card.title}\n{card.content}\n"
            content += text
        title = f"At {self.venue}"
        if not content or content.isspace():
            title = TITLE_SYSTEM
            content = f"{self.venue} is currently unavailable!"
        return Card(title, content)

    def ssml(self, dialect: SSMLDialect = SSMLDialect.DEFAULT):
        if not self:
            return _sad_speech(f"{self.venue} is currently unavailable!", dialect)
        res = '<break strength="weak"/>'.join([i.ssml(dialect=dialect) for i in self])
        if not self[0]["title"].lower().endswith("open"):
            # We need to say the venue first, as it's probably not in the title
            # of its first submenu.
            res = f'At {self.venue}<break strength="weak"/>' + res
        return res


class Menu(MenuBase, UserDict):
    "A root menu object, containing all dining locations with hours and meal times. Roughly analogous to a response from the API. You'll probably want to instantiate one of these as an entry point."

    EMPTY_MSG = "Dining is currently unavailable at this time!"

    def __init__(self, data: dict = None, endpoint: str = DINING_ENDPOINT):
        """
        Instantiates a Menu object.
        data: a raw dictionary containing retrieved json data from the API. If unspecified, retrieve this data synchronously from endpoint.
        endpoint: the URL from where to retrieve json data. Defaults to The Dash.
        """
        if data is None:
            # Retrieve menu synchronously
            resp = requests.get(endpoint, headers=HTTP_HEADERS)
            resp.raise_for_status()
            data = resp.json()
        for k, v in data.items():
            if isinstance(v, list):
                data[k] = SubmenuContainer(k, v)
            elif isinstance(v, dict):
                data[k] = Menu(data=v)
        super().__init__(data)

    @classmethod
    async def asynchronous(cls, endpoint: str = DINING_ENDPOINT):
        "Coroutine to asynchronously retrieve and instantiate a menu object. Used in python >= 3.6 concurrent (async/await) programs. If you don't know what this is you probably don't need it."
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=HTTP_HEADERS) as resp:
                data = await resp.json()
        return cls(data=data)

    def __getitem__(self, item):
        if item in ("breakfast", "dinner"):
            return self.filter(lambda x: item in x["title"].lower())
        elif item == "lunch":
            return self.filter(
                lambda x: "unch" in x["title"].lower()
            )  # Hack to work around "brunch" on some days
        elif item == "now":
            now = datetime.now(tz)
            return self.filter(lambda x: x.start <= now <= x.end) or self.filter(
                lambda x: now < x.end
            )
        elif item == "current":
            # In older iterations of the API, "open door" was unlisted
            # so it made more sense to provide both menus on now and up next.
            # New users going forward probably want "now", but keeping this
            # for backwards compat/if it's useful for some situations.
            now = datetime.now(tz)
            return self.filter(lambda x: now < x.end)
        else:
            return super().__getitem__(item)

    def __str__(self):
        "Override of MenuBase.__str__ that just returns the card content in menus with multiple containers, as the card title conveys no useful information."
        if len(self.containers) == 1:
            return super().__str__()
        else:
            return self.card(html=False).content

    def filter(self, func: Callable):
        "From a Menu, returns a new Menu containing all SubmenuContainer objects for which the passed-in func returns True."
        res = defaultdict(list)
        for k, v in self.data.items():
            if isinstance(v, SubmenuContainer):
                for sm in v:
                    if func(sm):
                        res[k].append(sm)
        return Menu(data=res)

    @property
    def containers(self) -> List[SubmenuContainer]:
        "Returns all non-empty submenu containers in this menu."
        return [i for i in self.values() if i and isinstance(i, SubmenuContainer)]

    @property
    def open(self):
        return any((i.open for i in self.containers))

    def card(self, html=False):
        if len(self.containers) == 1:
            return self.containers[0].card(
                html=html
            )  # Fall back to the container-level method for nicer presentation
        if not self:
            return Card(TITLE_SYSTEM, Menu.EMPTY_MSG)
        content = ""
        for i in self.containers:
            c = i.card(html=html)
            if html:
                content += f"<h2>{c.title}</h2>{c.content}\n"
            else:
                content += f"{c.title}\n{c.content}\n"
        return Card(TITLE_SYSTEM, content)

    def ssml(self, dialect: SSMLDialect = SSMLDialect.DEFAULT):
        if not self:
            return _sad_speech(Menu.EMPTY_MSG, dialect)
        return '<break strength="weak"/>'.join(
            (i.ssml(dialect=dialect) for i in self.containers)
        )
