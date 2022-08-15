from enum import Enum
from typing import Final


class ApiEndpoint(Enum):
    API1: Final = ('https://api.publicapis.org/random', 'first')
    API2: Final = ('https://api.publicapis.org/categories', 'second')
    API3: Final = ('https://cat-fact.herokuapp.com/facts', 'third')

    def __init__(self, url, position: str) -> None:
        self.url = url
        self.position = position

    @property
    def do_something(self):
        return f'api endpoint {self.url} and position {self.position}'


class Ec2Images(Enum):
    USE1: Final = ('ami-090fa75af13c156b4', 'us-east-1')
    USW2: Final = ('ami-0cea098ed2ac54925', 'us-west-2')

    def __init__(self, ami_id, region: str) -> None:
        self.ami_id = ami_id
        self.region = region


class InstanceTypes(Enum):
    dev: Final = 't2.micro'
    prod: Final = 't3.large'

    def __init__(self, instance_type: str) -> None:
        self.instance_type = instance_type
