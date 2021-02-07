import pytz

from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple, UserDict
from datetime import datetime
from dateutil import parser as dateparser
from enum import Enum, auto
from html import unescape
from typing import Callable, List
from unidecode import unidecode

tz = pytz.timezone("US/Eastern")
Card = namedtuple("Card", ("title", "content"))
DINING_ENDPOINT = "https://dash.swarthmore.edu/dining_json"
TITLE_SYSTEM = "Menu"


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
            return Card(title, self["html_description"].strip())
        else:
            return Card(title, self["cleaned_description"])

    def ssml(self, dialect: SSMLDialect = SSMLDialect.DEFAULT):
        tr = f"from {' to '.join(self['short_time'].split(' - '))}"
        res = f"{self['title'].capitalize()} ({tr}) <break/>"
        # Logic imported from skill codebase
        # Todo: Clean this up when more complete test data is available
        t = (
            i.translate({ord("\t"): None})
            for i in self["cleaned_description"].strip().split("\n")
            if (i != "" and not i[0:3].lower() == "(v)")
        )
        t = (
            i.replace("(v)", "(vegan)").replace("$5.50", "for five dollars fifty")
            for i in t
        )
        res += "<break/>".join(t)
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
        return f"At {self.venue}<break/>" + "<break/>".join(
            [i.ssml(dialect=dialect) for i in self]
        )


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
            import requests

            data = requests.get(endpoint).json()
        for k, v in data.items():
            if isinstance(v, list):
                data[k] = SubmenuContainer(k, v)
            elif isinstance(v, dict):
                data[k] = Menu(data=v)
        super().__init__(data)

    @classmethod
    async def asynchronous(cls, endpoint: str = DINING_ENDPOINT):
        "Coroutine to asynchronously retrieve and instantiate a menu object. Used in python >= 3.6 concurrent (async/await) programs. If you don't know what this is you probably don't need it."
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                data = await resp.json()
        return cls(data=data)

    def __getitem__(self, item):
        if item in ("breakfast", "dinner"):
            return self.filter(lambda x: item in x["title"].lower())
        elif item == "lunch":
            return self.filter(
                lambda x: "unch" in x["title"].lower()
            )  # Hack to work around "brunch" on some days
        elif item == "current":
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
        return "<break/>".join((i.ssml(dialect=dialect) for i in self.containers))
