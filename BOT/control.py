#!usr/bin/python

# User interface and updater for KITSUNE
# --------------------------------------

import time
import os
import sendHistory
import kitsune
import advert
import validate

# Version tracking & clangelog for update screen
version = 1.6
latest = """ 
Version %s (latest update):
  - Added Follow function, bot will now follow all individuals it replies to.
  - Added Follow and Post controls so replies and auto-following can be switched on or off.
  - Re-ordered main menu to incorporate new controls.

Version %s:
  - Feature control functions added to Update menu.
  - Version validation checks enabled.
  - Auto-update core functionality on each run.

Version %s
  - Added option to overwrite API details.
  - Improved version tracking.
  - Self promotion adverts enabled (see EULA: Fees and Marketing).""" % (version, (version - 0.1), (version - 0.2))

filepath = '/home/pi/kitsune/BOT/'

wordFile = '%skey_words.txt' % filepath
messageFile = '%sresponse_text.txt' % filepath
postHistory = '%sDATA/postHistory.log' % filepath
archive = '%sDATA/postArchive.log' % filepath
APIfile = '%sDATA/API.dat' % filepath

defaultSearch = ['TEST_SEARCH_TERM']
defaultMessage = ['TEST_RESPONSE_MESSAGE']

AUTORUN = True
SENDHISTORY = False
AUTO_UPDATE = False

# ---------------------------------------------------------------
# MENU

def menu():
	while True:
		os.system('clear')
		print """ 
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     MAIN MENU
 0 > Start Twitter Bot

 1 > Follow & Post controls
 2 > Search Terms and Responses
 3 > View Interaction History

 4 > Check for Updates
 5 > Change API details

 6 > Shutdown""" % version

		selection = raw_input('\n   > ')

		if selection == '0':
# Run KITSUNE Twitter bot
			print 'The Twitter bot will now start. Press Enter/Return to stop it and return to the main menu.'
			time.sleep(2)
			try:
				kitsune.main()
			except KeyboardInterrupt:
				print '\n Twitter bot stopped. Returning to main menu.'
				time.sleep(2)

		elif selection == '1':
# Change POST & FOLLOW settings
			while True:
				currentSettings = kitsune.postSetting(['READ', '0', '0'])
				followOK = currenSettings[1]
				postOK = currentSettings[2]
				print """ 
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     INTERACTION SETTINGS

 Current Settings:
   - Follow users = %s
   - Post replies = %s

 1 > Toggle Following
 2 > Toggle Posting
 3 > Return to main menu""" % (version, followOK, postOK)
				selection = raw_input('\n   > ')
				if selection == '1':
					# Swap the value of followOK to it's opposite
					if followOK == True:
						followOK = False
					else:
						followOK = True

					# Save changes
					kitsune.postSettings(['WRITE', followOK, postOK])
					time.sleep(0.5)

				if selection == '2':
					# Swap the value of postOK to it's opposite
					if postOK == True:
						postOK = False
					else
						postOK = True

					# Save changes
					kitsune.postSettings(['WRITE', followOK, postOK])
					time.sleep(0.5)
				if selection == '3':
					break
				else:
					print 'Invalid selection, please try again'			

		elif selection == '2':
# Set Keywords/Responses
			while True:
				os.system('clear')
				print """ 
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     SEARCH SETTINGS
 1 > Review search term/response pairs
 2 > Add new pair
 3 > Return to main menu""" % version
				selection = raw_input('\n   > ')
				if selection == '1':
					changeTerms()
				if selection == '2':
					addTerm()
					print 'New pair added.'
					time.sleep(1)
				if selection == '3':
					break
				else:
					print 'Invalid selection, please try again'

		elif selection == '3':
# View postHistory.log
			history = viewHistory()
			if history != False:
				while True:
					os.system('clear')
					print """ 
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     INTERACTION HISTORY
  Would you like an email copy?
 1 > Yes
 2 > No""" % version
					selection = raw_input('\n   > ')
					if selection == '1':
				# Email file
						try:
							print "Please specify the recipient's email:"
							to = raw_input(' > ')
							sendHistory.sendAll(to, history)
							print 'History has been sent successfully'
							time.sleep(2)
							break
						except:
							print 'Error: Email failed to send.'
					elif selection == '2':
					# Return to menu
						break
					elif selection == '987':
						os.system('sudo mv %s %s' % (postHistory, archive))
						print 'postHistory has been archived in %s' % archive
					else:
						print 'Invalid selection, please try again'
						time.sleep(1)
			else:
			# No history file
				print 'No postHistory file found.'
			
		elif selection == '4':
