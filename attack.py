"""import  random

playerhp=260
ennemyatkl=60
ennemyatkh=80

class Ennemy:
    hp=200
    def __init__(self, atkl, atkh):
        self.atkl=atkl
        self.atkh=atkh



    def getatk(self):
        print(self.atkl)
    def gethp(self):
        print("hp is ", self.hp)
ennemuone=Ennemy(40,50)
ennemytwo=Ennemy(50,80)
ennemuone.getatk()
ennemuone.gethp()




while playerhp>0:
    dmg=random.randrange(ennemyatkl,ennemyatkh)
    playerhp-=dmg
    if playerhp<=30:
        playerhp=30
    print("enemy trike for",dmg,"point of damage, current hp is ", playerhp)
    if playerhp>30:
        continue

    print("you have low health")
    break

 """
from classes.Ennemy import Ennemy

ennemy = Ennemy(50, 60)
print("Hp ", ennemy.gethp())
