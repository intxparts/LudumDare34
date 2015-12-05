from abc import *


class Scene(metaclass=ABCMeta):
    """
        Defines a basic Scene interface for various Game scenes.
    """

    def __init__(self, screen_dimensions):
        self.__screen_width = screen_dimensions[0]
        self.__screen_height = screen_dimensions[1]

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def screen_width(self):
        return self.__screen_width

    @abstractmethod
    def reset(self):
        """
            Override to add logic to reset the scene to its starting state.
        """
        pass

    @abstractmethod
    def update(self, events):
        """
            Override to add update logic to the current scene and handle any transitions.
        """
        pass

    @abstractmethod
    def draw(self, display):
        """
            Override to add draw logic for the current scene.
        """
        black = (0, 0, 0)
        display.fill(black)

    @abstractproperty
    def id(self):
        """
            Required override for any unique scene to identify the scene in the scene dictionary
        """
        return ''
