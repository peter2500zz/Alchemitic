
class AlchemyError(Exception):
    def __init__(self, message='炼金术出错'):
        self.message = message
        super().__init__(self.message)

class AspectError(AlchemyError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AspectInvalid(AspectError):
    """
    未定义要素出现时抛出此错误
    """
    def __init__(self, message):
        self.message = f'{message} 要素无效'
        super().__init__(self.message)

class AspectNotExist(AspectError):
    """
    当要素有效但是并不含有时抛出此错误
    """
    def __init__(self, message):
        self.message = f'不含有 {message} 要素'
        super().__init__(self.message)
