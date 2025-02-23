# Play a game of Scoundrel. A roguelike played with a standard 52 card deck
# Author: Dondre Trotman
# Date: 2025-02-22
# Version: 1

# Changelog
# | version | date       | notes         |
# |---------|------------|---------------|
# | 1       | 2025-02-22 | first release |

#import modules
import random, os, sys, subprocess

#### INITIAL SET UP ####
# variable list
health = 20 #health starts at 20
fightresult = 0 #result of a fight
weapon = 0 #weapon value
maxweapon = 0 #equal to value of last monster fought with a weapon
heart = 0 #heart value
monster = 0 # monster value
point = 0	#points to randomly selected card in the deck
cardsleft = 40 #count of cards left
healcnt = 0	#tracks when last healed
spades = ["2♠","3♠","4♠","5♠","6♠","7♠","8♠","9♠","10♠","J♠","Q♠","K♠","A♠"]
clubs = ["2♣","3♣","4♣","5♣","6♣","7♣","8♣","9♣","10♣","J♣","Q♣","K♣","A♣"]
diamonds = ["2♦","3♦","4♦","5♦","6♦","7♦","8♦","9♦","10♦"]
hearts = ["2♥","3♥","4♥","5♥","6♥","7♥","8♥","9♥","10♥"]

#set up card matrix
deck = ["2♠","3♠","4♠","5♠","6♠","7♠","8♠","9♠","10♠","J♠","Q♠","K♠","A♠",
		"2♣","3♣","4♣","5♣","6♣","7♣","8♣","9♣","10♣","J♣","Q♣","K♣","A♣",
		"2♦","3♦","4♦","5♦","6♦","7♦","8♦","9♦","10♦",
		"2♥","3♥","4♥","5♥","6♥","7♥","8♥","9♥","10♥"]

#cards that have been selected
play = ["0","0","0","0","0","0","0","0","0","0","0","0","0",
		"0","0","0","0","0","0","0","0","0","0","0","0","0",
		"0","0","0","0","0","0","0","0","0",
		"0","0","0","0","0","0","0","0","0"]

#create card array
room = ["X","X","X","X"]

#### FUNCTIONS ####
#clear screen between plays
def ClearScreen():
	#os.system('cls' if os.name=='nt' else 'clear')
	#print("\033[H\033[3J")		#ANSI codes to clear the screen
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
	global healcnt
	healcnt = healcnt - 1
	for i in range(len(room)):
		if room[i] == "X":		#replace only "X" values (indent the rest of the function if uncommenting)
			while True:
				maxindex = len(deck) - 1
				point = random.randint(0,maxindex)
				play[point] = deck[point]		#keep track of dealt cards
				del deck[point]				#remove card from deck
				room[i] = play[point]
				cardsleft = len(deck)
				break
	return play[point]

# function to run from a room
def Run():
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
	if healcnt <= 0:		#only heal if did not heal in last turn
		life = hearts.index(card) + 2 
		if life + health > 20: health=20
		else: health = life + health
	x = room.index(card)
	room[x] = "X"		#discard card
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
	if health <= 0:
		sys.exit("You lose!!!")
		return 2
	elif len(deck) <= 0:
		sys.exit("YOU WIN!!! YAY!!!!!")
		return 1
	else:
		return 0

#get valid input
def GetInput():
	while True:
		user_input = input().strip()
		if user_input.isdigit():
			num = int(user_input)
			if 1 <= num <= 4:
				return num
		ClearScreen()
		print("Weapon = ", weapon, "     Max Weapon = ", maxweapon,"    Health = ", health,"    Cards Left = ", cardsleft)
		print("Dealing cards...")
		print(room[0], room[1], room[2], room[3])
		print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3])

while CheckEnd() == 0:
	ClearScreen()
	print("Weapon = ", weapon, "     Max Weapon = ", maxweapon,"    Health = ", health,"    Cards Left = ", cardsleft)
	print("Dealing cards...")
	Deal(room)		#deal cards to room
	print(room[0], room[1], room[2], room[3])
	print("Choose a card\n1 = "+room[0]+"\n2 = "+room[1]+"\n3 = "+room[2]+"\n4 = "+room[3])
	choice = GetInput()
	card = room[choice-1]
	if card in diamonds: weapon = Equip(card)
	elif card in hearts: 
		Heal(card)
		healcnt = 2
	elif card in spades or card in clubs: Fight(card)
