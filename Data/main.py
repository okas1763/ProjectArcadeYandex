from database import Boss, Player
import arcade
import random
import math
import json


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.PINK)

    def on_draw(self):
        self.clear()

    def update(self, delta_time):
        # Логика обновления игры
        pass


class BD(Boss, Player):
    def __init__(self):
        # Вызываем конструкторы обоих родительских классов
        Boss.__init__(self)
        Player.__init__(self)

        print(f"Урон игрока: {Player.get_damag(self)}")
        print(f"Имя босса: {Boss.get_name(self)}")
        print(f"HP босса: {Boss.get_hp(self)}")
        print(f"HP игрока: {Player.get_hp(self)}")
        print(f'Скорость босса {Boss.get_speed(self)}')
        print(f'Скорость игрока {Player.get_speed(self)}')


def main():
    game = MyGame(800, 800, "GAME")
    x = BD()

    arcade.run()


if __name__ == "__main__":
    main()