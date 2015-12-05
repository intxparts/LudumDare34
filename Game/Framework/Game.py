import pygame
from abc import *


class Game(metaclass=ABCMeta):
    """
       Defines a base Game class that provides the essentials for a basic 2D-game framework for rapid game prototyping.
    """

    def __init__(self):
        # clock for keeping track of time, ticks, and frames per second
        self._clock = pygame.time.Clock()

        # the current scene
        self._current_scene = None

        self._scenes = {}

        # the screen/display
        self._display = None

        self._on_initialize()
        self._on_set_display_mode()
        self._on_load_scenes(self._get_scenes())

    def _on_initialize(self):
        """
            Handles initialization of all pygame components needed for the game.
        """
        pygame.init()

        # initialize the display for drawing to the screen
        pygame.display.init()

        # initialize the mixer for sound to work
        pygame.mixer.init()

    @property
    def screen_dimensions(self):
        return [self.screen_width, self.screen_height]

    @abstractproperty
    def screen_width(self):
        return 800

    @abstractproperty
    def screen_height(self):
        return 600

    @abstractmethod
    def _get_scenes(self):
        """
            Override to return iterable object of all possible scenes needed for the game to run.
        """
        return []

    def _on_load_scenes(self, scene_list):
        """
            Loads the current scene and scenes from the scene_list into the scene dictionary
        """
        if scene_list:
            self._current_scene = scene_list[0]
            self._scenes.update({scene.id(): scene for scene in scene_list})

    def _on_set_display_mode(self):
        """
            override this to create and set the _display object
        """
        self._display = pygame.display.set_mode([self.screen_width, self.screen_height], pygame.DOUBLEBUF, 32)

    def _on_set_fps(self):
        """
            override to set the default FPS limit - defaults to 60
        """
        self._clock.tick(60)

    def _on_get_transition(self, transition_scene_id):
        """
            Returns the corresponding scene object to the given id.
            Returns None in the case that the id is falsey or not in the _scenes dict()
        """
        if transition_scene_id and transition_scene_id in self._scenes.keys():
            return self._scenes[transition_scene_id]
        else:
            return None

    def run(self):
        """
            Responsible for handling the main game loop.
        """
        done = False
        while not done:

            self._on_set_fps()
            self._current_scene.draw(self._display)
            pygame.display.flip()

            events = pygame.event.get()
            transition_scene_id = self._current_scene.update(events)

            if transition_scene_id:
                # get the next scene
                self._current_scene = self._on_get_transition(transition_scene_id)

                if self._current_scene:
                    self._current_scene.reset()
                else:
                    done = True

        # shuts down all pygame modules - IDLE friendly
        pygame.quit()
