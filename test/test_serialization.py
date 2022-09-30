import datetime
import typing
from typing import List, Union

from simple_auth.serialization import BaseSerialization, Field
from simple_auth.serialization.instance import is_instance


class GetSerialization(BaseSerialization):
    name: str = Field(defaults='', max=100, min=0, required=True, description='姓名')
    age: int = Field(defaults=0, max=100, min=0, required=True, description='年龄')

    def verification_name(self, value, values):

        if value == '1':
            raise ValueError('姓名不能为1')
        return value


class Put1Serialization(BaseSerialization):
    c: Union[str, int] = Field('', max=100, min=0, required=False, description='C')
    # a: List[GetSerialization] = Field([], max=100, min=0, required=False, description='A')

# a = GetSerialization(**{'name': '小明', 'age': 1})
# start_data = datetime.datetime.now()
# a = Put1Serialization(**{'c': '小明'})
# print(a.to_dict())
# print(datetime.datetime.now()-start_data)
a: str = 'a'
print(is_instance(a, str))
