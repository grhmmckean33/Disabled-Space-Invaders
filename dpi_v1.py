import sys
import pygame
import random
from settings_v1 import Settings
from game_stats_v1 import GameStats
from ship_v1 import Ship
from bullet_v1 import Bullet
from alien_v1 import Alien
from bomb_v1 import Bomb
from time import sleep
from button_v1 import Button
from scoreboard_v1 import Scoreboard
from barrier_v1 import Barrier

# Group for all sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bombs = pygame.sprite.Group()

# Joystick Init
pygame.joystick.init()
# Joystick control list
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class DPInvaders:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Disabled Parking Invaders')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()  # Group for bombs

        self._create_fleet()
        self._create_barriers()

        self.play_button = Button(self, 'Disabled Parking Invaders - Click Here to Play OR Q to Quit')
        self.bg_color = (230, 230, 230)

        self.stats = GameStats(self)  # For lives images
        self.sb = Scoreboard(self)
        self.ship = Ship(self)

        self.bomb_cooldown = 0 # Time between each bomb
        self.bomb_cooldown_max = 10  # Max Time between each bomb
        self.max_active_bombs = 1  # No. bombs that can be dropped at same time

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bombs()  # Update bombs

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    self._fire_bullet()

                elif event.button == 0 and not self.stats.game_active:
                    self.settings.initialize_dynamic_settings()
                    self.stats.reset_stats()
                    self.stats.game_active = True
                    self.sb.prep_score()
                    self.sb.prep_level()
                    self.sb.prep_ships()
                    self.aliens.empty()
                    self.bullets.empty()
                    self.bombs.empty()
                    self._create_fleet()
                    self._create_barriers()
                    self.ship.center_ship()

                elif event.button == 5:
                    sys.exit()
                print(event)

            if event.type == pygame.JOYHATMOTION:
                if event.value[0] == -1:
                    self.ship.moving_left = True
                    self.ship.moving_right = False
                elif event.value[0] == 1:
                    self.ship.moving_left = False
                    self.ship.moving_right = True
                else:
                    if event.value[0] == 0:
                        self.ship.moving_left = False
                        self.ship.moving_right = False
                print(event)

            if event.type == pygame.JOYAXISMOTION:
                # Read the horizontal axis (0) value
                axis_value = pygame.joystick.Joystick(0).get_axis(0)

                # Check if the axis is moved significantly to the left or right
                if axis_value < -0.5:
                    self.ship.moving_left = True
                    self.ship.moving_right = False
                elif axis_value > 0.5:
                    self.ship.moving_right = True
                    self.ship.moving_left = False
                else:
                    self.ship.moving_left = False
                    self.ship.moving_right = False
                print(event)


            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                self.settings.initialize_dynamic_settings()
                self.stats.reset_stats()
                self.stats.game_active = True
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                self.aliens.empty()
                self.bullets.empty()
                self.bombs.empty()
                self._create_fleet()
                self._create_barriers()  # Recreate barriers when the game restarts
                self.ship.center_ship()
                pygame.mouse.set_visible(False)










    def _check_keydown_events(self, event):
        if event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_s:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_s:
            self.ship.moving_right = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (1 * alien_width)
        number_aliens_x = available_space_x // (1 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (1 * alien_height) -
                             ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_barriers(self):
        barrier_y = self.settings.screen_height - 300  # Adjust the height above the ship
        barrier_spacing = 200
        for i in range(5):  # Create 3 barriers
            barrier_x = barrier_spacing + i * barrier_spacing
            barrier = Barrier(self, barrier_x, barrier_y)
            self.barriers.add(barrier)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.bombs.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_bombs(self):
        self.bombs.update()
        # Check for collisions between bombs and barriers
        bomb_barrier_collisions = pygame.sprite.groupcollide(self.bombs, self.barriers,
                                                             True, False)
        for bomb, barriers in bomb_barrier_collisions.items():
            for barrier in barriers:
                barrier.take_damage(20, bomb.rect)

        if pygame.sprite.spritecollideany(self.ship, self.bombs):
            self._ship_hit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.barriers.draw(self.screen)
        for bomb in self.bombs.sprites():
            bomb.draw_bomb()
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    dpi_game = DPInvaders()
    dpi_game.run_game()
