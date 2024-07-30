class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 10
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 4
        self.bullet_height = 24
        self.bullet_color = (88, 214, 141)  # Skywalker lightsabre green!
        self.bullets_allowed = 4

        # Alien settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 represents right; -1 represents left

        # Bomb settings
        self.bomb_speed = 2.0

        # Scoring
        self.alien_points = 50  # Points for each alien

        # Game speed up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 4
        self.bullet_speed = 5.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
