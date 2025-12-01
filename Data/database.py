import json

class Boss:
    def __init__(self):
        with open('Base/specifications.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.boss = data['BOSS']
        self.hp = self.boss.get('HP')
        self.speed = self.boss.get('SPEED')
        self.name = self.boss.get('NAME')

    def up_hp(self, num):
        """Увеличить HP"""
        self.hp += num
        self.boss['HP'] = self.hp
        return self.hp

    def down_hp(self, num):
        """Уменьшить HP"""
        self.hp = max(0, self.hp - num)
        self.boss['HP'] = self.hp
        return self.hp

    def edit_hp(self, new_hp):
        """Установить конкретное значение HP"""
        self.hp = max(0, new_hp)
        self.boss['HP'] = self.hp
        return self.hp

    def get_hp(self):
        """Получить текущее HP"""
        return self.hp

    def get_name(self):
        """Получить имя босса"""
        return self.name

    def edit_name(self, name):
        """Изменить имя босса"""
        self.name = name
        self.boss['NAME'] = name
        return self.name

    def get_speed(self):
        """Получить скорость"""
        return self.speed

    def edit_speed(self, speed):
        """Изменить скорость"""
        self.speed = speed
        self.boss['SPEED'] = speed
        return self.speed

    def __str__(self):
        return f"Boss {self.name}: HP={self.hp}, Speed={self.speed}"


class Player:

    def __init__(self):
        with open('Base/specifications.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.player = data['PLAYER']
        self.hp = self.player.get('HP')
        self.speed = self.player.get('SPEED')
        self.damag = self.player.get('DAMAG')

    def up_hp(self, num):
        """Увеличить HP"""
        self.hp += num
        self.player['HP'] = self.hp
        return self.hp

    def down_hp(self, num):
        """Уменьшить HP"""
        self.hp = max(0, self.hp - num)
        self.player['HP'] = self.hp
        return self.hp

    def edit_hp(self, hp):
        """Установить конкретное значение HP"""
        self.hp = max(0, hp)
        self.player['HP'] = self.hp
        return self.hp

    def get_hp(self):
        """Получить текущее HP"""
        return self.hp

    def up_damag(self, num):
        """Увеличить дамага"""
        self.damag += num
        self.player['DAMAG'] = self.damag
        return self.damag

    def down_damag(self, num):
        """Уменьшить дамаг"""
        self.damag = max(0, self.damag - num)
        self.player['DAMAG'] = self.damag
        return self.damag

    def get_damag(self):
        """Получить дамаг"""
        return self.damag

    def edit_damag(self, damag):
        """Изменить силу дамага"""
        self.damag = damag
        self.player['DAMAG'] = damag
        return self.damag

    def get_speed(self):
        """Получить скорость"""
        return self.speed

    def edit_speed(self, speed):
        """Изменить скорость"""
        self.speed = speed
        self.player['SPEED'] = speed
        return self.speed


    def __str__(self):
        return f" Your specifications, Damage {self.damag}: HP={self.hp}, Speed={self.speed}"



