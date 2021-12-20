#imports
from blessed import Terminal
from threading import Thread
import keyboard
import os
import random
import time

#resizing terminal
term = Terminal()
os.system('mode 41, 26')
while True:
	#the text
	ground = f'{term.yellow}#{term.normal}'
	wall = f'{term.green3}#{term.normal}'
	grass = f'{term.olivedrab1}#{term.normal}'
	bird = f'{term.bright_yellow}O{term.normal}'

	#pre-game variables
	background = ((' '*40+'\n')*22) + ('e'*40)+'\n' + (('g'*40+'\n')*2)[:-1]
	pipes = []
	side_stuff = []
	frame = -10
	player, vert, jump, fall = 10, -3, -2, -1
	score = 0
	ded = False

	#starting screen
	stuff = [list(i) for i in background.split('\n')]
	stuff[10][10] = bird
	print('\n'.join([''.join(i) for i in stuff]).replace('g',ground).replace('e',grass))
	print(term.move_up(26))
	print('\n'*11+f'{term.bright_yellow}Flappy Bird'.center(45)+'\n'+f'{term.bright_cyan}Press space to start'.center(45)+'\n'*11)
	keyboard.wait('space')

	#jumping thread, checking if its pressed is a little too much
	def wait():
		global vert,jump,killll
		while True:
			try:
				keyboard.wait('space')
			except:
				break
			vert = jump
	Thread(target=wait).start()

	#game loop starts
	while True:
		#term.move_up, genius function that can replace text on screen super fast
		print(term.move_up(27))
		frame += 1
		stuff = [list(i) for i in background.split('\n')]

		#adding to the pipes, and the small bit at the 2 sides
		if frame % 30 == 0:
			y = random.randint(1,15)
			pipes.append({'x':40,'y':y,'f':True})
			pipes.append({'x':41,'y':y})
			pipes.append({'x':42,'y':y})
			pipes.append({'x':43,'y':y})
			side_stuff.append({'x':44,'y':y-1})
			side_stuff.append({'x':39,'y':y-1})

		#moving the pipes
		for n,a in enumerate(pipes):
			pipes[n]['x'] -= 1
		for n,a in enumerate(side_stuff):
			side_stuff[n]['x'] -= 1

		#removing pipes that already gone through
		pipes = [i for i in pipes if i['x'] >= 0]
		side_stuff = [i for i in side_stuff if i['x'] >= 0]

		#placing the pipes
		for a in pipes:
			if a['x'] > 39: continue
			if a['x'] == 10 and 'f' in a.keys():
				score += 1
			for i in range(a['y']):
				stuff[i][a['x']] = 'w'
			for i in range(a['y']+5,22):
				stuff[i][a['x']] = 'w'
		for a in side_stuff:
			if a['x'] > 39: continue
			stuff[a['y']][a['x']] = 'w'
			stuff[a['y']+6][a['x']] = 'w'

		#plyer physics and death check
		if player + vert//2 > 21:
			stuff[21][10] = 'O'
			print('\n'.join([''.join(i) for i in stuff]).replace('w',wall).replace('g',ground).replace('O',bird).replace('e',grass))
			break

		if vert//2 > 0:
			for i in range(vert//2):
				player += 1
				if player >= 0 and stuff[player][10] == 'w':
					player -= 1
					ded = True
					break
		if vert//2 < 0:
			for i in range(vert//2,0):
				player -= 1
				if player >= 0 and stuff[player][10] == 'w':
					player += 1
					ded = True
					break

		if player < 0 and stuff[0][11] == 'w':
			ded = True
		if not player < 0:
			if stuff[player][10] == 'w': stuff[player-1][10] = 'O'
			else: stuff[player][10] = 'O'
		if ded:
			print('\n'.join([''.join(i) for i in stuff]).replace('w',wall).replace('g',ground).replace('O',bird).replace('e',grass))
			break
		vert -= fall

		#updating the frame
		scorelen = len(str(score))//2
		for i in range(len(str(score))):
			stuff[3][20-scorelen+i] = f'{term.bright_cyan}{str(score)[i]}{term.normal}'
		print('\n'.join([''.join(i) for i in stuff]).replace('w',wall).replace('g',ground).replace('O',bird).replace('e',grass))
		time.sleep(.07)

	#death screen
	print(term.move_up(14)+term.move_right(16)+f'{term.bright_red}You Died'+term.move_down(1)+'\r',term.move_right(7)+'Press space to continue...'+term.move_up(9)+'\r'+term.move_right(20 - (len(str(score))//2))+f'{term.bright_cyan}{str(score)}{term.normal}')
	keyboard.wait('space')