from database import Boss, Player
import arcade
import random
import math
import time


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.PINK)

        self.game = Game(target_x=width // 2, target_y=height // 2)

        self.player = Units(
            width, height,
            100, 100,
            30, arcade.color.BLUE,
            up_key=arcade.key.W,
            down_key=arcade.key.S,
            left_key=arcade.key.A,
            right_key=arcade.key.D
        )

        self.boss = Units(
            width, height,
            width / 2, height / 2,
            80, arcade.color.RED,
        )

        self.units = [self.player, self.boss]

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.boss.draw()
        self.game.draw()

    def on_update(self, delta_time):
        # Передаем позицию и радиус игрока для проверки столкновений
        self.game.update(delta_time, self.player.pos_x, self.player.pos_y, self.player.radius)

        for unit in self.units:
            unit.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.game.create_attack(start_x=self.player.pos_x, start_y=self.player.pos_y)

        elif key == arcade.key.SPACE:
            if self.game.is_shooting:
                self.game.stop_shooting()
            else:
                self.game.start_shooting()

        for unit in self.units:
            unit.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        for unit in self.units:
            unit.on_key_release(key, modifiers)


class Units:
    def __init__(self, width=800, height=800, pos_x=None, pos_y=None, radius=30,
                 color=arcade.color.LIGHT_GRAY, speed=5,
                 up_key=None, down_key=None,
                 left_key=None, right_key=None):
        self.width = width
        self.height = height

        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        if pos_x is None:
            self.pos_x = width // 2
        else:
            self.pos_x = pos_x

        if pos_y is None:
            self.pos_y = height // 2
        else:
            self.pos_y = pos_y

        if radius > 0 and radius * 2 <= min(self.width, self.height):
            self.radius = radius
        else:
            self.radius = min(30, min(self.width, self.height) // 2)

        self.color = color
        self.speed = speed

    def draw(self):
        arcade.draw_circle_filled(self.pos_x, self.pos_y, self.radius, self.color)

    def update(self):
        if self.up and self.pos_y < self.height - self.radius:
            self.pos_y += self.speed
        if self.down and self.pos_y > self.radius:
            self.pos_y -= self.speed
        if self.left and self.pos_x > self.radius:
            self.pos_x -= self.speed
        if self.right and self.pos_x < self.width - self.radius:
            self.pos_x += self.speed

    def on_key_press(self, key, modifiers):
        if self.up_key is not None and key == self.up_key:
            self.up = True
        elif self.down_key is not None and key == self.down_key:
            self.down = True
        elif self.left_key is not None and key == self.left_key:
            self.left = True
        elif self.right_key is not None and key == self.right_key:
            self.right = True

    def on_key_release(self, key, modifiers):
        if self.up_key is not None and key == self.up_key:
            self.up = False
        elif self.down_key is not None and key == self.down_key:
            self.down = False
        elif self.left_key is not None and key == self.left_key:
            self.left = False
        elif self.right_key is not None and key == self.right_key:
            self.right = False


class Atacs:
    def __init__(self, width=800, height=800, start_x=None, start_y=None,
                 end_x=None, end_y=None, color=arcade.color.GOLD,
                 line_width=3, speed=10, damage=20, max_distance=400):
        """
        start_x, start_y: начальная точка атаки (от босса)
        end_x, end_y: точка направления (позиция игрока)
        speed: скорость движения луча
        max_distance: максимальная дистанция до границы экрана
        """
        self.width = width
        self.height = height

        self.start_x = start_x if start_x is not None else width // 2
        self.start_y = start_y if start_y is not None else height // 2

        # Точка направления (позиция игрока в момент выстрела)
        self.target_x = end_x if end_x is not None else width
        self.target_y = end_y if end_y is not None else height

        self.current_x = self.start_x
        self.current_y = self.start_y

        # Вектор направления от босса к игроку
        dx = self.target_x - self.start_x
        dy = self.target_y - self.start_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance
        else:
            self.direction_x = 0
            self.direction_y = 0

        self.color = color
        self.line_width = line_width
        self.speed = speed
        self.damage = damage
        self.max_distance = max_distance
        self.distance_traveled = 0

        self.active = True
        self.has_hit_player = False  # Флаг попадания в игрока

    def draw(self):
        if self.active:
            arcade.draw_line(self.start_x, self.start_y,
                             self.current_x, self.current_y,
                             self.color, self.line_width)

    def update(self, delta_time):
        if not self.active:
            return

        # Двигаем луч в направлении игрока
        move_distance = self.speed * delta_time
        self.current_x += self.direction_x * move_distance
        self.current_y += self.direction_y * move_distance
        self.distance_traveled += move_distance

        # Луч активен пока не достиг границы экрана
        if (self.current_x < 0 or self.current_x > self.width or
                self.current_y < 0 or self.current_y > self.height):
            self.active = False

        if self.distance_traveled >= self.max_distance:
            self.active = False

    def is_active(self):
        return self.active

    def deactivate(self):
        self.active = False

    def check_player_hit(self, player_x, player_y, player_radius):
        """Проверка попадания луча в игрока"""
        if self.has_hit_player or not self.active:
            return False

        # Вектор луча
        line_dx = self.current_x - self.start_x
        line_dy = self.current_y - self.start_y
        line_length = math.sqrt(line_dx * line_dx + line_dy * line_dy)

        if line_length == 0:
            return False

        # Нормализованный вектор луча
        line_dir_x = line_dx / line_length
        line_dir_y = line_dy / line_length

        # Вектор от начала луча к игроку
        to_player_x = player_x - self.start_x
        to_player_y = player_y - self.start_y

        # Проекция вектора на луч
        projection = to_player_x * line_dir_x + to_player_y * line_dir_y

        # Если проекция за пределами луча
        if projection < 0 or projection > line_length:
            return False

        # Ближайшая точка на луче к игроку
        closest_x = self.start_x + line_dir_x * projection
        closest_y = self.start_y + line_dir_y * projection

        # Расстояние от игрока до ближайшей точки
        distance = math.sqrt((player_x - closest_x) ** 2 + (player_y - closest_y) ** 2)

        # Если расстояние меньше радиуса игрока + толщины луча
        if distance < player_radius + self.line_width / 2:
            self.has_hit_player = True
            return True

        return False


class Game:
    def __init__(self, target_x, target_y):
        self.time = time.time()
        self.target_x = target_x  # Позиция босса (откуда летят лучи)
        self.target_y = target_y

        self.attacks = []  # Список активных лучей
        self.shoot_timer = 0
        self.shoot_interval = 0.1  # Интервал между выстрелами
        self.shots_fired = 0
        self.max_shots = 999999999999999999
        self.is_shooting = False  # Флаг автострельбы

    def start_shooting(self):
        """Включить автострельбу"""
        self.is_shooting = True
        self.shots_fired = 0
        self.shoot_timer = 0

    def stop_shooting(self):
        """Выключить автострельбу"""
        self.is_shooting = False

    def create_attack(self, start_x, start_y):
        """Создать луч от босса к игроку"""
        attack = Atacs(
            width=800,
            height=800,
            start_x=self.target_x,  # От босса
            start_y=self.target_y,
            end_x=start_x,  # К игроку (направление)
            end_y=start_y,
            color=arcade.color.RED,
            speed=500,  # Скорость луча
            line_width=8,
            damage=20,
            max_distance=800
        )
        self.attacks.append(attack)
        return attack

    def update(self, delta_time, player_x=None, player_y=None, player_radius=30):
        """Обновление логики игры"""
        # Обновляем все лучи
        for attack in self.attacks[:]:
            attack.update(delta_time)

            # Проверяем попадание в игрока
            if player_x is not None and player_y is not None:
                if attack.check_player_hit(player_x, player_y, player_radius):
                    print("Игрок получил урон!")
                    # Здесь можно добавить логику урона

            # Удаляем неактивные лучи
            if not attack.is_active():
                self.attacks.remove(attack)

        # Автострельба
        if self.is_shooting and self.shots_fired < self.max_shots and player_x is not None:
            self.shoot_timer += delta_time

            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.shots_fired += 1
                self.create_attack(player_x, player_y)

    def draw(self):
        """Отрисовка всех лучей"""
        for attack in self.attacks:
            attack.draw()


def main():
    game = MyGame(800, 600, 'GAME')
    arcade.run()


if __name__ == "__main__":
    main()