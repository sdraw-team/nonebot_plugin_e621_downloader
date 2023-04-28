import asyncio
import time
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .errors import *
from .e621 import E621Post, E621Service, SearchFilter


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
        return None

    download_start = time.time()
    try:
        pics = await svc.download_pics(posts)
    except Exception as e:
        svc.log.error(str(e))
        return Message(str(e))
    download_end = time.time()
    download_cost = download_end - download_start
    svc.log.info("搜索耗时{:.2f}秒，下载了{}张图，耗时{:.2f}秒",
                 search_cost, len(pics), download_cost)

    message = Message(f'共{len(pics)}张图，耗时{download_cost:.2f}秒')
    for pic in pics:
        message.append(MessageSegment.image(pic))

    return message
