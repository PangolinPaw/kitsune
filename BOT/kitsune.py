##!/usr/bin/python
# TWITTER AD BOT - TEST VERSION
# ==============
# Designed as a free alternative to twitter's advert feature, this program
# scans twitter for key words and replies to all tweets with preset messages.
# --------------
import twitter
import time
import os
import string # Used to filter non-ASCII characters from tweets

DEBUG = False	# Console outputs will appear if set to True
interval = 1	# Time between twitter scans (minutes)

account = 'DATA/puzzleIsland'	# API details stored in file with this name
keyfile = 'key_words.txt'	# Search terms stored in file with this name
postHistory = 'DATA/postHistory.log'	# This program's posts recorded in file with this name
messageFile = 'messages.txt'	# Your responses are retrieved from here

# Default search terms & messages if none are set in keyFile or messageFile above
defaultSearch = ['keyphrase01', 'keyphrase02']
message00 = "We noticed you tweeted about %s and thought you might be interested in [url]" % defaultSearch[0]
message01 = "Hello. We just saw your tweet about %s, why not take a look at [url]?" % defaultSearch[1]
defaultMessage = [message00, message01]

# -----------------------------------------------------------------------------------------
# THE LINK WITH THE API IS SET UP AND MAINTAINED BY THIS BIT
def newFile():
# Checks id there's an API file present & creates one if not
	# API details
	Ckey = ' '
	Csec = ' '
	Atok = ' '
	Asec = ' '
	if os.path.exists(account + '.dat'):
		if DEBUG:
			print 'DEBUG: API details found'
		return True
	else:
		if DEBUG:
			print 'DEBUG: API details added'
		twitter.new_account(account, Ckey, Csec, Atok, Asec)
	return False

# -------------------------------------------------------------------------------------
# THESE BITS ARE ALL ABOUT SETTING THE KEYWORDS & THE MESSAGES WE WANT TO SEND IN RESPONSE
def readKeywords():
# Read the key words and phrases from the keyword file
	if os.path.exists(keyfile):
		# Read keywords
		if DEBUG:
				print 'DEBUG: Loading keywords'
		readFile = open(keyfile, 'r', 0)
		keywords = readFile.read()
		readFile.close()

		keywords = keywords.split('\n')
		# Reading from a file adds an empty line, which we don't want in the list
		keywords.pop()
		return keywords
	else:
		# Create file with default keywords
		if DEBUG:
			print 'DEBUG: Using default keywords'
		newFile = open(keyfile, 'w', 0)
		for phrase in defaultSearch:
			newFile.write('%s\n' % phrase)
		newFile.close()
		return defaultSearch

def readMessage():
# Reads preset tweets from message.txt
	if os.path.exists(messageFile):
		# Read messages
		if DEBUG:
			print 'DEBUG: Loading messages'
		readFile = open(messageFile, 'r', 0)
		messages = readFile.read()
		readFile.close()

		messageList = messages.split('\n')
		return messageList
	else:
		# No preset messages, create file with defaults
		if DEBUG:
			print 'DEBUG: Using default messages'
		newFile = open(messageFile, 'w', 0)
		for message in defaultMessage:
			newFile.write('%s\n' % message)
		newFile.close()
		return defaultMessage

def matchPosts():
# Matches keywords with messages so the correct reposne can be posted to each tweet found
	if DEBUG:
		print 'DEBUG: Creating dictionary of responses'
	keywords = readKeywords()
	messages = readMessage()
	postDictionary = {}
	for x in range(len(keywords)):
		postDictionary[keywords[x]] = messages[x]
		if DEBUG:
			print postDictionary[keywords[x]]
	return postDictionary

