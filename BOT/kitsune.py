#!/usr/bin/python

# KITSUNE v2.0
# =======
# Improved twitter interactions based on Twython

from twython import Twython, TwythonError	# To interface with Twitter
import time					# To regulate post and search rates
import pickle					# To save and load API details
import os					# To check for configuration files
import string					# To filter out non-readable characters

# If set to True, the program prints notificatons at each stage of the search/record/reply process:
DEBUG = True
DEBUG2 = False
# Bot will only post to twitter if this is set to True:
POST = True

SHUTDOWN = True	# If true, Pi will shut down after...
LIMIT = 95	# ...This many search/response loops

searchCount = 5	# How many tweets to return per search term
interval = 5 # Delay (minutes) between each search/reply loop

# Configuration files:
keyFile = 'DATA/API.dat'
wordFile = 'key_words.txt'
messageFile = 'response_text.txt'
postHistory = 'DATA/postHistory.log'

# If conficuration files have not been set up, the program uses the following search terms & replies:
defaultSearch = ['testphrase01']
defaultMessage = ['test response 01']

# ---------------------------------------------------------------------------------------------
# INITIALIZATION

def setup():
# Check for a file of API keys to use when accessing Twitter. If none exist, take them as an input.
	if os.path.exists(keyFile):
		if DEBUG: print 'D: API details found'
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
		print 'No API details found. Please enter them now.'
		while True:
			# Take input of new keys
		        CONSUMER_KEY = raw_input('CONSUMER KEY:    ')
		        CONSUMER_SECRET = raw_input('CONSUMER SECRET: ')
		        ACCESS_KEY = raw_input('ACCESS KEY:      ')
		        ACCESS_SECRET = raw_input('ACCESS SECRET:   ')
			
			print "Thank you. \nThe keys cannot be changed once set, please check that they are correct.\n Enter 'Y' to continue, 'N' to re-enter the keys."
			checked = raw_input(' > ')
			if checked.upper() == 'Y':
				# Save new API keys to file
			        save_data = {'itemOne':str(CONSUMER_KEY),'itemTwo':str(CONSUMER_SECRET),'itemThree':str(ACCESS_KEY),'itemFour':str(ACCESS_SECRET)}
			        save_file = open(keyFile,'wb')
			        pickle.dump(save_data,save_file)
			        save_file.close()

				# Save new keys for future use
			        api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
				break
	return api

# -------------------------------------------------------------------------------------------------
# SET SEARCH TERMS & RESPONSES

def search_terms():
# Read the key words and phrases from the keyword file
        if os.path.exists(wordFile):
                # Read keywords
                if DEBUG: print 'D: Loading keywords'
                readFile = open(wordFile, 'r', 0)
                keywords = readFile.read()
                readFile.close()

                keywords = keywords.split('\n')
                # Reading from a file adds an empty line, which we don't want in the list
                keywords.pop()
                return keywords
        else:
                # Create file with default keywords
                if DEBUG: print 'D: Using default keywords'
                newFile = open(wordFile, 'w', 0)
                for phrase in defaultSearch:
                        newFile.write('%s\n' % phrase)
                newFile.close()
                return defaultSearch

def responses():
# Reads preset tweets from message.txt
        if os.path.exists(messageFile):
                # Read messages
                if DEBUG: print 'D: Loading messages'
                readFile = open(messageFile, 'r', 0)
                messages = readFile.read()
                readFile.close()

                messageList = messages.split('\n')
                return messageList
        else:
                # No preset messages, create file with defaults
                if DEBUG: print 'D: Using default messages'
                newFile = open(messageFile, 'w', 0)
                for message in defaultMessage:
                        newFile.write('%s\n' % message)
                newFile.close()
                return defaultMessage

def matchPosts():
# Matches keywords with messages so the correct reposne can be posted to each tweet found
        if DEBUG: print 'D: Creating dictionary of responses'
        keywords = search_terms()
        messages = responses()
        postDictionary = {}
        for x in range(len(keywords)):
                postDictionary[keywords[x]] = messages[x]
                if DEBUG:print postDictionary[keywords[x]]
        return postDictionary

# ------------------------------------------------------------------------------------------------
# POST & REPLY LOGGING

def record(customer, theirPost, myPost):
# Makes a note of each tweet caught & what was sent in return.
# Returns True if this is the first time we've met the Twitter user.
	customer = '@%s' % customer
        if os.path.exists(postHistory):
                # Read all post history
                if DEBUG: print 'D: Loading post history'
                historyFile = open(postHistory, 'r', 0)
                history = historyFile.read()
                historyFile.close()
                history = history.split('\n')
		
                for line in history:
                        logEntry = line.split('|')
                        if customer in logEntry:
				if DEBUG2: print '%s - %s' % (logEntry[0], customer)
                                if DEBUG: print 'D: %s found in post history' % customer
                                # We've tweeted at this customer before, ignore their tweet
                                canReply = False
				break
                        else:
                                # Never contacted this customer before, so save their details
                                historyFile = open(postHistory, 'a', 0)
                                historyFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
                                historyFile.close()
                                if DEBUG: print "D: Added record of %s's tweet to post history" % customer
                                canReply = True
				
        else:
                # No history file so create a new one with this first tweet included
                if DEBUG:
                        print 'D: Creating post history log'
                newFile = open(postHistory, 'w', 0)
                newFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
                newFile.close()
                if DEBUG: print "D: Added record of %s's tweet to post history" % customer
                # No history log so we know we've never tweeted to this customer before
                canReply = True

	if DEBUG2: print canReply
	return canReply


# ------------------------------------------------------------------------------------------------
# INTERACTIONS WITH TWITTER

def search(api, postDictionary):
# Search twitter for keywords


	for keyword, message in postDictionary.items():
		print '----------------------------------'
		print 'Searching for %s...' % keyword
		try:
			hits = api.search(q=keyword, count=searchCount)
			for tweet in hits['statuses']:
				text = tweet['text']
				text = clean(text)
				user = tweet['user']['screen_name']
				reply = '@%s %s' % (user, message)
				
				if record(user, text, reply) == True:
					print 'TWEET FOUND:\n%s\n%s' % (user, text)
					try:
						if POST: api.update_status(status=reply, in_reply_to_status_id=tweet['id_str'])
						print 'REPLY SENT:\n%s' % reply

					except TwythonError as e:
						print 'Send error:\n%s' % e
					print '\n'
				else:
					print 'Ignored a tweet from %s' % user

		except TwythonError as e:
			print 'Search error:\n%s' % e

# --------------------------------------------------------------------------------------------
# SANITIZE TWEETS OF NON-READABLE CHARACTERS

def clean(text):
        # Remove emoji & non-roman characters
        text = filter(lambda x: x in string.printable, text)
        # Remove any empty lines that confuse the history check
        text = text.replace('\n', '  ')
	return text

# ---------------------------------------------------------------------------------------------
# MAIN LOOP

def main():
	loopCount = 0
	api = setup()	# Get access via API
	while True:
		postDictionary = matchPosts()	# Associate keywords with responses
		search(api, postDictionary)	# Search twitter for keywords & post responses
		if DEBUG: print 'D: Sleeping for %s min' % interval

		loopCount = loopCount +1
		if loopCount > LIMIT:
			if SHUTDOWN:
				api.update_status(status='Auto Shutdown')
				os.system('sudo halt')

		time.sleep(interval * 60)


if __name__ == '__main__':
	main()
