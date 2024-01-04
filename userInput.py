
from constants import *

def normal_conditions(player):
    player.set_vel(NORMAL_VEL)
    player.set_hitbox(player.get_vel() * 1.5 + 4)

    if player.get_is_time_frozen():
        player.disable_hitbox()
    else:
        player.enable_hitbox()

def movement(keys, player):
    if keys[pygame.K_LSHIFT]:
        player.set_vel(SHIFT_VEL)
        player.set_hitbox(player.get_vel()*2 + 4)

        if player.get_is_time_frozen():
            player.disable_hitbox()
        else:
            player.enable_hitbox()

    elif keys[pygame.K_z]:
        player.set_vel(Z_VEL)
        player.set_hitbox(player.get_vel()*1.5 + 4)

        if player.get_is_time_frozen():
            player.disable_hitbox()
        else:
            player.enable_hitbox()

    elif keys[pygame.K_x]:
        if player.get_special_points() > player.get_min_points():
            player.set_vel(X_VEL)

        if player.get_special_points() > player.dash_cost and player.get_vel() == X_VEL:
            player.set_vel(X_VEL)
            player.set_hitbox(X_VEL * player.power_level*2)
            player.add_special_points(- player.dash_cost)
            player.disable_hitbox()

        else:
            normal_conditions(player)

    else:
        normal_conditions(player)

    if keys[pygame.K_LEFT] and player.x - player.get_vel() > 0:
        player.x -= player.get_vel()
        player.set_image(USER_CHAR_DISPLAY_LEFT)

    elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and player.x + player.get_vel() + player.get_width() < WIDTH:
        player.x += player.get_vel()
        player.set_image(USER_CHAR_DISPLAY_RIGHT)

    else:
        player.set_image(USER_CHAR_DISPLAY)

    if keys[pygame.K_UP] and player.y - player.get_vel() > 0:
        player.y -= player.get_vel()

    if keys[pygame.K_DOWN] and player.y + player.get_vel() + player.get_height() < HEIGHT:
        player.y += player.get_vel()

def special(keys, player):
    if keys[pygame.K_SPACE] and player.get_special_points() >= 100:
        player.add_special_points(-FREEZE_COST)
        player.freeze_time()