# ---------------------------------------------------------------------------------------
# THESE BITS ACTUALLY INTERRACT WITH TWITTER
def scan():
	postDictionary = matchPosts()
	hits = []
	for keyword, message in postDictionary.items():
		# Search for tweets containing the keyword
		print """ 
===========================================
SEARCH TERM:
%s""" % keyword

		try:
			hits.append(twitter.read_tweet(account, keyword)) 
		except:
			# Prevent crash if twitter API blocks search
			print '15 searches per 15 minutes exceeded'
			time.sleep(5*60)
		for hit in hits:
			# Pass our response message to respond()
			respond(hit, message) 
		# Each iteration of the dictionary appended the next keword's hits to
		# the list. So wipe the hit list after each loop:
		hits = []
	return hits

def respond(tweet, message):
# Posts *message* to the owner of *tweet*
	if tweet != []:
		data = extract(tweet)
		name = data[0]
		text = data[1]


		myPost = "@%s %s" % (name, message)
		if DEBUG:
			print 'DEBUG: Composing response'
	
		try:
			if record(name, text, myPost) == True:
				# Post response to twitter
#				post(myPost)
				print """ 
TWEET FOUND:
-------------------------------------------
%s
%s
-------------------------------------------
RESPONSE SENT:
-------------------------------------------
%s
-------------------------------------------"""% (name, text, myPost)

		except:
			# Prevent crash if twitter API blocks post
			print '15 posts per 15 minutes exceeded'

		else:
			print '%s has been contacted before, ignoring their tweet:\n %s' % (name, text)

	else:
		print 'No hits'

def extract(tweet):
# Extract useful data from tweet dictionary
	dictionary = tweet[0]

	text = dictionary['text']
	# Remove emoji & non-roman characters
	text = filter(lambda x: x in string.printable, text)
	# Remove any empty lines that confuse the history check
	text = text.replace('\n', '  ')

	userPortion = dictionary['user'] # User details are in a sub-dictionary named 'user'
	name = userPortion['screen_name']

	return (name, text)

def post(message):
# Post preset tweet online
	if DEBUG:
		print 'DEBUG: Sending:\n%s' % message
	twitter.tweet_function(account, message)

# ----------------------------------------------------------------------------------------
# THIS RECORDS ALL OF OUR TWEETS TO PREVENT SPAM & FOR ANALYTICS
def record(customer, theirPost, myPost):
# Makes a note of each tweet caught & what was sent in return 
# RETURNS True IF THIS CUSTOMER HASN'T BEEN CONTACTED BEFORE
	if os.path.exists(postHistory):
		# Read all post history
		if DEBUG:
			print 'DEBUG: Loading post history'
		historyFile = open(postHistory, 'r', 0)
		history = historyFile.read()
		historyFile.close()
		history = history.split('\n')

		for line in history:
			logEntry = line.split('|')
			if customer in logEntry:
				if DEBUG:
					print 'DEBUG: %s found in post history' % customer
				# We've tweeted at this customer before, ignore their tweet
				return False
			else:
				# Never contacted this customer before, so save their details
				historyFile = open(postHistory, 'a', 0)
				historyFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
				historyFile.close()	
				if DEBUG:
					print "DEBUG: Added record of %s's tweet to post history" % customer			
				return True
	else:
		# No history file so create a new one with this first tweet included
		if DEBUG:
			print 'DEBUG: Creating post history log'
		newFile = open(postHistory, 'w', 0)
		newFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
		newFile.close()
		if DEBUG:
				print "DEBUG: Added record of %s's tweet to post history" % customer
		# No history log so we know we've never tweeted to this customer before
		return True


# ----------------------------------------------------------------------------------------
# THIS IS THE MAIN LOOP OF THE PROGRAM THAT BRINGS ALL OF THE ABOVE TOGETHER
def main():
	print 'TWEETBOT is running'
	if DEBUG:
		print 'DEBUG MODE ON'
	print '------------------------'
	print '%s  |  %sm' % (account, interval)
	print '------------------------'
	newFile()
	matchPosts()

	while True:
		hits = scan()
		print '==========================================='
		print 'Sleeping for %s min' % interval
		time.sleep(interval*60)
			
if __name__ == '__main__':
	main()
