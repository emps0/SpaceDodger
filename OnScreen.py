import random
from userInput import *
from abc import ABC, abstractmethod
from constants import *
from main import *


def collide(obj1, obj2):
    # Checks for collision between two objects based on hitbox. Returns True if collides, False otherwise.

    offset_x = obj2.get_x() - obj1.get_x()
    offset_y = obj2.get_y() - obj1.get_y()
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


class Player:
    def __init__(self):

        # Basics
        self.image = USER_CHAR_DISPLAY
        self.x = WIDTH // 2 - self.get_width() // 2
        self.y = HEIGHT // 2 - self.get_height() // 2
        self.start_time = pygame.time.get_ticks()
        self.seconds = 0

        # Hitbox
        self.hitbox_size = 5
        self.is_hittable = True
        self.set_hitbox()  # sets self.player_hitbox and self.mask
        self.hitbox_x = self.x + self.get_width() // 2 - self.player_hitbox.get_width() // 2
        self.hitbox_y = self.y + self.get_height() // 2 - self.player_hitbox.get_height() // 2

        # Special
        self.min_points = 30
        self.score = 0
        self.quest_points = 0
        self.points_to_next_upgrade = 100
        self.max_special_points = 100
        self.special_points = 0
        self.dash_cost = 3
        self.power_level = 1
        self.freeze_duration = 1500
        self.freeze_start_time = None
        self.is_frozen = False

    def draw(self, window):
        self.__draw_special_bar(window)
        self.__recalculate_hitbox()
        window.blit(self.image, (self.x, self.y))
        window.blit(self.player_hitbox, (self.hitbox_x, self.hitbox_y))

    def __recalculate_hitbox(self):
        # Calculate the center of the player image
        self.hitbox_x = self.x + self.get_width() // 2 - self.player_hitbox.get_width() // 2
        self.hitbox_y = self.y + self.get_height() // 2 - self.player_hitbox.get_height() // 2

    def __draw_special_bar(self, window):
        ratio = self.special_points / self.max_special_points
        x_position = WIDTH // 2 - BAR_WIDTH // 2
        y_position = HEIGHT - BAR_HEIGHT - 15

        pygame.draw.rect(window, (192, 192, 192), (x_position, y_position, BAR_WIDTH, BAR_HEIGHT))
        if ratio == 1:
            pygame.draw.rect(window, "green", (x_position, y_position, BAR_WIDTH * ratio, BAR_HEIGHT))

        elif ratio >= self.get_min_points() / self.max_special_points or not self.is_hitbox():
            pygame.draw.rect(window, "blue", (x_position, y_position, BAR_WIDTH * ratio, BAR_HEIGHT))

        else:
            pygame.draw.rect(window, "red", (x_position, y_position, BAR_WIDTH * ratio, BAR_HEIGHT))

    def add_score(self, number=1):
        self.quest_points += number
        self.score += number

    def add_special_points(self, points):
        self.special_points += points
        if self.special_points > self.max_special_points:
            self.special_points = self.max_special_points

    def disable_hitbox(self):
        self.is_hittable = None

    def enable_hitbox(self):
        self.is_hittable = True

    def is_hitbox(self):
        return self.is_hittable is not None

    def freeze_time(self):
        self.is_frozen = True
        self.freeze_start_time = pygame.time.get_ticks()

    def update_time_and_status(self):
        if self.is_frozen:
            elapsed_time = pygame.time.get_ticks() - self.freeze_start_time
            if elapsed_time >= self.freeze_duration:
                self.is_frozen = False

        if self.quest_points >= self.points_to_next_upgrade and self.power_level < PLAYER_MAX_LEVEL:
            self.power_level += 1
            self.quest_points = 0
            self.points_to_next_upgrade *= 1.1
            self.freeze_duration += 200
            if self.dash_cost >= 0.4:
                self.dash_cost -= 0.3
            if self.get_min_points() > 15:
                self.min_points -= 3

    # Setters

    def set_image(self, image):
        self.image = image

    def set_hitbox(self, size=5):
        self.player_hitbox = pygame.transform.scale(PLAYER_HITBOX, (size, size))
        self.mask = pygame.mask.from_surface(self.player_hitbox)

    def set_vel(self, vel):
        self.vel = vel

    def set_seconds(self, paused_time):
        self.seconds = (pygame.time.get_ticks() - paused_time - self.start_time) / 1000
    # Getters

    def get_vel(self):
        return self.vel

    def get_is_time_frozen(self):
        return self.is_frozen

    def get_special_points(self):
        return self.special_points

    def get_min_points(self):
        return self.min_points

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def get_x(self):
        return self.hitbox_x

    def get_y(self):
        return self.hitbox_y

    def get_score(self):
        return self.score

    def get_seconds(self):
        return self.seconds

