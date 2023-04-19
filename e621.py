import aiohttp as aio
from .errors import WrongOrderTypeException,requestException

class e621post:
    def __init__(self,originJson) -> None:
        self.id = originJson['id']
        self.sample = originJson['sample']['url'] if originJson['sample']['has'] else None
        self.originPic = originJson['file']['url']
        self.preview = originJson['preview']['url']


class e621:
    def __init__(self,e621_account:str,e621_api_key:str) -> None:
        self.default_header = {
            "User-Agent":"OrcasE621Bot/0.1(Orcas)",
            "login":e621_account,
            "api_key":e621_api_key
        }
        self.base_url = "https://e621.net"
    def __sesson_new(self,header:dict = None):
        if header is None or type(header)!=dict:
            header = self.default_header
        return aio.ClientSession(base_url=self.base_url,
                                 headers=header)
    async def search(self,tags:str,order:str="new",limit:int=1,rating:str = 's',score:int = 0):
        if not order in ['new','score','random']:
            raise WrongOrderTypeException
        rating = 's' if rating not in ['s','q','e'] else rating
        limit = 10 if limit>10 else limit
        score = 50 if score>50 else score
        data = {
            "limit":limit,
            "tags":f"order:{order} rating:{rating} score:>={score} -webm "+tags
        }
        async with self.__sesson_new() as session:
            async with session.get('/posts.json',data = data) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise requestException