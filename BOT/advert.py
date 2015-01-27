#!/usr/bin/python

# KITSUNE advertisement module
# =======
# KITSUNE bot's EULA's terms include being allowed to self promote  up to once every 30 days
# via the end user's Twitter account. This module handles these promotional tweets.

from twython import Twython, TwythonError	# To interface with Twitter
import pickle				# To save and load API details
import os					  # To check for configuration files
import datetime			# To add timestamps to post history logs


# Bot will only post to twitter if this is set to True:
POST = True

# How many months (minumum) between advert posts?
rate = 3

# Configuration files:
filepath = '/home/pi/kitsune/BOT/'
postHistory = '%sDATA/postHistory.log' % filepath
keyFile = '%sDATA/API.dat' % filepath

advert = "Our Twitter account makes use of the KITSUNE social interaction bot. Email botKitsune@gmail.com for info."

# ---------------------------------------------------------------------------------------------
# INITIALIZATION

def setup():
# Check for a file of API keys to use when accessing Twitter.
	if os.path.exists(keyFile):
		# Read API detals from file
		load_file = open(keyFile,'rb')
		load_data = pickle.load(load_file)
		load_file.close()
	
		# Consumer keys relate to the app, access keys to the account
		CONSUMER_KEY = load_data['itemOne']
		CONSUMER_SECRET = load_data['itemTwo']
		ACCESS_KEY = load_data['itemThree']
		ACCESS_SECRET = load_data['itemFour']
	
		# Save above details for future use
		api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
	else:
		# No API details, take no action
		api = 0
	return api


# ------------------------------------------------------------------------------------------------
# POST & REPLY LOGGING

def record():
        if os.path.exists(postHistory):
			# Log that the advert was posted
			historyFile = open(postHistory, 'a', 0)
			historyFile.write('%s|KITSUNE|-----|Advert posted.\n' % timestamp())
			historyFile.close()
				
        else:
        	# No postHistory file, take no action.
		pass

def lastPost():
	global rate
	postTime = 0
	if os.path.exists(postHistory):
    		# Read all post history
    		historyFile = open(postHistory, 'r', 0)
    		history = historyFile.read()
        	historyFile.close()
        	history = history.split('\n')
		
        	for line in history:
        	    # Check each entry for the word KITSUNE
        	    logEntry = line.split('|')
        	    if 'KITSUNE' in logEntry:
        	        # KITSUNE entry found, save the timestamp
        	        postTime = logEntry[0]
    
	if postTime != 0:
    		# Get current month in number format
    		currentTime = timestamp()
    		currentTime = currentTime.split(" ")
    		currentDate = currentTime[0]
    		currentDate = currentDate.split(".")
    		currentMonth = int(currentDate[1])

    		# Extract month of post in number format
    		postTime = postTime.split(" ")
    		postDate = postTime[0]
    		postDate = postDate.split(".")
    		postMonth = int(postDate[1])

	    	if postMonth == 12:
	    		postMonth = 1 # To cope with end of year

	    	if rate != 0:
	    		rate = rate -1 # Convert rate of posting to fit formula below

	   	# Compare current time with time of last advert post
	    	if currentMonth > (postMonth + rate):
	    		return True # It's been long enough, post advert
	    	else:
	    		return False # Not been long enough, don't post advert

	else:
		return True # Advert never posted so OK to post



def timestamp():
        now = datetime.datetime.now()
        currentTime = now.strftime('%d.%m.%y %H:%M')
        return currentTime

# ------------------------------------------------------------------------------------------------
# INTERACTIONS WITH TWITTER

def postAd(api):
	if POST: api.update_status(status=advert)

# ------------------------------------------------------------------------------------------------
# MAIN LOOP

def main():
	api = setup()
	if api != 0: # check API keys
		if lastPost() == True: # Check if enough time has passed since last advert post
			record() # Log that advert has been posted
			postAd(api) # Post the advert tweet

if __name__ == '__main__':
	main()
