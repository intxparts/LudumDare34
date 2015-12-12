

class Player:

    def __init__(self):
        self.__is_facing_right = False

    @property
    def is_facing_right(self):
        return self.__is_facing_right

    def update(self):
        pass
