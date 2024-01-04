import pygame
import os

pygame.font.init()
# god_mode = True if input("God mode? (y/n)").lower() == "y" else False #for testing purposes
# WIDTH, HEIGHT = int(input("screen x")), int(input("screen y"))
god_mode = 0
WIDTH, HEIGHT = 1280, 960
BAR_WIDTH, BAR_HEIGHT = 500, 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_MAX_LEVEL = 8
NORMAL_VEL = 7
SHIFT_VEL = 3
Z_VEL = 12
X_VEL = 16
FREEZE_COST = 75

FPS = 60
ENEMY_TIMER = 1500 # time in milliseconds
ENEMY_TIMER_EVENT = pygame.USEREVENT + 1

GAME_ICON = pygame.image.load(os.path.join("assets", "game icon.png"))
GAME_NAME = "Space Dodger 0.1"
GAME_MUSIC = os.path.join("audio", "Necrofantasia.mp3")
MAIN_FONT = pygame.font.SysFont("calibri", 30)
SECOND_FONT = pygame.font.SysFont("audiowide", 50)

NUM_ORBS = 10
NUM_PARTICLES = 1
NUM_GOOD_PARTICLES = 100

# Load images
USER_CHAR = pygame.image.load(os.path.join("assets", "quinzel", "quinzel.png")).convert_alpha()
USER_CHAR_LEFT = pygame.image.load(os.path.join("assets", "quinzel", "quinzel left.png")).convert_alpha()
USER_CHAR_RIGHT = pygame.image.load(os.path.join("assets", "quinzel", "quinzel right.png")).convert_alpha()
USER_CHAR_DISPLAY = pygame.transform.scale_by(USER_CHAR, 0.5).convert_alpha()
USER_CHAR_DISPLAY_LEFT = pygame.transform.scale_by(USER_CHAR_LEFT, 0.5).convert_alpha()
USER_CHAR_DISPLAY_RIGHT = pygame.transform.scale_by(USER_CHAR_RIGHT, 0.5).convert_alpha()
PLAYER_HITBOX = pygame.image.load(os.path.join("assets", "quinzel", "player hitbox.png")).convert_alpha()
PLAYER_HORIZONTAL_BAR = pygame.image.load(os.path.join("assets", "horizontal bar.png")).convert_alpha()

GOOD_PARTICLE= pygame.image.load(os.path.join("assets", "good particle.png")).convert_alpha()
GREY_GOOD_PARTICLE= pygame.image.load(os.path.join("assets", "grey good particle.png")).convert_alpha()


ORB1 = pygame.image.load(os.path.join("assets", "orb1.png")).convert_alpha()
GREY_ORB = pygame.image.load(os.path.join("assets", "grey orb1.png")).convert_alpha()

GREY_DIAMOND = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "diamonds", "grey diamond.png")), 0.7).convert_alpha()
DIAMOND1 = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "diamonds", "diamond.png")), 0.7).convert_alpha()
DIAMOND2 = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "diamonds", "diamond2.png")), 0.7).convert_alpha()
DIAMOND3 = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "diamonds", "diamond3.png")), 0.7).convert_alpha()
DIAMOND4 = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "diamonds", "diamond4.png")), 0.7).convert_alpha()

DIAMONDS = [DIAMOND1, DIAMOND2, DIAMOND3, DIAMOND4]


LASER = pygame.image.load(os.path.join("assets", "laser", "laser.png")).convert_alpha()
LASER2 = pygame.image.load(os.path.join("assets", "laser", "laser2.png")).convert_alpha()

LASERS = [LASER, LASER2]


GREY_PARTICLE = pygame.image.load(os.path.join("assets", "grey particle.png")).convert_alpha()
PARTICLE1 = pygame.image.load(os.path.join("assets", "particle.png")).convert_alpha()

# Background
BG = pygame.image.load(os.path.join("assets", "background.png")).convert_alpha()