# Update process
			os.system('clear')
			print """
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     UPDATES AND UPGRADES
%s""" % (version, latest)
   			output = validate.validate()
   			if output[0] == True: # Update Key OK
				os.system('sudo git pull origin %s' % output[1]) # Download branch specified by Update Key

				print """ 
   > The software is now up to date and the system will restart so changes can take effect."""
				time.sleep(2)
				# Restart necessary for changes to take effect
#				os.system('sudo reboot')
			else: # Invalid Update Key
				print """ 
   > The software update was not successful, please try again."""				

		elif selection == '5':
# Change API details
			while True:
				os.system('clear')

				print """ 
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     API DETAILS
 0 > Go Back
 1 > Clear data""" % version
				selection = raw_input('\n  > ')
				if selection == '0':
					print 'Returning to main menu'
					break
				elif selection == '1':
					print "\nThis will permanently clear current API details so Kitsune will not be able to interact with Twitter."
					print "To add new details, run the bot from the main menu and enter all four keys when prompted."
					while True:
						print '\nAre you sure you want to clear the current API details?'
						print """ 
 2 > Yes
 3 > No"""
						selection = raw_input('\n  > ')	
						if selection == '2':
						        if os.path.exists(APIfile):
								os.system('sudo rm %s' % APIfile)
								print 'API keys deleted. Run the bot from the main menu to input new keys.'
							else:
								print 'No API details are saved. Run the bot from the main menu to input new keys.'
							selection = raw_input('Press Enter to continue')
							break
						elif selection == '3':
							print 'API details unchanged.'
							selection = raw_input('Press Enter to continue')
							break
						else:
							print 'Invalid selection, please try again.'
						time.sleep(1)

				else:
					print 'Invalid selection: please try again.'
				time.sleep(2)


		elif selection == '6':
# Shutdown menu
			while True:
				os.system('clear')
	
				print """
----------------------------------------
                KITSUNE		    v%s
             User Interface
----------------------------------------
========================================
     SHUTDOWN MENU
 0 > Go Back
 1 > Shutdown
 2 > Restart""" % version
				selection = raw_input('\n   > ')
				if selection == '0':
					break
				elif selection == '1':
					os.system('sudo halt')
				elif selection == '2':
					os.system('sudo reboot')
				elif selection == '987':
					os.system('sudo killall python')
				else:
					print 'Invalid selection: Please try again.'
		else:
# Invalid selection error capture
			print 'Invalid selection: Please try again.'

		time.sleep(2)

# ---------------------------------------------------------------------------
# FILE MANIPULATION

def viewHistory():
        if os.path.exists(postHistory):

		timeStamp = 0
		newFile = open(postHistory, 'r', 0)
		history = newFile.read()
		newFile.close()
	
		history = history.split('\n')
		history.pop()
	
		print '%s post(s) recorded' %  len(history)
		for line in history:
			print
			line = line.split('|')
			pastTimeStamp = timeStamp
			timeStamp = line[0]
			if timeStamp != pastTimeStamp:
				print '-----%s-----' % timeStamp
			print 'USER: \n%s' % line[1]
			print 'TWEET: \n%s' % line[2]
			print 'RESPONSE: \n%s' % line[3]
		input = raw_input('\nPress Enter to continue')
	
		return history
	else:
		return False

def changeTerms():
	postDictionary = matchPosts()
	items = len(postDictionary)
	os.system('clear')
	print """ 
----------------------------------------
                KITSUNE
             User Interface
----------------------------------------
========================================
     REVIEW SEARCH TERMS & RESPONSES"""

	if items < 1:
		postDictionary['TEST_SEARCH_TERM_01'] = 'TEST RESPONSE MESSAGE 01'
		print 'There were no search term/response pairs, but the list cannot be left blank. A placeholder has been added:'
	else:
		print 'There is currently %s search term/reponse pair(s):' % items
	count = 0
	for search, response in postDictionary.items():
		count = count +1
		while True:
			print """ 
SEARCH %s:
 %s
RESPONSE:
 %s

Would you like to change this pair?
 0 > Leave them as they are
 1 > Change search term
 2 > Change response
 3 > Delete pair (list cannot be blank)""" % (count, search, response)

			selection = raw_input('\n   > ')
			if selection == '0':
