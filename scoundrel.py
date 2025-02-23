# Play a game of Scoundrel. A roguelike played with a standard 52 card deck
# Author: Dondre Trotman
# Date: 2025-02-23
# Version: 2

# Changelog
# | version | date       | notes                                     |
# |---------|------------|-------------------------------------------|
# | 1       | 2025-02-22 | First release                             |
# | 2       | 2025-02-23 | Implement run and proper rooms.           |
# |         |            | Probably final unless there are bugs.     |

#import modules
import random, os, sys, subprocess

#### INITIAL SET UP ####
# variable list
health = 20 #health starts at 20
fightresult = 0 #result of a fight
weapon = 0 #weapon value
maxweapon = 0 #equal to value of last monster fought with a weapon
heart = 0 #heart value
point = 0	#points to randomly selected card in the deck
roomcnt = 0	#counts the used cards in a room
cardsleft = 40 #count of cards left
healed = 0	#tracks when last healed
ran = 0		#tracks when last ran
spades = ["2♠","3♠","4♠","5♠","6♠","7♠","8♠","9♠","10♠","J♠","Q♠","K♠","A♠"]
clubs = ["2♣","3♣","4♣","5♣","6♣","7♣","8♣","9♣","10♣","J♣","Q♣","K♣","A♣"]
diamonds = ["2♦","3♦","4♦","5♦","6♦","7♦","8♦","9♦","10♦"]
hearts = ["2♥","3♥","4♥","5♥","6♥","7♥","8♥","9♥","10♥"]

#set up card matrix
deck = ["2♠","3♠","4♠","5♠","6♠","7♠","8♠","9♠","10♠","J♠","Q♠","K♠","A♠",
		"2♣","3♣","4♣","5♣","6♣","7♣","8♣","9♣","10♣","J♣","Q♣","K♣","A♣",
		"2♦","3♦","4♦","5♦","6♦","7♦","8♦","9♦","10♦",
		"2♥","3♥","4♥","5♥","6♥","7♥","8♥","9♥","10♥"]

#create card array
room = ["X","X","X","X"]

#### FUNCTIONS ####
#clear screen between plays
def ClearScreen():
	#print("\033[H\033[3J")		#ANSI codes to clear the screen (looks messy)
	if os.name in ('linux', 'osx', 'posix'):
		subprocess.call("clear")
	elif os.name in ('nt', 'dos'):
		subprocess.call('cls')
	else:
		print("\n") * 120
	return


# function to deal cards
def Deal(room):
	global point
	global cardsleft
	global healed
	global ran
	healed = 0		#reset healing ability
	ran = ran - 1	#cooldown ruun
	for i in range(len(room)):
		if room[i] == "X" and len(deck) > 0:		#replace only "X" values
			while True:
				maxindex = len(deck) - 1
				point = random.randint(0,maxindex)
				room[i] = deck[point]		#keep track of dealt cards
				del deck[point]				#remove card from deck
				#room[i] = play[point]
				cardsleft = len(deck)
				break
	return room[i]

# function to run from a room
def Run():
	global room
	global deck
	global ran
	if ran <= 0 and "X" not in room:	#can only run if didn't run in previous room or haven't started playing this room
		for i in range(len(room)):
			deck.append(room[i])	#put room cards back into deck
			#break
		room = ["X","X","X","X"]		#reset room
		Deal(room)		#deal a new room
		ran = 2		#set run countdown so that you can't run from consecutive rooms
	return 

# function to fight
def Fight(card):
	global weapon
	global health
	global fightresult
	global maxweapon
	global room
	if card in spades: enemy = spades.index(card) + 2		#get enemy strength
	elif card in clubs: enemy = clubs.index(card) + 2 
	if maxweapon < enemy: 
		fightresult = enemy		#enemy bypasses weapon if stronger than las enemy
	else: 
		fightresult = enemy - weapon
		maxweapon = enemy
	if fightresult < 0: fightresult = 0		#enemy can't deal degative damage
	health = health - fightresult
	x = room.index(card)
	room[x] = "X"		#discard card
	return health

# function to heal
def Heal(card):
	global health
	global healed
	if healed <= 0:		#only heal if did not heal in current room
		life = hearts.index(card) + 2 
		if life + health > 20: health=20
		else: health = life + health
	x = room.index(card)
	room[x] = "X"		#discard card
	healed = 1
	return

#function to equip weapon
def Equip(card):
	global weapon
	global maxweapon
	weapon = diamonds.index(card) + 2		#get weapon strength
	maxweapon = 14
	x = room.index(card)
	room[x] = "X"		#discard card
	return weapon

def CheckEnd():
	global roomcnt
	if health <= 0:
		sys.exit("You lose!!!")
		return 2
	elif len(deck) <= 0 and roomcnt >= 3:
		sys.exit("YOU WIN!!! YAY!!!!!")
		return 1
	else:
		return 0

#get valid input
def GetInput():
	global roomcnt
	while True:
		user_input = input().strip()
		if user_input.isdigit():
			num = int(user_input)
			if 0 <= num <= 4:
				return num
		ClearScreen()
		print("Weapon = ", weapon, "     Max Weapon = ", maxweapon,"    Health = ", health,"    Cards Left = ", cardsleft)
		print("Only choose valid card from 1 - 4, or 0 to run")
		print(room[0], room[1], room[2], room[3])
		if roomcnt <= 0: print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3]+"\n0 = Run")
		elif roomcnt > 0: print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3]+"\n")

while CheckEnd() == 0:
	ClearScreen()
	print("Weapon = ", weapon, "     Max Weapon = ", maxweapon,"    Health = ", health,"    Cards Left = ", cardsleft)
	roomcnt = room.count("X")
	if roomcnt >= 3:		#deal new room if there is one card left
		print("Dealing cards...")
		Deal(room)		#deal cards to room
	else: print("")
	print(room[0], room[1], room[2], room[3])
	roomcnt = room.count("X")
	if roomcnt  <= 0: print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3]+"\n0 = Run")
	elif roomcnt > 0 : print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3]+"\n")
	choice = GetInput()
	card = room[choice-1]
	if choice == 0: Run()
	elif card in diamonds: weapon = Equip(card)
	elif card in hearts: Heal(card)
	elif card in spades or card in clubs: Fight(card)
