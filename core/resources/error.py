from core.resources.resource import *

class ResourceError(Exception):
    pass

class ResourceNotEnoughError(ResourceError):
    def __init__(self, resource: Resource):
        message = f'库存中没有至少 {resource.num} 个 {resource.__class__.__name__} 来相减, 如果要强制减少请添加 just_do_it=True'
        super().__init__(message)

class NormalRecipeCannotCreateAspectsError(ResourceError):
    def __init__(self, provides: list[Aspect]):
        message = f'常规合成无法得到 {", ".join([asp.name for asp in provides])} 要素'
        super().__init__(message)

