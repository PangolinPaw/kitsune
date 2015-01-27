#!usr/bin/python

# UPDATE VALIDATION
# Forces user to request permission from botKITSUNE@gmail.com before an update is applied.
# This is only effective if the software is supplied on a pre-imaged SD card that doesn't allow read access to any files. This allows for different versions
# of KITSUNE (with different features) to be made available.

import pickle
import os
import random
import datetime
import gmail

filepath = '/home/pi/kitsune/BOT/'
IDFile = '%sDATA/ID.dat' % filepath
IPfile = '%sDATA/IP.dat' % filepath

def createID():
	if os.path.exists(IDFile):
# Update file exists, calculate Update Key & email to botKITSUNE
		IPaddr = getIP()
		IDnum = readID()
		
		day = datetime.now().timetuple().tm_yday # Day of the year (keys only valid for one day)
		updateKey = ((IDnum/22) +9)*day

		subject = '**Update Request (%s)**' % IPaddr
		message = """ 
An existing copy of KITSUNE is requesting an update.
Details:
User IP:    %s
ID number:  %s

UPDATE KEY: %04x""" % (IPaddr, IDnum, updateKey)
		try:
			gmail.message('botKitsune@gmail.com', '***', 'botKitsune@gmail.com', subject, message)
		except:
			pass
		return True

# No update file exists, create it & log creation with botKITSUNE
	else:
		IDdata = ['***Editing or removing this file will cause KITSUNE to become nonfunctional.***', 'IP:', getIP(), 'Product serial number:', generateNum()] # Serial number is always last item in list
		fileObject = open(IDFile, 'wb')
		pickle.dump(IDdata, fileObject)
		fileObject.close()

		# Registration email sent automatically
		subject = '**New Installation (%s)**' %IDdata[-3]
		message =""" 
A new copy of KISTUNE has been installed and an update attempted. 
Details:
User IP:   %s
ID number: %s""" % (IDdata[-3], IDdata[-1])
		try:
			gmail.message('botKitsune@gmail.com', '***', 'botKitsune@gmail.com', subject, message)
		except:
			pass
		return False

def getIP():
	# Fetch external IP address & save to temporary file
	os.system('curl -s echoip.com > %s' IPfile)
	fileObject = open(IPfile, 'r')
	IPaddr = fileObject.read()
	fileObject.close()

	# Delete temporary IP file
	os.system('sudo rm %s' % IPfile)
	return IPaddr

def generateNum():
	number = random.randint(1000,9999)
	return number

def readID():
	# Check identity of install
	fileObject.open(IDFile, 'r')
	IDdata = pickle.load(fileObject)
	ID = IDdata[-1] # Serial number is always last item in the list
	return float(ID)

def validate(key):
	# Carry out calculation using the Update Key & serial number to check if installation is valid
	day = datetime.now().timetuple().tm_yday # Day of the year (keys only valid for one day)
	ID = readID()
	result = ((ID/22) +9)*day
	if key == int(result):
		return True
	else:
		return False


def main():
	# Bring the process above together in the corect order, take input from user & check validity
	createID() # Check ID has been created (& do so if it hasn't)
	ID = readID() # Fetch product ID
	print """ 
Your software needs to be authenticated before installing the latest features. 
If you do not have an Update Key, please press Ctrl+C to go back to the main menu and email botKITSUNE@gmail.com
Product ID: %s""" % ID
	key = raw_input('Update key: ')
	key = int(key, 16) # Convert key (hexadecimal number) to integer

	if validate(key) == True:
		# Valid key, continue with update
		return True
	else:
		# Invalid key, prevent update
		print "That Update Key is either invalid or has expired. Please ensure it was entered correctly or email botKITSUNE@gmail.com for assistance."
		return False

if __name__ == '__main__':
	if main() == True:
		print 'VALID'
	else:
		print 'INVALID'


