import pygame
import os
from Game.Framework.Scene import *
from Game.Framework.Vector import *


class Cereal:

    box_32 = pygame.image.load(os.path.join('Assets', 'cereal32.png'))

    def __init__(self, position):
        self.__size = 32
        self.image = Cereal.box_32
        self.rect = pygame.Rect((position.x, position.y), (self.__size, self.__size))
        self.velocity = Vector(0, 0)


class Player:
    """
        Holds the state of the player object
    """
    right_facing_32 = pygame.image.load(os.path.join('Assets', 'soul_right.png'))
    right_facing_40 = pygame.image.load(os.path.join('Assets', 'soul_right40.png'))
    right_facing_48 = pygame.image.load(os.path.join('Assets', 'soul_right48.png'))
    right_facing_56 = pygame.image.load(os.path.join('Assets', 'soul_right56.png'))
    right_facing_64 = pygame.image.load(os.path.join('Assets', 'soul_right64.png'))
    right_facing_list = [right_facing_32, right_facing_40, right_facing_48, right_facing_56, right_facing_64]

    left_facing_32 = pygame.image.load(os.path.join('Assets', 'soul_left.png'))
    left_facing_40 = pygame.image.load(os.path.join('Assets', 'soul_left40.png'))
    left_facing_48 = pygame.image.load(os.path.join('Assets', 'soul_left48.png'))
    left_facing_56 = pygame.image.load(os.path.join('Assets', 'soul_left56.png'))
    left_facing_64 = pygame.image.load(os.path.join('Assets', 'soul_left64.png'))
    left_facing_list = [left_facing_32, left_facing_40, left_facing_48, left_facing_56, left_facing_64]

    right_facing_scrunched = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right.png'))
    right_facing_scrunched_40 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right40.png'))
    right_facing_scrunched_48 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right48.png'))
    right_facing_scrunched_56 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right56.png'))
    right_facing_scrunched_64 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_right64.png'))
    right_facing_crouch_list = [right_facing_scrunched, right_facing_scrunched_40, right_facing_scrunched_48,
                                right_facing_scrunched_56, right_facing_scrunched_64]

    left_facing_scrunched = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left.png'))
    left_facing_scrunched_40 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left40.png'))
    left_facing_scrunched_48 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left48.png'))
    left_facing_scrunched_56 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left56.png'))
    left_facing_scrunched_64 = pygame.image.load(os.path.join('Assets', 'soul_scrunch_left64.png'))
    left_facing_crouch_list = [left_facing_scrunched, left_facing_scrunched_40, left_facing_scrunched_48,
                               left_facing_scrunched_56, left_facing_scrunched_64]

    def __init__(self, position, velocity):
        self.__velocity = velocity
        self.__size_index = 0
        self.image = Player.right_facing_list[self.__size_index]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.on_ground = False
        self.__moving_left = False
        self.__moving_right = False
        self.__facing_right = True
        self.is_scrunched = False

    @property
    def size(self):
        return self.__size_index

    def grow(self):
        if self.__size_index < 4:
            self.__size_index += 1

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

    @property
    def growth_difference(self):
        return 8

    @property
    def scrunch_difference(self):
        return (Player.left_facing_list[self.__size_index].get_rect().height -
                Player.left_facing_crouch_list[self.__size_index].get_rect().height)

    def unscrunch(self):
        if self.__facing_right:
            self.image = Player.right_facing_list[self.__size_index]
        else:
            self.image = Player.left_facing_list[self.__size_index]
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y - self.scrunch_difference

    def scrunch(self):
        if self.__facing_right:
            self.image = Player.right_facing_crouch_list[self.__size_index]
        else:
            self.image = Player.left_facing_crouch_list[self.__size_index]
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y + self.scrunch_difference

    def update(self):
        if self.__facing_right:
            if self.is_scrunched:
                self.image = Player.right_facing_crouch_list[self.__size_index]
            else:
                self.image = Player.right_facing_list[self.__size_index]
        else:
            if self.is_scrunched:
                self.image = Player.left_facing_crouch_list[self.__size_index]
            else:
                self.image = Player.left_facing_list[self.__size_index]
        current_position = Vector(self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = current_position.x
        self.rect.y = current_position.y


class Platform:
    """
        Holds the state of a basic platform object
    """

    def __init__(self, position, image, id):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.__id = id

    @property
    def id(self):
        return self.__id

    @staticmethod
    def create_standard_image(dimensions):
        image = pygame.Surface(dimensions)
        image.fill(color=(0, 255, 0))
        return image


class GameScene(Scene):
    move_left_vector = Vector(-3, 0)
    move_right_vector = Vector(3, 0)
    jump_vector = Vector(0, -4)
    platform_thickness = 6
    platform_75_image = pygame.image.load(os.path.join('Assets', 'platform_75.png'))
    platform_50_image = pygame.image.load(os.path.join('Assets', 'platform_50.png'))
    platform_477_image = pygame.image.load(os.path.join('Assets', 'platform_477.png'))
    platform_315_image = pygame.image.load(os.path.join('Assets', 'platform_315.png'))
    cave_image = pygame.image.load(os.path.join('Assets', 'cave.png'))
    cave_full_image = pygame.image.load(os.path.join('Assets', 'cave_full.png'))

    def __init__(self, screen_dimensions):
        super(GameScene, self).__init__(screen_dimensions)
        self.__player = Player(position=Vector(375, 0), velocity=Vector(0, 0))
        soul_friend = Platform(Vector(500, 326), pygame.image.load(os.path.join('Assets', 'soul_friend_left56.png')), 'soul-friend')
        breakable_door = Platform(Vector(285, 326), pygame.image.load(os.path.join('Assets', 'breakable_door.png')), 'breakable-door')
        self.__platform_display_list = [soul_friend, breakable_door]
        self.__platforms = [Platform(Vector(700, 125), Platform.create_standard_image([75, GameScene.platform_thickness]), 'top-right'),
                            Platform(Vector(25, 525), Platform.create_standard_image([75, GameScene.platform_thickness]), 'bottom-left'),
                            Platform(Vector(125, 260), Platform.create_standard_image([50, GameScene.platform_thickness]), 'center-left'),
                            Platform(Vector(180, 382), Platform.create_standard_image([475, GameScene.platform_thickness]), 'bottom-center'),
                            Platform(Vector(275, 320), Platform.create_standard_image([315, GameScene.platform_thickness]), 'center-center'),
                            Platform(Vector(300, 326), Platform.create_standard_image([50, 15]), 'hang-down'),
                            Platform(Vector(375, 250), Platform.create_standard_image([75, GameScene.platform_thickness]), 'top-center'),
                            Platform(Vector(575, 326), Platform.create_standard_image([10, 56]), 'back-wall'),
                            breakable_door,
                            soul_friend]
        self.__cereal_boxes = [Cereal(position=Vector(705, 93)),
                               Cereal(position=Vector(35, 493)),
                               Cereal(position=Vector(425, 344))]
        # [K_a, K_d] - this holds the state of whether the key is pressed or not
        self.__grunt_sound = pygame.mixer.Sound(os.path.join('Assets', 'grunt.ogg'))
        self.__short_grunt_sound = pygame.mixer.Sound(os.path.join('Assets', 'grunt_short.ogg'))
        self.__eating_sound = pygame.mixer.Sound(os.path.join('Assets', 'eating.ogg'))
        self.__unscrunch_requested = False
        self.__background = pygame.image.load(os.path.join('Assets', 'background.png'))
        self.__cave_opened = False

    def __handle_player_off_screen(self):
        if self.__player.rect.x < 400:
            self.__player.rect.x += 400
        else:
            self.__player.rect.x -= 400
        self.__player.rect.y = 0
        self.__player.on_ground = False

    def reset(self):
        self.__player.rect.x = 300
        self.__player.rect.y = 0
        self.__player.on_ground = False

    def __apply_gravity(self):
        GameScene.__apply_gravity_to_entity(self.__player)
        for cereal_box in self.__cereal_boxes:
            GameScene.__apply_gravity_to_entity(cereal_box)

    @staticmethod
    def __apply_gravity_to_entity(entity):
        if entity.velocity.y == 0:
            entity.velocity.y = 1
        else:
            entity.velocity.y += 0.15

    def update(self, events):
        self.__player.on_ground = self.__is_entity_on_ground(self.__player)
        if self.__player.on_ground:
            self.__player.velocity.x = 0
        for cereal_box in self.__cereal_boxes:
            if self.__is_entity_on_ground(cereal_box):
                cereal_box.velocity.x = 0

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
                    self.__grunt_sound.play(0)
                elif event.key == pygame.K_s:
                    self.__unscrunch_requested = False
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
                    self.__unscrunch_requested = True

        if self.__unscrunch_requested and self.__player.is_scrunched:
            anticipated_position = self.__player.rect.copy()
            anticipated_position.y -= self.__player.scrunch_difference
            can_unscrunch = True
            for platform in self.__platforms:
                if anticipated_position.colliderect(platform.rect):
                    can_unscrunch = False
                    break
            if can_unscrunch:
                self.__player.unscrunch()
                self.__player.is_scrunched = False

        if self.__player.moving_left:
            self.__player.velocity.x = -3
        if self.__player.moving_right:
            self.__player.velocity.x = 3
        self.__apply_gravity()
        self.__handle_platform_collisions()
        self.__handle_entity_collisions()

        if self.__player.rect.left < 0 or self.__player.rect.right > self.screen_width or self.__player.rect.top > self.screen_height:
            self.__handle_player_off_screen()

        self.__player.update()

    def __handle_entity_collisions(self):
        to_remove = []
        for cereal_box in self.__cereal_boxes:
            if self.__player.rect.colliderect(cereal_box.rect):
                self.__eating_sound.play(0)
                self.__player.grow()
                self.__player.rect.y -= self.__player.growth_difference
                to_remove.append(cereal_box)
        for cereal_box in to_remove:
            self.__cereal_boxes.remove(cereal_box)

    @staticmethod
    def __check_entity_x_collision(entity, platform):
        if entity.rect.colliderect(platform.rect):

            # entity collides with a platform on their right
            if entity.velocity.x > 0:
                entity.rect.right = platform.rect.left

            # entity collides with a platform on their left
            elif entity.velocity.x < 0:
                entity.rect.left = platform.rect.right

            entity.velocity.x = 0
            return True
        return False

    @staticmethod
    def __check_entity_y_collision(entity, platform):
        if entity.rect.colliderect(platform.rect):

            # entity collides with a platform on their head
            if entity.velocity.y < 0:
                entity.rect.top = platform.rect.bottom

            # entity collides standing on a platform
            elif entity.velocity.y > 0:
                entity.rect.bottom = platform.rect.top

            entity.velocity.y = 0
            return True
        return False

    def __handle_platform_collisions(self):
        for cereal_box in self.__cereal_boxes:
            cereal_box.rect.x += cereal_box.velocity.x
        self.__player.rect.x += self.__player.velocity.x
        to_remove = []
        for platform in self.__platforms:
            if GameScene.__check_entity_x_collision(self.__player, platform):
                if platform.id == 'breakable-door' and self.__player.size > 1:
                    self.__cave_opened = True
                    to_remove.append(platform)

            for cereal_box in self.__cereal_boxes:
                GameScene.__check_entity_x_collision(cereal_box, platform)

        for cereal_box in self.__cereal_boxes:
            cereal_box.rect.y += cereal_box.velocity.y
        self.__player.rect.y += self.__player.velocity.y
        for platform in self.__platforms:
            GameScene.__check_entity_y_collision(self.__player, platform)
            for cereal_box in self.__cereal_boxes:
                GameScene.__check_entity_y_collision(cereal_box, platform)

        for platform in to_remove:
            self.__platforms.remove(platform)
            self.__platform_display_list.remove(platform)

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

        display.blit(GameScene.cave_image, (274, 315))

        # draw the platforms
        for platform in self.__platform_display_list:
            display.blit(platform.image, (platform.rect.x, platform.rect.y))

        for cereal_box in self.__cereal_boxes:
            display.blit(cereal_box.image, (cereal_box.rect.x, cereal_box.rect.y))

        # draw the player
        display.blit(self.__player.image, (self.__player.rect.x, self.__player.rect.y))

        display.blit(GameScene.platform_75_image, (699, 122))
        display.blit(GameScene.platform_75_image, (24, 522))
        display.blit(GameScene.platform_75_image, (374, 247))
        display.blit(GameScene.platform_50_image, (124, 256))
        display.blit(GameScene.platform_315_image, (274, 315))
        if not self.__cave_opened:
            display.blit(GameScene.cave_full_image, (274, 315))

        display.blit(GameScene.platform_477_image, (179, 375))

    def id(self):
        return 'game_scene'
