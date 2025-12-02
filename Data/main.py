from database import Boss, Player
import arcade
import random
import math
import json


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.PINK)

        # Создаем игрока и босса с разными условиями
        self.player = Units(
            width, height,
            100, 100,
            30, arcade.color.BLUE,
            speed=5,
            up_key=arcade.key.W,
            down_key=arcade.key.S,
            left_key=arcade.key.A,
            right_key=arcade.key.D
        )

        self.boss = Units(
            width, height,
            width / 2, height / 2,
            80, arcade.color.RED,
            speed=0,
        )

        # Список всех обектов для удобного обновления
        self.units = [self.player]

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.boss.draw()

    def on_update(self, delta_time):
        # Обновляем позиции всех обектов
        for unit in self.units:
            unit.update()

    def on_key_press(self, key, modifiers):
        # Передаем нажатия клавиш всем обектов
        for unit in self.units:
            unit.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        # Передаем отпускания клавиш всем обектов
        for unit in self.units:
            unit.on_key_release(key, modifiers)


class Units:
    def __init__(self, width=800, height=800, pos_x=None, pos_y=None, radius=30,
                 color=arcade.color.LIGHT_GRAY, speed=5,
                 up_key=None, down_key=None,
                 left_key=None, right_key=None):
        self.width = width
        self.height = height

        # Клавиши управления для этого обектов
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
        self.speed = speed  # Скорость перемещения скоро реализую через json

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


class BD(Boss, Player):
    def __init__(self):
        # Вызываем конструкторы обоих родительских классов
        Boss.__init__(self)
        Player.__init__(self)


def main():
    game = MyGame(800, 800, 'GAME')
    x = BD()

    arcade.run()


if __name__ == "__main__":
    main()