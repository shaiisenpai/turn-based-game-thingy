import random


class Character:
    def __init__(self, name, hp, atk, spd):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd

    def attack(self, target):
        self.deal_damage(target, self.atk)

    def is_alive(self):
        return self.hp > 0 

    def take_damage(self, damage):
        if self.is_alive():
            self.hp = max(0, self.hp - damage)
            print(f"{self.name}は{damage}ダメージを受けた。")
            print(f"{self.name}のHPは残り{self.hp}です。")

            if not self.is_alive():
                print(f"{self.name}は倒れた。")

    def deal_damage(self, target, damage):
        if self.is_alive():
            print(f"{self.name}の攻撃！")
            target.take_damage(damage)




class Warrior(Character):
    def smash(self, target):
        smash_damage = self.atk*2
        smash_hp_consumption = self.hp//5

        self.deal_damage(target, smash_damage)
        self.take_damage(smash_hp_consumption)

    def uproar(self, party, enemies):
        uproar_damage = self.atk*3
        uproar_hp_consumption = self.hp//5

        for unit in enemies:
            self.deal_damage(unit, uproar_damage)

        for member in party:
            member.take_damage(uproar_hp_consumption)




class Mage(Character):
    def __init__(self, name, hp, atk, spd, mp):
        self.max_mp = mp
        super().__init__(name, hp, atk, spd)
        self.mp = mp

    def flame(self, target):
        flame_damage = self.atk*3
        flame_mp = 50

        if self.cast_spell(flame_mp):
            self.deal_damage(target, flame_damage)
        
    def concentrate(self): # MPを回復する行動
        mp_gain = 50
        if self.is_alive():
            self.mp = min(self.max_mp, self.mp + mp_gain)
            print(f"MPを{mp_gain}回復した。現在の{self.name}のMPは{self.mp}です。")

    def cast_spell(self, cost):
        if not self.is_alive():
            return False
        else:
            if self.mp >= cost:
                self.mp = max(0, self.mp - cost)
                print(f"{self.name}はMPを{cost}消費した。現在の{self.name}のMPは{self.mp}です。")
                return True
            else:
                print(f"MPが足りない！")
                return False




class Enemy(Character):
    def __init__(self, name, hp, atk, spd):
        super().__init__(name, hp, atk, spd)




class Battle:
    def __init__(self, party, enemies):
        self.party = party
        self.enemies = enemies
        self.turn_count = 1

    def next_turn(self):
        print(f"----- Turn {self.turn_count} Start! -----")

        units = self.get_alive_units(self.party + self.enemies)
        self.action_order(units)
        for unit in units:
            if self.is_battle_continuing():
                if not unit.is_alive():
                    continue
                if unit in self.party:
                    self.player_turn(unit)
                else:
                    self.enemy_turn(unit)


        self.display_result()
        self.turn_count += 1


    def player_turn(self, unit):
        print(f"{unit.name}の行動！")

        action = self.select_action(unit)

        if action == "attack":
            target = self.select_target(self.enemies)
            unit.attack(target)

        if action == "flame":
            target = self.select_target(self.enemies)
            unit.flame(target)

        if action == "concentrate":
            unit.concentrate()

        if action == "smash":
            target = self.select_target(self.enemies)
            unit.smash(target)

        if action == "uproar":
            unit.uproar(self.party, self.enemies)

    def select_action(self, unit):
        while True:
            if isinstance(unit, Mage):
                print("1.通常攻撃")
                print("2.フレイム")
                print("3.集中")

            if isinstance(unit, Warrior):
                print("1.通常攻撃")
                print("2.スマッシュ")
                print("3.大暴れ")

            command = input("コマンドを入力してください: ")

            if command == "1".lower():
                return "attack"

            if isinstance(unit, Mage):
                if command == "2".lower():
                    return "flame"
                elif command == "3".lower():
                    return "concentrate"

            if isinstance(unit, Warrior):
                if command == "2".lower():
                    return "smash"
                elif command == "3".lower():
                    return "uproar"

            print("正しい番号を入力してください。")

    def select_target(self, targets):
        alive_targets = self.get_alive_units(targets)

        while True:
            print("攻撃対象を選んでください。")

            for index, target in enumerate(alive_targets, start=1):
                print(f"{index}: {target.name} | HP: {target.hp}")

            command = input("対象の番号: ")

            if command.isdigit():
                target_index = int(command) - 1

                if 0 <= target_index <= len(alive_targets):
                    return alive_targets[target_index]

            print("正しい番号を入力してください。")


    def enemy_turn(self, unit):

        alive_target = self.get_alive_units(self.party)

        if not alive_target:
            return

        target = random.choice(alive_target)
        unit.attack(target)
        

    def action_order(self, units):
        units.sort(
            key = lambda unit: unit.spd,
            reverse = True
        )

    def get_alive_units(self, units):
        return [
            unit for unit in units
            if unit.is_alive()
        ]

    def display_result(self):
        if not self.get_alive_units(self.enemies):
            print("----- Victory! -----")
        if not self.get_alive_units(self.party):
            print("----- Defeat... -----")

    def is_battle_continuing(self):
        return self.get_alive_units(self.enemies) and self.get_alive_units(self.party)




Enemy1 = Enemy("Maou", 100, 100, 150)
Enemy2 = Enemy("Slime", 100, 40, 50)
Ally1 = Mage("Lala", 200, 40, 80, 100)
Ally2 = Warrior("Zeta", 300, 80, 100)

party = [Ally1, Ally2]
enemies = [Enemy1, Enemy2]

Battle_Manager = Battle(party, enemies)

while Battle_Manager.is_battle_continuing():
    Battle_Manager.next_turn()