from classes.game import person, bcolors


magic=[{"name":"fire", "cost":10,"damage":100},
       {"name":"thunder", "cost":10,"damage":120},
       {"name":"blizzard", "cost":10,"damage":140}]
player=person(460,65,60,30,magic)
ennemy=person(1200,65,45,35,magic)

run=True
i=0
print(bcolors.FAIL+bcolors.BOLD+"ennemy attacks!"+bcolors.ENDC)

while run:

    print("=========================")
    player.choose_action()
    choice=input("choose action")
    index =int(choice)-1
    if index==0:
        dmg=player.generate_damage()
        ennemy.take_damage(dmg)
        print("you attacked for :", dmg,"point of damage. Ennemy's HP :", ennemy.get_hp())

    elif index==1:
        player.choose_magic()
        magic_choice=int(input("choose magic spell"))-1
        magic_dmg=player.generate_spell_damage(magic_choice)
        spell=player.get_spell_name(magic_choice)
        cost=player.spell_mp_cost(magic_choice)
        current_mp=player.get_mp()
        if cost>current_mp:
            print(bcolors.FAIL+"\n not ennoutgh mp"+bcolors.ENDC)
            continue
        player.reduce_mp(cost)
        ennemy.take_damage(magic_dmg)
        print(bcolors.OKBLUE+"\n "+spell+" deals ", str(magic_dmg), "points of damage  Ennemy's HP :", str(ennemy.get_hp())+bcolors.ENDC)


    ennemy_choice=1
    ennemy_dmg  =ennemy.generate_damage()
    player.take_damage(ennemy_dmg)
    print("Ennemy attacks for :",ennemy_dmg,"points of damages, your HP is: ", player.get_hp())

    if ennemy.get_hp()==0:
        print(bcolors.OKGREEN+"you win"+bcolors.ENDC)
        run==False

    elif player.get_hp()==0:
        print(bcolors.FAIL+"busted"+bcolors.ENDC)
        run=False