class GoodParticle():
    def __init__(self, player):
        if random.randint(1, 10) != 1:
            self.type = 1
        else:
            self.type = 2

        self.image = pygame.transform.scale_by(GOOD_PARTICLE, self.type)
        self.grey_image = pygame.transform.scale_by(GREY_GOOD_PARTICLE, self.type)
        self.y_velocity = 2
        self.x_velocity = 0.2
        self.mask = pygame.mask.from_surface(pygame.Surface((30*self.type, 30*self.type)))
        self.width = self.mask.to_surface().get_width() // 2
        self.height = self.mask.to_surface().get_height() // 2
        self.x = 0
        self.y = 0
        self.spawn()
        self.player = player

    def spawn(self):
        self.x = random.randint(0, WIDTH + 50) - 60
        self.y = -random.randint(0, HEIGHT // 4) * 4

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def draw_grey(self, window):
        window.blit(self.grey_image, (self.x, self.y))

    def move(self):
        self.y += self.y_velocity
        self.x += self.x_velocity

    def collision(self, obj):
        # If player is hittable, turns Good Particles into Special Points. If not, 10% of it into score.

        if collide(self, obj):
            if self.player.is_hitbox():
                self.player.add_special_points(0.5 * self.type)
            else:
                self.player.add_score(0.1)
            return True

    def get_x(self):
        return self.x - self.width

    def get_y(self):
        return self.y - self.height


class Enemy(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = None
        self.image = None
        self.grey_image = None
        self.mask = None

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def draw_grey(self, window):
        window.blit(self.grey_image, (self.x, self.y))

    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image

    def set_grey_image(self, image):
        self.grey_image = image

    def get_speed(self):
        return self.speed

    def move(self):
        self.y += self.speed

    def collision(self, obj):
        return collide(self, obj)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Orb(Enemy):
    def __init__(self, x, y, speed=1.5):
        super().__init__(x, y)
        self.x_speed = speed // 16
        self.y_speed = speed
        self.y_acceleration = 0.005
        self.x_acceleration = 0.0005
        self.set_image(ORB1)
        self.set_grey_image(GREY_ORB)
        self.mask = pygame.mask.from_surface(pygame.transform.scale_by(self.get_image(), 0.8))
        self.hitbox_x = self.x + (0.3 * self.get_width())
        self.hitbox_y = self.y + (0.3 * self.get_height())

    def move(self):
        self.x_speed += self.x_acceleration
        self.y_speed += self.y_acceleration
        self.y += self.y_speed
        self.x += self.x_speed

    def draw(self, window):
        self.recalculate_hitbox()
        window.blit(self.image, (self.x, self.y))

    def recalculate_hitbox(self):
        self.hitbox_x = self.x + (0.1 * self.get_width())
        self.hitbox_y = self.y + (0.1 * self.get_height())


class Diamond(Enemy):
    def __init__(self, x, y, speed=3):
        super().__init__(x, y)
        self.x_speed = speed * 0.7
        self.y_speed = speed
        self.acceleration = 1.3
        self.bounce = 0
        self.stage = 1
        self.set_image(DIAMOND1)
        self.set_grey_image(GREY_DIAMOND)
        self.mask = pygame.mask.from_surface(self.get_image())

    def move(self):
        self.y += self.y_speed
        self.x += self.x_speed

    def invert_y(self):
        self.add_bounce()
        self.y_speed = -self.y_speed

    def invert_x(self):
        self.add_bounce()
        self.x_speed = -self.x_speed

    def add_bounce(self):
        self.bounce += 1
        if self.bounce % 4 == 0:  # it has to bounce 4 times to become more powerful
            self.more_powerful()
        return self.bounce

    def more_powerful(self):
        if self.stage != 4:
            self.stage += 1
            self.set_image(DIAMONDS[self.stage - 1])
            self.y_speed *= self.acceleration
            self.x_speed *= self.acceleration


class Particle(Enemy):
    def __init__(self, x, y, player, speed=0.5):
        super().__init__(x, y)
        self.x_speed = speed * 3
        self.y_speed = speed
        self.y_acceleration = 0.01
        self.player = player
        self.set_image(PARTICLE1)
        self.set_grey_image(GREY_PARTICLE)
        self.mask = pygame.mask.from_surface(self.get_image())

    def move(self):
        self.y_speed += self.y_acceleration
        self.y += self.y_speed

        if self.y < self.player.y and abs(
                (self.player.x + self.player.get_width() // 2) - (self.x + self.get_width() // 2)) > 15:
            if self.player.x < self.x:
                self.x -= self.x_speed

            else:
                self.x += self.x_speed
        else:
            self.y_speed *= 1.05

    def invert_x(self):
        self.x_speed = -self.x_speed


class Laser():
    def __init__(self, player):
        self.image = LASERS[0]
        self.player = player
        self.x = player.get_x() - self.image.get_width()//2
        self.y = 0
        self.counter = 0
        self.explosion_start_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(LASERS[1])

    def draw(self, window):
        current_time = pygame.time.get_ticks()
        if current_time - self.explosion_start_time < 600:
            self.image = LASERS[0]
        elif current_time - self.explosion_start_time < 2000:
            self.image = LASERS[1]

        elif current_time - self.explosion_start_time < 2100:
            self.image = LASERS[0]

        else:
            return True
        window.blit(self.image, (self.x, self.y))

    def move(self):
        pass

    def draw_grey(self, window):
        self.draw(window)

    def collision(self, obj):
        if self.image == LASERS[1]:
            return collide(self, obj)
        else:
            return False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
