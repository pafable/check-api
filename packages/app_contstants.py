from enum import Enum


class ApiEndpoint(Enum):
    API1 = ('https://api.publicapis.org/random', 'first')
    API2 = ('https://api.publicapis.org/categories', 'second')
    API3 = ('https://cat-fact.herokuapp.com/facts', 'third')

    def __init__(self, url, position):
        self.url = url
        self.position = position

    @property
    def do_something(self):
        return f'api endpoint {self.url} and position {self.position}'
