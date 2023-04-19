class WrongOrderTypeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("搜索排序类型错误",*args)
class requestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("返回状态错误",*args)
class configUnfinishedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("配置项未填写或未填写完整"*args)