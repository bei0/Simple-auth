import datetime
from simple_auth.serialization import BaseSerialization, Field


class GetSerialization(BaseSerialization):
    name: str = Field(defaults='', max=100, min=0, required=True, description='姓名')
    age: int = Field(defaults=0, max=100, min=0, required=True, description='年龄')

    def verification_name(self, value, values):

        if value == '1':
            raise ValueError('姓名不能为1')
        return value


class SetSerialization(GetSerialization):
    a: str = Field(max=100, min=0, required=False)


class PutSerialization(SetSerialization):
    b: str = Field('10', max=100, min=0, required=True, description='B')


class Put1Serialization(SetSerialization):
    c: str = Field(max=100, min=0, required=False, description='C')


# a = GetSerialization(**{'name': '小明', 'age': 1})
start_data = datetime.datetime.now()
a = GetSerialization(**{'name': '小明', 'age': 1, 'v': 2})
print(a.to_dict())
print(datetime.datetime.now()-start_data)
