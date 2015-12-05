from Game.Framework.Game import *
from Game.GameScene import *


class DemoGame(Game):

    def _get_scenes(self):
        return [GameScene(self.screen_dimensions)]

    @property
    def screen_height(self):
        return super(DemoGame, self).screen_height

    @property
    def screen_width(self):
        return super(DemoGame, self).screen_width
