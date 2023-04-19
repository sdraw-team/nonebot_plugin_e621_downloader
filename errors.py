class WrongOrderTypeException(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("搜索排序类型错误", *args)


class RequestException(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__("返回状态错误", *args)


class ConfigUnfinishedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("配置项未填写或未填写完整"*args)
