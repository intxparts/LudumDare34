import pygame
import os
from Game.Framework.Scene import *
from Game.Framework.Vector import *


class Cereal:

    def __init__(self, size):
        pass


class Player:
    """
        Holds the state of the player object
    """
    right_facing_32 = pygame.image.load(os.path.join('Assets', 'soul_right.png'))
    left_facing_32 = pygame.image.load(os.path.join('Assets', 'soul_left.png'))
    right_facing_scrunched = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right.png'))
    left_facing_scrunched = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left.png'))

    def __init__(self, position, velocity):
        self.__velocity = velocity
        self.image = Player.right_facing_32
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.on_ground = False
        self.__moving_left = False
        self.__moving_right = False
        self.__facing_right = True
        self.is_scrunched = False
        self.size = 32

    def grow(self):
        # update the image
        self.size += 8

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity

    @property
    def moving_left(self):
        return self.__moving_left

    @moving_left.setter
    def moving_left(self, start_moving_left):
        if start_moving_left and not self.__moving_right:
            self.__facing_right = False
        self.__moving_left = start_moving_left

    @property
    def moving_right(self):
        return self.__moving_right

    @moving_right.setter
    def moving_right(self, start_moving_right):
        if start_moving_right and not self.__moving_right:
            self.__facing_right = True
        self.__moving_right = start_moving_right

    def unscrunch(self):
        if self.__facing_right:
            self.image = Player.right_facing_32
        else:
            self.image = Player.left_facing_32
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y - 8

    def scrunch(self):
        if self.__facing_right:
            self.image = Player.right_facing_scrunched
        else:
            self.image = Player.left_facing_scrunched
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y + 8

    def update(self):
        if self.__facing_right:
            if self.is_scrunched:
                self.image = Player.right_facing_scrunched
            else:
                self.image = Player.right_facing_32
        else:
            if self.is_scrunched:
                self.image = Player.left_facing_scrunched
            else:
                self.image = Player.left_facing_32
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y


class Platform:
    """
        Holds the state of a basic platform object
    """

    def __init__(self, position, dimensions):
        self.__width = dimensions[0]
        self.__height = dimensions[1]
        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(color=(0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y


class GameScene(Scene):
    move_left_vector = Vector(-3, 0)
    move_right_vector = Vector(3, 0)
    jump_vector = Vector(0, -4)

    def __init__(self, screen_dimensions):
        super(GameScene, self).__init__(screen_dimensions)
        self.__player = Player(position=Vector(300, 0), velocity=Vector(0, 0))
        self.__platforms = [Platform(position=Vector(300, 300), dimensions=[200, 15]),
                            Platform(position=Vector(515, 250), dimensions=[50, 15]),
                            Platform(position=Vector(350, 215), dimensions=[25, 15])]
        # [K_a, K_d] - this holds the state of whether the key is pressed or not
        self.__key_state = [False, False]
        self.__background = pygame.image.load(os.path.join('Assets', 'background.png'))

    def reset(self):
        self.__player.rect.x = 300
        self.__player.rect.y = 0
        self.__player.on_ground = False

    def update(self, events):
        self.__player.on_ground = self.__is_entity_on_ground(self.__player)
        if self.__player.on_ground:
            self.__player.velocity.x = 0

        unscrunch_requested = False
        # handle input
        for event in events:
            # handle clicking the X on the game window
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.__player.moving_left = True
                elif event.key == pygame.K_d:
                    self.__player.moving_right = True
                elif event.key == pygame.K_SPACE and self.__player.on_ground:
                    self.__player.velocity += GameScene.jump_vector
                elif event.key == pygame.K_s:
                    self.__player.is_scrunched = True
                    self.__player.scrunch()
                elif event.key == pygame.K_ESCAPE:
                    # return exit to trigger graceful exit of program
                    return 'exit'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.__player.moving_left = False
                elif event.key == pygame.K_d:
                    self.__player.moving_right = False
                elif event.key == pygame.K_s:
                    self.__player.is_scrunched = False
                    unscrunch_requested = True

        if unscrunch_requested and not self.__player.is_scrunched:
            anticipated_position = self.__player.rect.copy()
            anticipated_position.y -= 8
            can_unscrunch = True
            for platform in self.__platforms:
                if anticipated_position.colliderect(platform.rect):
                    can_unscrunch = False
                    break
            if can_unscrunch:
                self.__player.unscrunch()

        if self.__player.moving_left:
            self.__player.velocity.x = -3
        if self.__player.moving_right:
            self.__player.velocity.x = 3

        if self.__player.velocity.y == 0:
            self.__player.velocity.y = 1
        else:
            self.__player.velocity.y += 0.15

        self.__player.rect.x += self.__player.velocity.x
        for platform in self.__platforms:
            # if there is a collision
            if self.__player.rect.colliderect(platform.rect):

                # player collides with a platform on their right
                if self.__player.velocity.x > 0:
                    self.__player.rect.right = platform.rect.left

                # player collides with a platform on their left
                elif self.__player.velocity.x < 0:
                    self.__player.rect.left = platform.rect.right

                self.__player.velocity.x = 0

        self.__player.rect.y += self.__player.velocity.y
        for platform in self.__platforms:
            if self.__player.rect.colliderect(platform.rect):

                # player collides with a platform on their head
                if self.__player.velocity.y < 0:
                    self.__player.rect.top = platform.rect.bottom

                # player collides standing on a platform
                elif self.__player.velocity.y > 0:
                    self.__player.rect.bottom = platform.rect.top

                self.__player.velocity.y = 0

        if self.__player.rect.left < 0 or self.__player.rect.right > self.screen_width or self.__player.rect.top > self.screen_height:
            self.reset()

        self.__player.update()

    def __is_entity_on_ground(self, entity):
        entity_rect = entity.rect.copy()
        entity_rect.y += 2
        for platform in self.__platforms:
            if entity_rect.colliderect(platform.rect):
                return True
        return False

    def draw(self, display):
        # draw the black background
        super(GameScene, self).draw(display)

        display.blit(self.__background, (0, 0))

        # draw the platforms
        for platform in self.__platforms:
            display.blit(platform.image, (platform.rect.x, platform.rect.y))

        # draw the player
        display.blit(self.__player.image, (self.__player.rect.x, self.__player.rect.y))

    def id(self):
        return 'game_scene'
