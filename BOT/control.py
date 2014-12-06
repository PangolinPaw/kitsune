#!usr/bin/python

# User interface and updater for KITSUNE
# --------------------------------------

import time
import os

wordFile = 'key_words.txt'
messageFile = 'response_text.txt'
postHistory = 'DATA/postHistory.log'

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

		selection = raw_input('\n          > ')
		print '----------------------------------------'

		if selection == '1':
# Run KITSUNE Twitter bot
			print 'The Twitter bot will now start. Press Ctrl + C to stop and return to the main menu.'
			time.sleep(2)
			os.system('sudo python kitsune.py')
			print '\n Twitter bot stopped. Returning to main menu.'
		elif selection == '2':
# Set Keywords/Responses
			print """ 
       SEARCH SETTINGS"""
			changeTerms()

		elif selection == '3':
# View postHistory.log
			print '3'

		elif selection == '4':
# Update process
			print '4'
	
		elif selection == '5':
# Shutdown menu
			print """
        SHUTDOWN MENU
        0 > Go Back
        1 > Shutdown
        2 > Restart"""
			selection = raw_input('           > ')
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
# FILE EDITING

def changeTerms():
	postDictionary = matchPosts()
	items = len(postDictionary)
	print 'There is/are currently %s search term/reponse pairs:' % items
	count = 0
	for search, response in postDictionary.items():
		count = count +1
		while True:
			print """ 
SEARCH %s: %s
RESPONSE : %s""" % (count, search, response)
			print """ 
Would you like to change this pair?
 0 > Leave them as they are
 1 > Change search term
 2 > Change response
 3 > Delete the pair"""
			selection = raw_input('\n > ')
			if selection == '0':
				print 'Pair unchanged'
				break
			elif selection == '1':
				print 'Change search term'
				break
			elif selection == '2':
				print 'Change response'
				break
			elif selection == '3':
				print 'Delete pair'
				del postDictionary[search]
				break
			else:
				print 'Invalid selection, please try again.'

	proceed = raw_input('Press Enter to continue')

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
