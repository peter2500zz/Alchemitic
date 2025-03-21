

class GUIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)



class AssetsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AssetsNotInitializedYet(Exception):
    def __init__(self, path):
        self.message = f'在还未初始化资源时试图读取资源 {path}'
        super().__init__(self.message)