# Move to next pair
				print 'Pair unchanged'
				break
			elif selection == '1':
# Change search term
				print 'Change search term to:'
				newSearch = raw_input(' > ')
				# Create new key with newSearch & add original response to it
				postDictionary[newSearch] = response
				# Remove the old search
				del postDictionary[search]
				print 'Search term changed'
				break
			elif selection == '2':
# Change response
				print 'Change response to:'
				newResponse = raw_input(' > ')
				postDictionary[search] = newResponse
				print 'Response changed'
				break
			elif selection == '3':
				print 'Delete pair'
				del postDictionary[search]
				break
			else:
				print 'Invalid selection, please try again.'
				time.sleep(1)

	convertToList(postDictionary)
	proceed = raw_input('Press Enter to continue')

def addTerm():
	postDictionary = matchPosts()
	print 'Enter new search term (use - to indicate words to exclude):'
	search = raw_input(' > ')
	print "Enter new response message (the user's Twitter name is added automatically as the 1st word):"
	response = raw_input(' > ')
	postDictionary[search] = response
	convertToList(postDictionary)

# --------------------------------------------------------------------------------------
# WRITE FILES

def convertToList(dictionary):
# Converts the dictionary into two lists, one for keys and one for responses
	keys = []
	items = []
	for search, response in dictionary.items():
		keys.append(search)
		items.append(response)

	newFile = open(wordFile, 'w', 0)
	for item in keys:
		newFile.write('%s\n' % item)
	newFile.close()

	newFile = open(messageFile, 'w', 0)
	for item in items:
		newFile.write('%s\n' % item)
	newFile.close()

# ---------------------------------------------------------------------------------------
# RETRIEVE SEARCH TERMS & RESPONSES
def search_terms():
# Read the key words and phrases from the keyword file
        if os.path.exists(wordFile):
                # Read keywords
                readFile = open(wordFile, 'r', 0)
                keywords = readFile.read()
                readFile.close()

                keywords = keywords.split('\n')
                # Reading from a file adds an empty line, which we don't want in the list
                keywords.pop()
                return keywords
        else:
                # Create file with default keywords
                newFile = open(wordFile, 'w', 0)
                for phrase in defaultSearch:
                        newFile.write('%s\n' % phrase)
                newFile.close()
                return defaultSearch
def responses():
# Reads preset tweets from message.txt
        if os.path.exists(messageFile):
                # Read messages
                readFile = open(messageFile, 'r', 0)
                messages = readFile.read()
                readFile.close()

                messageList = messages.split('\n')
                return messageList
        else:
                # No preset messages, create file with defaults
                newFile = open(messageFile, 'w', 0)
                for message in defaultMessage:
                        newFile.write('%s\n' % message)
                newFile.close()
                return defaultMessage

def matchPosts():
# Matches keywords with messages so the correct reposne can be posted to each tweet found
        keywords = search_terms()
        messages = responses()
        postDictionary = {}
        for x in range(len(keywords)):
                postDictionary[keywords[x]] = messages[x]
        return postDictionary


def dailyHistory(to,content):
        newFile = open(postHistory, 'r', 0)
        history = newFile.read()
        newFile.close()

        history = history.split('\n')
        history.pop()

	print 'Daily history updates have not yet been implememnted.'

# --------------------------------------------------------------------------
if __name__ == '__main__':
	# Send self-promoting Tweet according to predefined schedule
	advert.main()
	# Update core functionality ready for next boot
	if AUTO_UPDATE: os.system('sudo git pull origin master')
	# Start the main menu
	hasRun = False
	while True:
		try:
		# Autorun the bot once program starts
			if AUTORUN == True and hasRun == False:
				hasRun = True
			        if os.path.exists(postHistory):
					kitsune.main()


		# Then go to main menu if Ctrl+C pressed
			menu()
		except KeyboardInterrupt:
			print '\nRebooting menu, please wait...'
			print '(Press Ctrl+C again to abort)'
			time.sleep(2)
