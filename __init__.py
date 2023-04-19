from nonebot import get_driver,on_shell_command
from nonebot.params import ShellCommandArgs
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.matcher import Matcher
from nonebot.rule import ArgumentParser,Namespace
from .config import Config
from .utils import unpack_seach_result,download_pic
from .e621 import e621post
from .errors import configUnfinishedError

global_config = get_driver().config
config = Config.parse_obj(global_config)
pic_argument = ArgumentParser()
pic_argument.add_argument('-t',nargs='*',help='标签',dest='tags')
pic_argument.add_argument('-s',type=str,help='控制安全等级，s->q->e逐渐增大',dest='safe',default='s')
pic_argument.add_argument('-o',type=str,help='图片拉取的顺序，默认random，可选new或者score',dest='order',default='random')
pic_argument.add_argument('-n',type=int,help='图片数量，最多不超过10',dest='number',default = 1)

pic_command = on_shell_command("来点图",priority=10,block=True,parser=pic_argument,aliases={"e621",'来张图','621'})


@pic_command.handle()
async def handle_function(args:  Namespace= ShellCommandArgs()):
    ltags =  ' '.join(args.tags) if type(args.tags) == list else ''
    try:
        picList = await unpack_seach_result(tags=ltags,order=args.order,limit=args.number,rating=args.safe)
    except configUnfinishedError:
        pic_command.finish("有人没填写配置项，我不说是谁(;´ヮ`)7")
    if picList:
        message_sequence=[]
        for post in picList:
            message_sequence.append(MessageSegment.image(await(download_pic(post))))
        await pic_command.finish(message=message_sequence)
    else:
        await pic_command.finish("没有找到你想要的图片呢σ`∀´)")
