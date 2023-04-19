import aiohttp
from .errors import ConfigUnfinishedError, WrongOrderTypeException, RequestException


class E621Post(object):
    def __init__(self, svc, id, sample_pic, origin_pic, preview) -> None:
        self.svc = svc
        self.id = id
        self.sample_pic = sample_pic
        self.origin_pic = origin_pic
        self.preview = preview


class SearchFilter(object):
    def __init__(self) -> None:
        self.tags = ''
        self._limit = 1
        self._rating = 's'
        self._score = 0
        self._order = 'new'

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if value not in ['new', 'score', 'random']:
            raise WrongOrderTypeException()
        self._order = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value not in ['s', 'q', 'e']:
            self._rating = 's'
        self._rating = value

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        value = 5 if value > 5 else value
        value = 1 if value < 1 else value
        self._limit = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        value = 50 if value > 50 else value
        value = 0 if value < 0 else value
        self._score = value


class E621Service(object):
    def __init__(self, e621_account: str, e621_api_key: str, log, proxy: str) -> None:
        self.log = log
        
        self.proxy = proxy
        if not e621_account or not e621_api_key:
            raise ConfigUnfinishedError()

        self.default_header = {
            "User-Agent": "OrcasE621Bot/0.1(Orcas)",
            "login": e621_account,
            "api_key": e621_api_key
        }
        self.base_url = "https://e621.net"

    def _new_sesson(self, header: dict[str, str] = None) -> aiohttp.ClientSession:
        if header is None or not isinstance(header, dict):
            header = self.default_header
        return aiohttp.ClientSession(base_url=self.base_url,
                                     headers=header)

    async def search(self, search_filter: SearchFilter):
        data = {
            "limit": search_filter.limit,
            "tags": f"order:{search_filter.order} rating:{search_filter.rating} score:>={search_filter.score} -webm "+search_filter.tags
        }
        async with self._new_sesson() as session:
            async with session.get('/posts.json', data=data, proxy=self.proxy) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise RequestException()
