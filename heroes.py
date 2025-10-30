import random
from monsters import MonsterBerserk, MonsterHunter


class Hero:
    # Базовый класс, который не подлежит изменению
    # У каждого наследника будут атрибуты:
    # - Имя
    # - Здоровье
    # - Сила
    # - Жив ли объект
    # Каждый наследник будет уметь:
    # - Атаковать
    # - Получать урон
    # - Выбирать действие для выполнения
    # - Описывать своё состояние

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        return self.__hp

    def set_hp(self, new_value):
        self.__hp = max(new_value, 0)

    def get_power(self):
        return self.__power

    def set_power(self, new_power):
        self.__power = new_power

    def is_alive(self):
        return self.__is_alive

    # Все наследники должны будут переопределять каждый метод базового класса (кроме геттеров/сеттеров)
    # Переопределенные методы должны вызывать методы базового класса (при помощи super).
    # Методы attack и __str__ базового класса можно не вызывать (т.к. в них нету кода).
    # Они нужны исключительно для наглядности.
    # Метод make_a_move базового класса могут вызывать только герои, не монстры.
    def attack(self, target):
        # Каждый наследник будет наносить урон согласно правилам своего класса
        raise NotImplementedError("Вы забыли переопределить метод Attack!")

    def take_damage(self, damage):
        # Каждый наследник будет получать урон согласно правилам своего класса
        # При этом у всех наследников есть общая логика, которая определяет жив ли объект.
        print("\t", self.name, "Получил удар с силой равной = ", round(damage), ". Осталось здоровья - ", round(self.get_hp()))
        # Дополнительные принты помогут вам внимательнее следить за боем и изменять стратегию, чтобы улучшить выживаемость героев
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        # С каждым днём герои становятся всё сильнее.
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        # Каждый наследник должен выводить информацию о своём состоянии, чтобы вы могли отслеживать ход сражения
        raise NotImplementedError("Вы забыли переопределить метод __str__!")


class Healer(Hero):
    """
    Дочерний класс наследуется от базового класса Hero.

    Args:
        magic_power(int): магическая сила.

    Methods:
        attack: атака заданной цели.
        take_damage: получение урона от врага.
        healing: исцеление союзников.
        make_a_move: делает один ход в игре, атакует врага или исцеляет союзника.
    """

    def __init__(self, name):
        super().__init__(name)
        self.magic_power = self.get_power() * 3

    def attack(self, target):
        damage = self.get_power() / 2
        target.take_damage(damage)
        print(f'{self.name} нанёс {damage} урона монстру {target.name}')

    def take_damage(self, damage):
        damage_special = 1.2 * damage
        self.set_hp(self.get_hp() - damage_special)
        super().take_damage(damage_special)

    def healing(self, target):
        target.set_hp(target.get_hp() + self.magic_power)
        print(f'{target.name} получил {self.magic_power} очков здоровья')

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        target_of_potion = friends[0]
        min_health = target_of_potion.get_hp()
        
        for friend in friends:
            if friend.get_hp() < min_health:
                target_of_potion = friend
                min_health = target_of_potion.get_hp()

        if min_health < 60:
            print("Исцеляю", target_of_potion.name)
            self.healing(target_of_potion)
        else:
            target_monster = enemies[0]
            min_health = target_monster.get_hp()

            for enemie in enemies:
                if enemie.get_hp() < min_health:
                    target_monster = enemie
                    min_health = target_monster.get_hp()
            print("Атакую монстра с низким здоровьем -", target_monster.name)
            self.attack(target_monster)
        print('\n')

    def __str__(self):
        return 'Name: {0} | HP: {1}'.format(self.name, self.get_hp())


class Tank(Hero):
    """
       Дочерний класс наследуется от базового класса Hero.

       Args:
           defence(int): индекс защиты
           shield(bool): показывет активирован щит или нет.

       Methods:
           attack: атака заданной цели.
           take_damage: получение урона от врага.
           up_shield: активация щита.
           down_shield: деактивация щита
           make_a_move: делает один ход в игре, атакует врага или исцеляет союзника.
       """
    def __init__(self, name):
        super().__init__(name)
        self.defense = 1
        self.shield = False

    def attack(self, target):
        damage = self.get_power() / 2
        target.take_damage(damage)
        print(f'{self.name} нанёс {damage} урона монстру {target.name}')

    def take_damage(self, damage):
        damage_special = damage/self.defense
        self.set_hp(self.get_hp() - damage_special)
        super().take_damage(damage_special)

    def up_shield(self):
        if not self.shield:
            self.shield = True
            self.defense *= 2
            self.set_power(self.get_power() / 2)
        print(f'{self.name} поднял щит. Показатель брони увеличился в 2 раза. Показатель силы уменьшился в 2 раза')

    def down_shield(self):
        if self.shield:
            self.shield = False
            self.defense /= 2
            self.set_power(self.get_power() * 2)
        print(f'{self.name} опустил щит. Показатель брони уменьшился в 2 раза. Показатель силы увеличился в 2 раза')

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')

        target_of_potion = enemies[0]
        min_health = target_of_potion.get_hp()
        for enemie in enemies:
            if enemie.get_hp() < min_health:
                target_of_potion = enemie
                min_health = target_of_potion.get_hp()

        if min_health < 20 and self.shield:
            self.down_shield()
            print("Атакую монстра", target_of_potion.name)
            self.attack(target_of_potion)
        else:
            if isinstance(target_of_potion, MonsterHunter):
                self.up_shield()
            print('Поднимаю щит перед монстром', target_of_potion.name)
        print('\n')

    def __str__(self):
        return 'Name: {0} | HP: {1}'.format(self.name, self.get_hp())


class Attacker(Hero):
    """
          Дочерний класс наследуется от базового класса Hero.

          Args:
              power_multiply(int): коэффициент усиления урона.

          Methods:
              attack: атака заданной цели.
              take_damage: получение урона от врага.
              power_up: увеличние урона на 2х.
              power_down: уменьшение урона на 2х
              make_a_move: делает один ход в игре, атакует врага или исцеляет союзника.
          """

    def __init__(self, name):
        super().__init__(name)
        self.power_multiply = 1 # коэффициент усиления урона

    def attack(self, target):
        damage = self.get_power() * self.power_multiply
        target.take_damage(damage)
        self.power_down()
        print(f'{self.name} нанёс {damage} урона монстру {target.name}')

    def take_damage(self, damage):
        damage_special = damage * (self.power_multiply / 2)
        self.set_hp(self.get_hp() - damage_special)
        super().take_damage(damage_special)

    def power_up(self):
        self.power_multiply *= 2

    def power_down(self):
        self.power_multiply /= 2

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')

        target_monster = None
        for enemie in enemies:
            if isinstance(enemie, MonsterBerserk) or isinstance(enemie, MonsterHunter):
                target_monster = enemie
                break
        if target_monster:
            print(f'Атакую монстра - {target_monster.name}')
            self.power_up()
            self.attack(target_monster)
        else:
            print('Монстр класса Берсерк или Охотник не найдены')
        print('\n')

    def __str__(self):
        return 'Name: {0} | HP: {1}'.format(self.name, self.get_hp())




