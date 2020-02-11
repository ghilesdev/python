class Ennemy:
    hp = 200

    def __init__(self, hp, mp):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp

    def gethp(self):
        return self.hp
