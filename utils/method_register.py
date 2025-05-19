from methods.slae_solver import SLAESolver

class SLAEMethodRegistry:
    _methods = {}

    @classmethod
    def register(cls, method_class):
        if not issubclass(method_class, SLAESolver):
            raise TypeError("Method must inherit from SLAESolver")
        cls._methods[method_class.__name__.lower()] = method_class
        return method_class

    @classmethod
    def get_method(cls, method_id):
        return cls._methods.get(method_id)

    @classmethod
    def get_method_choices(cls):
        return [(key, getattr(cls._methods[key], "display_name", key.title())) for key in cls._methods]
