#!usr/bin/python

# User interface and updater for KITSUNE
# --------------------------------------

import time
import os
import sendHistory

filepath = '/home/pi/kitsune/BOT/'

wordFile = '%skey_words.txt' % filepath
messageFile = '%sresponse_text.txt' % filepath
postHistory = '%sDATA/postHistory.log' % filepath

defaultSearch = ['TEST_SEARCH_TERM']
defaultMessage = ['TEST_RESPONSE_MESSAGE']

# ---------------------------------------------------------------
# MENU

def menu():
	while True:
		os.system('clear')
		print """ 
----------------------------------------
                KITSUNE
             User Interface
----------------------------------------
========================================
     MAIN MENU
 1 > Start Twitter Bot
 2 > Search Terms and Responses
 3 > View Interaction History
 4 > Check for Updates
 5 > Shutdown"""

		selection = raw_input('\n   > ')

		if selection == '1':
# Run KITSUNE Twitter bot
			print 'The Twitter bot will now start. Press Ctrl + C to stop and return to the main menu.'
			time.sleep(2)
			os.system('sudo python %skitsune.py' % filepath)
			print '\n Twitter bot stopped. Returning to main menu.'
		elif selection == '2':
# Set Keywords/Responses
			while True:
				os.system('clear')
				print """ 
----------------------------------------
                KITSUNE
             User Interface
----------------------------------------
========================================
     SEARCH SETTINGS
 1 > Review search term/response pairs
 2 > Add new pair
 3 > Return to main menu"""
				selection = raw_input('\n   > ')
				if selection == '1':
					changeTerms()
				if selection == '2':
					addTerm()
				if selection == '3':
					break
				else:
					print 'Invalid selection, please try again'

		elif selection == '3':
# View postHistory.log
			history = viewHistory()
			while True:
				os.system('clear')
				print """ 
----------------------------------------
                KITSUNE
             User Interface
----------------------------------------
========================================
     INTERACTION HISTORY
  Would you like an email copy?
 1 > Yes
 2 > No"""
				selection = raw_input('\n   > ')
				if selection == '1':
				# Email file
#					try:
					print "Please specify the recipient's email:"
					to = raw_input(' > ')
					sendHistory.sendAll(to, history)
					print 'History has been sent successfully'
					break
#					except:
#						print 'Error: Email failed to send.'
				elif selection == '2':
				# Return to menu
					break
				else:
					print 'Invalid selection, please try again'
					time.sleep(1)
			
		elif selection == '4':
# Update process
			print 'Please wait'
			os.system('sudo git pull origin master')
			print 'Restart the system for the updates to take effect.'
	
		elif selection == '5':
# Shutdown menu
			while True:
				os.system('clear')
	
				print """
----------------------------------------
                KITSUNE
             User Interface
----------------------------------------
========================================
     SHUTDOWN MENU
 0 > Go Back
 1 > Shutdown
 2 > Restart"""
				selection = raw_input('\n   > ')
				if selection == '0':
					break
				elif selection == '1':
					os.system('sudo halt')
				elif selection == '2':
					os.system('sudo reboot')
				else:
					print 'Invalid selection: Please try again.'
		else:
# Invalid selection error capture
			print 'Invalid selection: Please try again.'

		time.sleep(2)

# ---------------------------------------------------------------------------
# FILE MANIPULATION

def viewHistory():
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



# --------------------------------------------------------------------------
if __name__ == '__main__':
	while True:
		try:
			menu()
		except KeyboardInterrupt:
			print '\nRebooting menu, please wait...'
			print '(Press Ctrl+C again to abort)'
			time.sleep(2)