from core.resources.resource import Resource

class ResourceError(Exception):
    pass

class ResourceBelowZeroError(ResourceError):
    def __init__(self, resource: Resource):
        message = f'库存中没有至少 {resource.num} 个 {resource.__class__.__name__} 来相减, 如果要强制减少请添加 just_do_it=True'
        super().__init__(message)

