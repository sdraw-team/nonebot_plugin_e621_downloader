from pydantic import BaseModel, Extra
import nonebot

class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    e621_account: str = None
    e621_api_key: str = None
    e621_proxy: str = None