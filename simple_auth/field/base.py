from typing import Any


class Field:

    def __init__(self, defaults: Any = None, max: int = 100,
                 min: int = 0, required: bool = True, description: str = None
                 ):
        self.defaults = defaults
        self.max = max
        self.min = min
        self.required = required
        self.description = description
        self.__verify_required()
        self.__verify_max()
        self.__verify_min()

    def __get__(self, instance, value):
        return self.defaults

    def __set__(self, instance, value):
        self.defaults = value
        self.__verify_required()
        self.__verify_max()
        self.__verify_min()

    def __verify_required(self):
        if self.required and self.defaults is None:
            raise TypeError(f'{self.description if self.description else self.__class__.__name__}不能为空')

    def __verify_max(self):
        if self.defaults is not None:
            if not isinstance(self.defaults, int) and len(self.defaults) > self.max:
                raise TypeError(f'{self.description if self.description else self.__class__.__name__}'
                                f'不能大于{self.max}位')
            elif len(str(self.defaults)) > self.max:
                raise TypeError(f'{self.description if self.description else self.__class__.__name__}'
                                f'不能大于{self.max}位')

    def __verify_min(self):
        if self.defaults is not None:
            if not isinstance(self.defaults, int) and len(self.defaults) < self.min:
                raise TypeError(f'{self.description if self.description else self.__class__.__name__}'
                                f'不能小于{self.min}位')
            elif len(str(self.defaults)) < self.min:
                raise TypeError(f'{self.description if self.description else self.__class__.__name__}'
                                f'不能小于{self.min}位')
