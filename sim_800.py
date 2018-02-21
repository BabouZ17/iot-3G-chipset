#!/usr/bin/env python
#-*- coding: utf-8 -*-
# function connexion uses Hayes commands to initialize the GPRS connection to the 3G network
# function is_connected uses an Hayes command to check the current connection state
# The global variables used are passed into the serial bus and need a specific syntax with two double quotes
# Python 2.7 by BabouZ17

import serial
import time

apn = '"free"' # free
apn_id = '""' # sometimes needed regarding the network provider used
apn_password = '""' # same thing with the apn password
sim_password = '""' # fill free to fill if needed
error_counter = 0 # an error counter (for me)


### Serial Port Set Up (GSM) #
try:
	ser = serial.Serial(

        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2,
        xonxoff = False,
        rtscts = True,       
	)

except SerialException:
	print 'Error regarding the serial port !'

finally:
	pass

def connexion(apn = apn, apn_id = apn_id, apn_password = apn_password, sim_password = sim_password):
	"""
	Connection GSM & GPRS using Hayes or AT commands on the serial port of the raspberry (for this instance)
		- apn string
		- apn_id string
		- apn_password string
		- sim_password string
	"""

	global error_counter

	sim_state = ''
	not_connected = True
	response = ''
	timer = 0


	# Checking if the serial port is open
	if (ser.isOpen() == False):
		ser.open()

	print ' --- %s ---' %(time.strftime("%x %X"),)
	print ' --- Connexion Started --- '
	

	while (ser.inWaiting() != 0):
		print ser.readline()
	
	ser.write('AT\r')
	time.sleep(0.5)
	
	while (ser.inWaiting() != 0):
		print ser.readline()

	ser.write('AT+CPIN?\r')
	time.sleep(5)
	
	while (ser.inWaiting() != 0):
		sim_state += ser.read()

	if (sim_state.find('READY',0,len(sim_state)) != -1):
		print sim_state
	
	else:
		ser.write('AT+CPIN=%s\r'%(sim_password,))
		time.sleep(1)
		
		while (ser.inWaiting() != 0):
			print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r') 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=3,1,"APN",%s\r'%(apn,)) 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=3,1,"USER",%s\r'%(apn_id,)) 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=3,1,"PWD",%s\r'%(apn_password,)) 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=1,1\r') 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	# Setting Up APN parameters
	ser.write('AT+SAPBR=2,1\r') 
	time.sleep(2)
	
	while (ser.inWaiting() != 0):
		print ser.readline()
	
	ser.write('AT+CGREG?\r')
	time.sleep(1)
	
	while (ser.inWaiting() != 0):
		response += ser.read()
	
	while response.find('5',0,len(response)) == -1:
		ser.write('AT+CGREG?\r')
		time.sleep(1)
		timer += 1
		
		while (ser.inWaiting() != 0):
			response += ser.read()
		
		print ' --- Looking For Network --- '
		
		if response.find('3',0,len(response)) != -1 or timer >= 60:
			print ' --- %s --- ' %(time.strftime("%x %X"),)
			print ' --- Going To Reset --- '
			reset()
			break

		elif response.find('5',0,len(response)) != -1:
			not_connected = False
			print ' --- Network Connected --- '
			break

	if response.find('5',0,len(response)) != -1:
		not_connected = False

	return not_connected

def is_connected():
	"""
	Check if the gprs connection is still operating
	"""
	
	global error_counter

	still_connected = False
	response = ''

	if (ser.isOpen() == False):
		ser.open()

	print ' --- %s --- ' %(time.strftime("%x %X"),)
	print ' --- Checking GPRS Connexion --- '

	ser.write('AT+CGREG?\r')
	time.sleep(1)
	
	while (ser.inWaiting() != 0):
		response += ser.read()

	# 5 means your gprs connection is still working	
	if response.find('5',0,len(response)) != -1:

			still_connected = True
			print ' --- %s --- ' %(time.strftime("%x %X"),)
			print ' --- Still Connected! --- '

	return still_connected