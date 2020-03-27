'''
  ___          _____     __  __
   _/    _  _ (_  | |\/|  _)  _)
  /__|_||||(_)__) | |  | __) /__
 
 Fachhochschule Südwestfalen
 Mechatronik/Mikrocomputer
 Prof. Dr.-Ing. Tobias Ellermeyer

 Klasse, um statt echter Bluetooth-Daten eine Datei zu verwenden...

'''

import random	# random number generators
from time import sleep

UPDATE_MILLIS = 500.0		# Update Rate in Milliseconds

class Serial():
	def __init__(self, filename, baudrate):
		
		# memories for generating random data
		self.range_ff=150
		self.range_fr=150
		self.range_fl=150
		self.range_rr=150
		self.range_ll=150
		self.enc_r = 0
		self.enc_l = 0
		self.delayenabled = True

		self.filename = filename

		# if filename==__RANDOM__, this class will generate 
		# random data instead of reading a file ...
		if (filename=='__RANDOM__'):
			self.random = True
			print("DEBUG: Generating RANDOM data for Bluetooth simulation")
		else:
			self.random = False
			try:
				self.fileobj = open(self.filename,"r")	# open file as read only 
			except:
				print("***ERROR*** File ", self.filename , "not found")
				exit()
			self.fileopened = True
			print("DEBUG: Opened ", self.filename, " for Bluetooth simulation")
	def disableDelay(self):
		self.delayenabled = False

	def readline(self):
		if (self.delayenabled):
			sleep(UPDATE_MILLIS/1000.0)		# Speed of new data
		if self.random:
			line = self.__generate_random()
		else:
			line = self.fileobj.readline()
			line = line.encode()
		return(line)

	# Private methods

	def __constrain_range(self, val):
		if (val>220): val = 220
		if (val<0): val = 0
		return val

	def __constrain_encoder(self, val):
		if (val>65535): val = val-65535
		if (val<0): val = 65536-val
		return val

	def __generate_random(self):
		#from c-code of ZumoSTM32 routine
		#sprintf(buf,"FF %3i; FL %3i; FR %3i; LL %3i; RR %3i; EL %9i; ER %9i\r\n",
		#		range[0], range[1], range[2], range[3], range[4], encoder_left, encoder_right);
		self.range_ff = self.__constrain_range(self.range_ff+random.randint(-10,10))
		self.range_fl = self.__constrain_range(self.range_fl+random.randint(-10,10))
		self.range_fr = self.__constrain_range(self.range_fr+random.randint(-10,10))
		self.range_ll = self.__constrain_range(self.range_ll+random.randint(-10,10))
		self.range_rr = self.__constrain_range(self.range_rr+random.randint(-10,10))
		self.enc_r    = self.__constrain_encoder(self.enc_r+random.randint(-50,50))
		self.enc_l    = self.__constrain_encoder(self.enc_l+random.randint(-50,50))
		line="FF {:3d}; FL {:3d}; FR {:3d}; LL {:3d}; LL {:3d}; EL {:9d}; ER {:9d};".format(
			self.range_ff, self.range_fl, self.range_fr, self.range_ll, self.range_rr,
			self.enc_l, self.enc_r)
		line = line +"\r\n"
		return line.encode()