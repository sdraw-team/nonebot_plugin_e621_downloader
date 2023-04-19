from pydantic import BaseModel, Extra
import nonebot

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    e621_account: str = None
    e621_api_key: str = None

global_config = nonebot.get_driver().config
e621_config = Config(**global_config.dict())  # 载入配置