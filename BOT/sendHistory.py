#!/usr/bin/python

import gmail
import datetime

sender = 'BOTkitsune@gmail.com'
password = 'kitsune2211'

def sendAll(to, content):
	subject = 'KITSUNE: Full interaction history (manual request)'
	message = "Below is the full history of Twitter interactions carried out by the KITSUNE bot."
	timeStamp = 0
	for line in content:
                line = line.split('|')
                pastTimeStamp = timeStamp
                timeStamp = line[0]
                if timeStamp != pastTimeStamp:
                        lineOne = '-----%s-----\n' % timeStamp
		else:
			lineOne = '\n'
                lineTwo = 'USER: \n%s\n' % line[1]
                lineThree = 'TWEET: \n%s\n' % line[2]
                lineFour = 'RESPONSE: \n%s\n' % line[3]

		message = '%s\n%s%s%s%s' % (message, lineOne, lineTwo, lineThree, lineFour)
	
	gmail.message(sender, password, to, subject, message)

def sendRecent(to, content):
	subject = 'KITSUNE: Recent interaction history.'
	message = "Below are all the Twitter interactions from the past 24 hours."
	timeStamp = 0
	for line in content:
                line = line.split('|')
                pastTimeStamp = timeStamp
                timeStamp = line[0]
		
		if compareTime(timeStamp, getTime()) == True:

	                if timeStamp != pastTimeStamp:
	                        lineOne = '-----%s-----\n' % timeStamp
			else:
				lineOne = '\n'
	                lineTwo = 'USER: \n%s\n' % line[1]
	                lineThree = 'TWEET: \n%s\n' % line[2]
	                lineFour = 'RESPONSE: \n%s\n' % line[3]
	
			message = '%s\n%s%s%s%s' % (message, lineOne, lineTwo, lineThree, lineFour)
	
	gmail.message(sender, password, to, subject, message)
	
def getTime():
	now = datetime.datetime.now()
	currentTime = now.strftime('%d.%m.%y %H:%M')
	return currentTime

def compareTime(timestamp, currentTime):
# Check if the timestamp from postHistory is from less than 24hrs ago
	# Separate timestamp strings into more easily compared lists
	stampList = timestamp.split(' ')
	stampDate = stampList[0]
	stampDate = stampDate.split('.')

	currentList = currentTime.split(' ')
	currentDate = currentList[0]
	currentDate = currentDate.split('.')

	if stampDate[2] == currentDate[2]:
	# The years match
		if stampDate[1] == currentDate[1]:
		# The months match
			if int(stampDate[0]) == int(currentDate[0]) -1:
			# The day is yesterday
				check = True
			else:
			# The day isn't yesterday
				check = False
		else:
		# The months don't match
			check = False
	else:
	# The years don't match
		check = False

	return check

if __name__ == '__main__':

        newFile = open('DATA/postHistory.log', 'r', 0)
        history = newFile.read()
        newFile.close()

        history = history.split('\n')
        history.pop()

	sendRecent('xxx',history)
