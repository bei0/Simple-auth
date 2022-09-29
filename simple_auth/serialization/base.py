from simple_auth.field import Field


class SerializationMetaclass(type):
    __to_dict__ = dict()

    def __init__(self, class_name, class_bases, class_dic):
        super(SerializationMetaclass, self).__init__(class_name, class_bases, class_dic)

    @classmethod
    def __prepare__(metacls, name, bases):
        d = dict()
        for base in bases:
            for key, value in base.__dict__.items():
                if not key.startswith('_'):
                    d[key] = value
        return d

    def __new__(cls, name, bases, namespace):

        for base in bases:
            for key, value in base.__dict__.items():
                if not key.startswith('_'):
                    del namespace[key]

        for key, value in namespace.items():

            if key.startswith('verification_'):
                args = key.split('_')[-1]
                if args not in namespace.get('__annotations__'):
                    qualname = namespace.get('__qualname__')
                    raise ModuleNotFoundError(f'`{qualname}`类参数`{args}`不存在, 定义验证函数`{key}`失败')
            if isinstance(value, Field):
                cls.__to_dict__[key] = value

        return type.__new__(cls, name, bases, dict(namespace))

    def __call__(self, *args, **kwargs):

        for k, v in self.__dict__.get('__annotations__').items():
            if hasattr(self.__dict__.get(k), '__set__'):
                if not isinstance(self.__dict__.get(k).__get__(self, k), v):
                    description = self.__dict__.get(k).description or k
                    raise TypeError(f'{description}类型错误:{v.__name__}')

        for key, value in kwargs.items():
            if key in self.__to_dict__:
                value_type = self.__dict__.get('__annotations__').get(key)
                if not isinstance(value, value_type):
                    description = self.__dict__.get(key).description or key
                    raise TypeError(f'{description}类型错误:{value_type.__name__}')
                self.__to_dict__[key].__set__(self, value)

        return super().__call__(*args, **kwargs)


class BaseSerialization(metaclass=SerializationMetaclass):

    __to_dict = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__to_dict = {key: value.__get__(self, value) for key, value in self.__class__.__to_dict__.items()}
        self.execute_verify()

    def execute_verify(self):
        obj_dir = self.__dir__()
        verification_ware = [obj for obj in obj_dir if obj.startswith('verification_')]
        for func in verification_ware:
            args = func.split('_')[-1]
            value = getattr(self, func)(value=getattr(self, args), values=self.__to_dict)
            _ = {key: value.__get__(self, value) for key, value in self.__class__.__to_dict__.items()}
            if len(self.__to_dict) != len(_):
                if len(self.__to_dict) > len(_):
                    key = list(set(self.__to_dict.keys()) - set(_.keys()))[0]
                else:
                    key = list(set(_.keys()) - set(self.__to_dict.keys()))[0]
                raise KeyError(f'{key}:非法参数')
            self.__class__.__to_dict__[args].__set__(args, value)

    def to_dict(self):
        return self.__to_dict
