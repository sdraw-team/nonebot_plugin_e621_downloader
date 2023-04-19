import asyncio
import time
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .errors import *
import aiohttp as aio
from .e621 import E621Post, E621Service, SearchFilter


async def download_pic(post: E621Post) -> bytes:
    # 之后把图片下载方法封装到post里面或者svc里面
    url = post.sample_pic if post.sample_pic else post.origin_pic
    async with aio.ClientSession(headers=post.svc.default_header) as session:
        async with session.get(url=url, proxy=post.svc.proxy) as resp:
            return await resp.read()


async def search_pics(svc: E621Service, search_filter: SearchFilter) -> Message:
    posts = []
    search_start = time.time()
    try:
        search_result = await svc.search(search_filter=search_filter)
        origin_json = search_result['posts']
        for p in origin_json:
            id = p['id']
            sample_pic = p['sample'].get('url', '')
            origin_pic = p['file']['url']
            preview = p['preview']['url']
            posts.append(E621Post(
                svc=svc,
                id=id,
                sample_pic=sample_pic,
                origin_pic=origin_pic,
                preview=preview
            ))
    except WrongOrderTypeException:
        svc.log.error("搜索排序类型错误")
        return Message("搜索排序类型错误")
    except Exception as e:
        svc.log.error(str(e))
        return Message(str(e))
    search_end = time.time()
    search_cost = search_end - search_start

    # 异步下载所有post
    if len(posts) == 0:
        return Message()

    download_start = time.time()
    tasks = []
    for post in posts:
        tasks.append(download_pic(post))
    pics: list[bytes] = await asyncio.gather(*tasks)
    download_end = time.time()
    download_cost = download_end - download_start
    svc.log.info("搜索耗时{}秒，下载了{}张图，耗时{:.2f}秒",
                 search_cost, len(tasks), download_cost)

    message = Message(f'共{len(tasks)}张图，耗时{download_end-download_start:.2f}秒')
    for pic in pics:
        message.append(MessageSegment.image(pic))

    return message
