from .e621 import e621,e621post
from .errors import *
import aiohttp as aio
from .config import e621_config
async def download_pic(post:e621post):
    if e621_config.e621_account is None or e621_config.e621_api_key is None:
        raise configUnfinishedError
    e621x = e621(e621_config.e621_account,e621_config.e621_api_key)
    url = post.sample if post.sample else post.originPic
    async with aio.ClientSession(headers=e621x.default_header) as session:
        async with session.get(url=url) as resp:
            return await resp.read()

async def unpack_seach_result(tags,limit=1,order='new',rating = 's',score = 0):
    if e621_config.e621_account is None or e621_config.e621_api_key is None:
        raise configUnfinishedError
    e621x = e621(e621_config.e621_account,e621_config.e621_api_key)
    try:
        result = (await e621x.search(limit=limit,order=order,tags=tags,rating = rating,score=score))['posts']
    except WrongOrderTypeException:
        print("搜索排序类型错误")
        return False
    tmplist = []
    for post in result:
            # await download_pic(e621post(post))  
            tmplist.append(e621post(post))
    return tmplist

