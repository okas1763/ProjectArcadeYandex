from database import Boss, Player  # Закомментировал, так как вероятно нет этого файла
import arcade
import random
import math
import time


class MyGame(arcade.Window, Boss, Player):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.PINK)

        # Создаем объекты Boss и Player
        boss_obj = Boss()
        player_obj = Player()

        self.player = Units(
            width, height,
            100, 100,
            30, arcade.color.BLUE,
            speed=player_obj.get_speed(),  # Используем метод get_speed()
            up_key=arcade.key.W,
            down_key=arcade.key.S,
            left_key=arcade.key.A,
            right_key=arcade.key.D
        )

        self.boss = Units(
            width, height,
            width / 2, height / 2,
            80, arcade.color.RED,
            speed=boss_obj.get_speed(),  # Используем метод get_speed()
        )

        # Список всех объектов
        self.units = [self.player]

        # Список активных атак
        self.attacks = []

        # Для тестирования: кнопка выстрела
        self.shoot_key = arcade.key.SPACE

        # Инициализируем score_text с использованием boss_obj
        self.score_text = arcade.Text(boss_obj.get_name(), width / 2 - 32, height / 2 - 10, arcade.color.NAVY_BLUE, 16)

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.boss.draw()
        self.score_text.draw()

        # Отрисовываем все активные атаки
        for attack in self.attacks:
            attack.draw()

    def on_update(self, delta_time):
        # Обновляем позиции всех объектов
        for unit in self.units:
            unit.update()

        # Обновляем все атаки
        for attack in self.attacks[:]:  # Копируем список для безопасного удаления
            attack.update(delta_time)  # Добавил delta_time

            # Удаляем неактивные атаки
            if not attack.is_active():
                self.attacks.remove(attack)

    def on_key_press(self, key, modifiers):
        # Управление игроком
        for unit in self.units:
            unit.on_key_press(key, modifiers)

        # Выстрел при нажатии SPACE
        if key == self.shoot_key:
            # Создаем атаку от игрока к курсору мыши или к боссу
            attack = Atacs(
                width=self.width,
                height=self.height,
                start_x=self.player.pos_x,
                start_y=self.player.pos_y,
                end_x=self.boss.pos_x,  # Можно заменить на позицию курсора
                end_y=self.boss.pos_y,
                color=arcade.color.BLACK,
                line_width=5,
                speed=15,
                damage=10
            )
            self.attacks.append(attack)

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

        # Клавиши управления для этого объекта
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

        # Флаги движения
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        # Устанавливаем позицию
        if pos_x is None:
            self.pos_x = width // 2
        else:
            self.pos_x = pos_x

        if pos_y is None:
            self.pos_y = height // 2
        else:
            self.pos_y = pos_y

        self.radius = radius
        self.color = color
        self.speed = speed

    def draw(self):
        arcade.draw_circle_filled(self.pos_x, self.pos_y, self.radius, self.color)

    def update(self):
        # Двигаем в зависимости от нажатых клавиш
        if self.up and self.pos_y < self.height - self.radius:
            self.pos_y += self.speed
        if self.down and self.pos_y > self.radius:
            self.pos_y -= self.speed
        if self.left and self.pos_x > self.radius:
            self.pos_x -= self.speed
        if self.right and self.pos_x < self.width - self.radius:
            self.pos_x += self.speed

        # Добавляем границы экрана
        self.pos_x = max(self.radius, min(self.pos_x, self.width - self.radius))
        self.pos_y = max(self.radius, min(self.pos_y, self.height - self.radius))

    def on_key_press(self, key, modifiers):
        # Проверяем, соответствуют ли нажатые клавиши нашим клавишам управления
        if key == self.up_key:
            self.up = True
        elif key == self.down_key:
            self.down = True
        elif key == self.left_key:
            self.left = True
        elif key == self.right_key:
            self.right = True

    def on_key_release(self, key, modifiers):
        # Проверяем, соответствуют ли отпущенные клавиши нашим клавишам управления
        if key == self.up_key:
            self.up = False
        elif key == self.down_key:
            self.down = False
        elif key == self.left_key:
            self.left = False
        elif key == self.right_key:
            self.right = False


class Atacs:
    def __init__(self, width=800, height=800, start_x=None, start_y=None,
                 end_x=None, end_y=None, color=arcade.color.GOLD,
                 line_width=3, speed=10, damage=20, max_distance=400):
        """
        start_x, start_y: начальная точка атаки
        end_x, end_y: конечная точка (куда целится атака)
        speed: скорость движения луча
        max_distance: максимальная дистанция полета
        """
        self.width = width
        self.height = height

        # Начальная позиция
        self.start_x = start_x if start_x is not None else width // 2
        self.start_y = start_y if start_y is not None else height // 2

        # Конечная позиция (цель)
        self.target_x = end_x if end_x is not None else width
        self.target_y = end_y if end_y is not None else height

        # Текущая позиция конца луча (начинается с начальной позиции)
        self.current_x = self.start_x
        self.current_y = self.start_y

        # Вектор направления
        dx = self.target_x - self.start_x
        dy = self.target_y - self.start_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Нормализуем вектор направления
        if distance > 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance
        else:
            self.direction_x = 0
            self.direction_y = 0

        # Параметры
        self.color = color
        self.line_width = line_width
        self.speed = speed
        self.damage = damage
        self.max_distance = max_distance
        self.distance_traveled = 0

        # Состояние
        self.active = True
        self.reached_target = False

        # Конечная точка в направлении выстрела
        self.final_x = self.start_x + self.direction_x * self.max_distance
        self.final_y = self.start_y + self.direction_y * self.max_distance

    def draw(self):
        """Отрисовка луча от начальной точки к текущей позиции конца луча"""
        if self.active:
            arcade.draw_line(self.start_x, self.start_y,
                             self.current_x, self.current_y,
                             self.color, self.line_width)

    def update(self, delta_time):
        """Обновление позиции луча"""
        if not self.active or self.reached_target:
            return

        # Двигаем конец луча в направлении цели
        self.current_x += self.direction_x * self.speed
        self.current_y += self.direction_y * self.speed
        self.distance_traveled += self.speed

        # Проверяем, достигли ли мы цели или максимальной дистанции
        distance_to_target = math.sqrt(
            (self.current_x - self.target_x) ** 2 +
            (self.current_y - self.target_y) ** 2
        )

        # Если достигли цели или пролетели максимальную дистанцию
        if (distance_to_target < self.speed or
                self.distance_traveled >= self.max_distance or
                self.current_x < 0 or self.current_x > self.width or
                self.current_y < 0 or self.current_y > self.height):
            self.reached_target = True
            # Убрал time.sleep() - он блокирует поток
            # Вместо этого можно добавить таймер для исчезновения

    def is_active(self):
        """Проверка, активна ли еще атака"""
        return self.active and not self.reached_target

    def deactivate(self):
        """Деактивировать атаку"""
        self.active = False


def main():
    game = MyGame(800, 800, 'GAME')
    arcade.run()


if __name__ == "__main__":
    main()