import random


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class person:
    def __init__(self, hp, mp, atk, df, magic):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.action = ["attack", "magic"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def generate_spell_damage(self, i):
        mgl = self.magic[i]["damage"] - 5
        mgh = self.magic[i]["damage"] + 5
        return random.randrange(mgl, mgh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_spell_name(self, i):
        return self.magic[i]["name"]

    def spell_mp_cost(self, i):
        return self.magic[i]["cost"]

    def choose_action(self):
        i = 1
        print("action")
        for item in self.action:
            print(str(i), ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("magic")
        for spell in self.magic:
            print(str(i), ":", spell["name"], "cost: ", str(spell["cost"]))
            i += 1
