import nonebot
from nonebot import on_shell_command
from nonebot.log import logger
from nonebot.params import ShellCommandArgs
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.matcher import Matcher
from nonebot.rule import ArgumentParser, Namespace
from .e621 import E621Service, SearchFilter
from .config import Config
from .usecase import search_pics
from nonebot.adapters.onebot.v11.exception import NetworkError

config = Config.parse_obj(nonebot.get_driver().config.dict())

pic_argument = ArgumentParser()
pic_argument.add_argument('-t', "--tags", nargs='*', help='标签', dest='tags')
pic_argument.add_argument('-r', "--rating", type=str,
                          help='控制安全等级，s->q->e逐渐增大', dest='rating', default='s')
pic_argument.add_argument(
    '-o', type=str, help='图片拉取的顺序，默认random，可选new或者score', dest='order', default='random')
pic_argument.add_argument(
    '-n', type=int, help='图片数量，最多不超过10', dest='number', default=1)
pic_argument.add_argument('-s', "--score", type=int,
                          help='图片的score，最高不超过50', dest='score', default=0)

pic_command = on_shell_command(
    "来点图", priority=10, block=True, parser=pic_argument, aliases={"e621", '来张图', '621'})

svc = E621Service(config.e621_account, config.e621_api_key, logger,
                  proxy=config.e621_proxy)

@pic_command.handle()
async def handle_function(matcher: Matcher, event: MessageEvent, args:  Namespace = ShellCommandArgs()):
    ltags = ' '.join(args.tags) if isinstance(args.tags, list) else ''
    try: 
        search_filter = SearchFilter()
        search_filter.tags = ltags
        search_filter.limit = args.number
        search_filter.order = args.order
        search_filter.rating = args.rating
        search_filter.score = args.score
        message = await search_pics(svc,search_filter=search_filter)
    except NetworkError:
        matcher.finish("上传超时了，尝试减少图片请求数量或者再试一次吧･ﾟ(ﾉд`ﾟ)")
    except Exception as e:
        logger.error(str(e))
        matcher.finish(str(e))
    if message:
        await matcher.finish(message=message)
    else:
        await matcher.finish("没有找到你想要的图片呢σ`∀´)")
