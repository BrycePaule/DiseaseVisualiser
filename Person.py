import random

from Names import get_random_name


class Person:
    """
    0 - healthy
    1 - infected
    """

    def __init__(self, id):
        self.id = id
        self.name = get_random_name()
        self.status = 0

        # self.happiness = 0


    def __repr__(self):
        return f'<Person:  {self.name}, {self.status}>'