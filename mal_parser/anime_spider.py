from http import HTTPStatus
from typing import List, Tuple

from .anime import AnimeParser
from .manga import MangaParser
from .spider import AbstractAsyncSpider
from .top import AnimeTopParser

MANGA_ID_OFFSET = 1000000


class AnimeTopSpider(AbstractAsyncSpider):
    def __init__(self, loop, limit=None, session=None):
        super().__init__(loop, limit, session)
        self.iterator = iter(range(0, 100000, 50))
        self.url_format = 'https://myanimelist.net/topanime.php?limit={}'

    async def get_next_url(self):
        return self.url_format.format(next(self.iterator))

    def parser(self, url, status, html):
        return AnimeTopParser(url, html).parse()

    async def save_result(self, parsed_data: List[Tuple[int, str, float]]):
        pass


class MangaTopSpider(AnimeTopSpider):
    def __init__(self, loop, limit=None, session=None):
        super().__init__(loop, limit, session)
        self.url_format = 'https://myanimelist.net/topmanga.php?limit={}'

    async def save_result(self, parsed_data: List[Tuple[int, str, float]]):
        pass


class AnimeMangaSpider(AbstractAsyncSpider):
    relation_rename = {
        "alternative version": "alv",
        "alternative setting": "als",
        "adaptation": "ada",
        "character": "cha",
        "full story": "ful",
        "other": "oth",
        "prequel": "pre",
        "parent story": "par",
        "sequel": "seq",
        "spin-off": "spi",
        "side story": "sid",
        "summary": "sum",
    }

    def __init__(self, loop, limit=None, session=None):
        super().__init__(loop, limit, session)
        self.anime_format = 'https://myanimelist.net/anime/{}'
        self.manga_format = 'https://myanimelist.net/manga/{}'

        self.processing_ids = set()
        self.anime_types = ["TV", "Movie", "OVA", "Special", "ONA", "Music"]
        self.manga_types = ["Doujinshi", "Manhwa", "Manhua", "Novel", "One-shot", "Manga"]

    async def get_next_url(self):
        pass

    def parser(self, url, status, html):
        type, id = url.split('/')[3:5]
        if status == HTTPStatus.NOT_FOUND:
            return {'errors': 'not_found', 'id': int(id), 'type': type}
        else:
            if type == 'anime':
                return AnimeParser(url, html).parse()
            else:
                return MangaParser(url, html).parse()

    async def save_result(self, parsed_data: List[Tuple[int, str, float]]):
        pass
