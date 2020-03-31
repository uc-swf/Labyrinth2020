'''
  ___          _____     __  __
   _/    _  _ (_  | |\/|  _)  _)
  /__|_||||(_)__) | |  | __) /__

 Fachhochschule Südwestfalen
 Mechatronik/Mikrocomputer
 Prof. Dr.-Ing. Tobias Ellermeyer

  ==> SIMULATOR, verwendet Daten aus einer Datei, um Fahrt zu simulieren...

'''

#hier ein Kommentar aus master...

import pygame	# for graphics, see pygame.org
import btsim as serial


SerialPort = "BTdata_2020_03_30.txt"		
#SerialPort = "__RANDOM__"		

pygame.init()		# init graphics
pygame.display.set_caption("Zumo Distances")	# Set window title
screen = pygame.display.set_mode((640,640))		# generate screen in window

pygame.font.init()	# init font system

# define normal and small font
font = pygame.font.SysFont("comicsansms", 24)
fontsmall = pygame.font.SysFont("comicsansms", 12)

# Render "ZumoSTM32" in large, white font
text = font.render("ZumoSTM32", True, (255,255,255))

# Open Bluetooth terminal
#try:
bt = serial.Serial(SerialPort,115200)
#except:
#	print("*** ERROR *** Bluetooth could not be opened (Port=" + SerialPort +")")
#	exit()

#define some colors
lc  = pygame.Color(0,100,200)		# Chassis color
lc2 = pygame.Color(50,50,50)		# connection line color
cc  = pygame.Color(127,127,0)     	# Circle color
fc  = pygame.Color(255,255,0)		# Color of values

# define a variable to control the main loop
running = True

#------------------------------------------------
# main loop
while running:
	# event handling, gets all event from the event queue
	for event in pygame.event.get():
		# only do something if the event is of type QUIT
		if event.type == pygame.QUIT:
			# change the value to False, to exit the main loop
			running = False
	res = bt.readline()
	#print("DEBUG: Received ",res)
	data_ok = True

	# Eval received data
	try:
		# remove \r\n
		res=res.replace(b'\n',b'')
		res=res.replace(b'\r',b'')
		#print(res)
		# split the string into list
		res=res.split(b';')
		#print(res)
		# separate values
		ff=int(res[0].split()[1])
		print("Wert von ff ", ff)
		if (ff>220):	ff=220
		fl=int(res[1].split()[1])
		if (fl>220):	fl=220
		fr=int(res[2].split()[1])
		if (fr>220):	fr=220
		ll=int(res[3].split()[1])
		if (ll>220):	ll=220
		rr=int(res[4].split()[1])
		if (rr>220):	rr=220
	except:
		print("Data not ok")
		data_ok = False

	# draw if valid data received
	if (data_ok == True):
		screen.fill(pygame.Color(0,0,0))	# clear screen
		# Draw chassis
		pygame.draw.lines(screen,lc,True,[ (220,420),(220,260),(260,220),(380,220),(420,260),(420,420)],3)

		# Draw FF data
		h= 220-int(ff)
		pygame.draw.circle(screen,cc,[320,h],5)
		pygame.draw.line(screen,lc2,[320,220],[320,h])
		# Render value of FF
		lbl1 = fontsmall.render(str(ff),True,fc)
		# Blit draws rendered font onto screen
		screen.blit(lbl1, (320-lbl1.get_width()//2 ,240-lbl1.get_height()-1))	# //2 is an integer division

		# Same for FL
		h= 240-int(fl/1.41)
		pygame.draw.circle(screen,cc,[h,h],5)
		pygame.draw.line(screen,lc2,[240,240],[h,h])
		lbl1 = fontsmall.render(str(fl),True,(255,255,0))
		lbl1 = pygame.transform.rotate(lbl1, 45)	# Rotate rendered Font
		screen.blit(lbl1, (246-lbl1.get_width()//2 ,246-lbl1.get_height()//2))

		# Same for FR
		h= 400+int(fr/1.41)
		j= 240-int(fr/1.41)
		pygame.draw.circle(screen,cc,[h,j],5)
		pygame.draw.line(screen,lc2,[400,240],[h,j])
		lbl1 = fontsmall.render(str(fr),True,(255,255,0))
		lbl1 = pygame.transform.rotate(lbl1, -45)
		screen.blit(lbl1, (394-lbl1.get_width()//2 ,246-lbl1.get_height()//2))

		# Same for LL
		pygame.draw.circle(screen,cc,[220-ll,320],5)
		pygame.draw.line(screen,lc2,[220,320],[220-ll,320])
		lbl1 = fontsmall.render(str(ll),True,(255,255,0))
		screen.blit(lbl1, (240-lbl1.get_width()//2 ,320-lbl1.get_height()//2))

		# Same for RR
		pygame.draw.circle(screen,cc,[420+rr,320],5)
		pygame.draw.line(screen,lc2,[420,320],[420+rr,320])
		lbl1 = fontsmall.render(str(rr),True,(255,255,0))
		screen.blit(lbl1, (400-lbl1.get_width()//2 ,320-lbl1.get_height()/2))

		screen.blit(text, (320 - text.get_width() // 2, 400 - text.get_height() // 2))
		pygame.display.update()

