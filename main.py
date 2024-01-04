import sys

import pygame

from OnScreen import *

pygame.display.set_caption(GAME_NAME)
pygame.display.set_icon(GAME_ICON)


class EnemyCreator():
    def __init__(self, player):
        self.enemies = []
        self.player = player
        self.number_of_orbs = NUM_ORBS
        self.number_of_particles = NUM_PARTICLES
        self.wave_counter = 0
        self.counter_for_diamond = 0
        self.counter_for_laser = 0
        self.default_cd = 6

    def create_enemies(self):
        if not self.player.get_is_time_frozen():
            self.create_orbs(round(self.number_of_orbs))
            if self.wave_counter > 5: # spawns in 5th wave
                self.create_particles(round(self.number_of_particles))
            self.wave_counter += 1

            if self.counter_for_diamond >= self.default_cd and self.wave_counter > 10:
                self.create_diamond()
                self.counter_for_diamond = 0

            if self.counter_for_laser >= self.default_cd + 2 and self.wave_counter >15:
                self.create_laser()
                self.counter_for_laser = 0
                self.default_cd -= 0.1

            self.counter_for_diamond += 1
            self.counter_for_laser += 1

    def create_orbs(self, number_orbs):
        for i in range(number_orbs):
            new_enemy = Orb(random.randint(-WIDTH // 4, round(0.99 * WIDTH)), -random.randint(10, HEIGHT // 2))
            self.enemies.append(new_enemy)

    def create_particles(self, number_particles):
        for i in range(number_particles):
            new_enemy = Particle(random.randint(0, round(0.9 * WIDTH)), random.randint(1, 20), self.player)
            self.enemies.append(new_enemy)

    def create_laser(self):
        new_enemy = Laser(self.player)
        self.enemies.append(new_enemy)

    def create_diamond(self):
        new_enemy = Diamond(random.randint(0, round(0.9 * WIDTH)), random.randint(1, 20))
        if random.random() < 0.5: new_enemy.invert_x()
        if random.random() < 0.5: new_enemy.invert_y()
        self.enemies.append(new_enemy)

    def how_many(self):
        return len(self.enemies)

    def get_enemies(self):
        return self.enemies

    def more_orbs(self, number):
        self.number_of_orbs += number

    def more_particles(self, number):
        self.number_of_particles += number

    def orbs_per_second(self):
        return f"{round(self.number_of_orbs / (ENEMY_TIMER / 1000), 3):.2f}"

    def particles_per_second(self):
        return f"{round(self.number_of_particles / (ENEMY_TIMER / 1000), 3):.2f}"

    def move_enemies(self):
        run = True
        for enemy in self.get_enemies():
            if not self.player.get_is_time_frozen():
                if enemy.move() is not None:
                    self.get_enemies().remove(enemy)

            if enemy.y > HEIGHT and type(enemy) != Diamond:
                self.get_enemies().remove(enemy)

            elif enemy.collision(self.player):
                if self.player.is_hitbox():
                    if not god_mode:
                        run = False

                elif type(enemy) != Laser:
                    self.get_enemies().remove(enemy)
                    self.player.add_score(1)

            elif type(enemy) == Diamond:
                if enemy.y + enemy.get_height() >= HEIGHT or enemy.y <= 0:
                    enemy.invert_y()

                elif enemy.x + enemy.get_width() >= WIDTH or enemy.x <= 0:
                    enemy.invert_x()

        return run


class GoodParticleCreator():
    def __init__(self, player):
        self.good_particles = []
        self.player = player
        self.number_of_good_particles = NUM_GOOD_PARTICLES

    def create_particles(self):
        for i in range(self.number_of_good_particles):
            new_good_particle = GoodParticle(self.player)
            self.good_particles.append(new_good_particle)

    def get_good_particles(self):
        return self.good_particles

    def move_particles(self):
        for good_particle in self.get_good_particles():
            if not self.player.get_is_time_frozen():
                good_particle.move()
            if good_particle.collision(self.player):
                self.get_good_particles().remove(good_particle)


def save_record(record):
    with open('records.txt', 'r') as file:
        existing_record = file.readlines()
    if not existing_record:
        existing_record = [0, 0]
    else:
        existing_record = existing_record[-1].split()

    if int(record.split()[1]) > int(existing_record[1]):
        with open('records.txt', 'w') as file:
            file.write(record)

    return f"time: {existing_record[0]} score: {existing_record[1]} "


def main():
    def draw_text(player, enemy_creator, fps):

        objects_on_screen = enemy_creator.how_many()
        power_level_label = MAIN_FONT.render(f"Power Level: {player.power_level}", 1, (255, 255, 255))
        time_label = MAIN_FONT.render(f"Time: {round(player.get_seconds())}", 1, (255, 255, 255))
        score_label = MAIN_FONT.render(f"Score: {round(player.get_score())}", 1, (255, 255, 255))
        fps_label = SECOND_FONT.render(f"{fps} FPS", 1, (255, 255, 255))

        WIN.blit(fps_label, (WIDTH - fps_label.get_width() - 10, 10))
        WIN.blit(power_level_label, (10, 10))
        WIN.blit(time_label, (10, 50))
        WIN.blit(score_label, (10, 90))

    def redraw_window(player, enemy_creator, good_particle_creator, fps):

        WIN.blit(BG, (0, 0))
        player.draw(WIN)

        for entity in enemy_creator.get_enemies() + good_particle_creator.get_good_particles():
            if player.get_is_time_frozen():
                entity.draw_grey(WIN)
            else:
                entity.draw(WIN)

        draw_text(player, enemy_creator, fps)

        pygame.display.update()

    def initial_screen():
        run = True
        record = save_record("0 0")

        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            WIN.blit(BG, (0, 0))

            commands = ["Record:", record, "Commands:",
                        "Use arrows for movement",
                        "Hold SHIFT to slow down",
                        "Hold Z to speed up",
                        "Hold X to destroy enemies",
                        "Hit SPACE to freeze time!"]

            start_label = SECOND_FONT.render(f"Press any key to start.", 1, (255, 255, 255))
            start_height = HEIGHT // 2
            # Render each line of text onto the surface
            for i, line in enumerate(commands):
                command_label = MAIN_FONT.render(commands[i], 1, (255, 255, 255))
                WIN.blit(command_label,
                         (WIDTH // 2 - command_label.get_width() // 2, start_height + 50 + i * MAIN_FONT.get_height()))

            WIN.blit(start_label,
                     (WIDTH // 2 - start_label.get_width() // 2, start_height - start_label.get_height()))

            pygame.display.update()
        game_screen()

    def game_screen():

        pygame.mixer.init()
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play()

        player = Player()
        clock = pygame.time.Clock()
        pygame.time.set_timer(ENEMY_TIMER_EVENT, ENEMY_TIMER)

        enemy_creator = EnemyCreator(player)
        good_particle_creator = GoodParticleCreator(player)

        next_enemy_spawn_time = ENEMY_TIMER / 1000

        paused_time = 0
        run = True
        while run:

            clock.tick(FPS)
            fps = round(clock.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused_time += pause_screen()
                    elif event.key == pygame.K_m:
                        if pygame.mixer.music.get_volume() != 0:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(0.01)

            if player.get_seconds() >= next_enemy_spawn_time:
                enemy_creator.more_orbs(0.2)
                enemy_creator.more_particles(0.05)
                enemy_creator.create_enemies()
                good_particle_creator.create_particles()
                next_enemy_spawn_time += ENEMY_TIMER / 1000

            player.update_time_and_status()
            player.add_score(0.1)

            keys = pygame.key.get_pressed()
            movement(keys, player)
            special(keys, player)

            good_particle_creator.move_particles()

            if run:
                run = enemy_creator.move_enemies()

            player.set_seconds(paused_time)
            redraw_window(player, enemy_creator, good_particle_creator, fps)

        save_record(f"{player.seconds} {round(player.get_score())}\n")
        death_screen(player)

    def pause_screen():
        pause_start_time = pygame.time.get_ticks()
        pause_text_label = SECOND_FONT.render("Game is paused. Press Esc to resume or R to restart.", 1, (255, 255, 255))
        WIN.blit(pause_text_label,
                 (WIDTH // 2 - pause_text_label.get_width() // 2, HEIGHT // 2 - pause_text_label.get_height() // 2))
        pygame.display.update()

        pygame.mixer.music.pause()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.key == pygame.K_r:
                        initial_screen()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.mixer.music.unpause()
        pause_duration = (pygame.time.get_ticks() - pause_start_time)
        return pause_duration

    def death_screen(player):
        run = True
        pygame.mixer.music.stop()

        death_label = SECOND_FONT.render(f"You Died. Press  R to play again.", 1, (255, 255, 255))
        score_label = SECOND_FONT.render(
            f"You survived for {player.seconds} seconds, with a score of {round(player.get_score())}", 1,
            (255, 255, 255))

        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        run = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            WIN.blit(BG, (0, 0))
            WIN.blit(death_label,
                     (WIDTH // 2 - death_label.get_width() // 2, HEIGHT // 2 - death_label.get_height() // 2 - 15))
            WIN.blit(score_label,
                     (WIDTH // 2 - score_label.get_width() // 2, HEIGHT // 2 - score_label.get_height() // 2 + 15))

            pygame.display.update()
        initial_screen()

    initial_screen()


if __name__ == '__main__':
    main()
