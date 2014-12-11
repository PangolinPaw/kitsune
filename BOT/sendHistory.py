#!/usr/bin/python

import gmail

sender = 'botkitsune@gmail.com'
password = 'kitsune2211'

def sendAll(to, content):
	subject = 'KITSUNE: Full interaction history (manual request)'
	message = "Below is a full list of bot interactions. They are in the format Timestamp | Username | Thier tweet | Bot's response\n\n"
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
                lineFour = 'RESPONSE: \n%s\n\n' % line[3]

		message = '%s\n%s%s%s%s' % (message, lineOne, lineTwo, lineThree, lineFour)
	
	gmail.message(sender, password, to, subject, message)
