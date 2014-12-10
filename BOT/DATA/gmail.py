#!/usr/bin/python

# ----- GMAIL INTERFACE MODULE -----
# Allows the Pi to send emails via a pre-authorised gmail account

# v1.0:
# Secure log in
# Send email to any address with any subject & content
# Attach file to message
# List unread messages

# Not yet implemented:
# Read messages

import smtplib
import string
import poplib
from email import parser

import email
import mimetypes
import email.mime.application

def login(sender, password):
	# Checks log-in credentials
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)     # NOTE:  This is the GMAIL SSL port.
	try:
		server.login(sender, password)
		server.quit()
		return True
	except:
		return False

def message(sender, password, to, subject, message):
	# Send message (text only)
	note = " (via GM's rPi emailApp)"

	SUBJECT = subject + note
	TO = to
	FROM = sender
	text = message 
	BODY = string.join((
	    'From: %s' % FROM,
	    'To: %s' % TO,
	    'Subject: %s' % SUBJECT,
	    '',
	    text
	    ), '\r\n')

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login(sender, password)
	server.sendmail(FROM, [TO], BODY)

	server.quit()

def attach(sender, password, to, subject, message, filename):
	# Create a text/plain message
	note = " (via GM's rPi emailApp)"

	msg = email.mime.Multipart.MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = to

	# The main body is just another attachment
	body = email.mime.Text.MIMEText(message)
	msg.attach(body)

	# Attachment
	fp=open(filename,'rb')
	att = email.mime.application.MIMEApplication(fp.read(),_subtype="dat")
	fp.close()
	att.add_header('Content-Disposition','attachment',filename=filename)
	msg.attach(att)

	# send via gmail
	s = smtplib.SMTP('smtp.gmail.com')
	s.starttls()
	s.login(sender, password)
	s.sendmail(sender, [to], msg.as_string())
	s.quit()

def read(username, password):
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(username)
	pop_conn.pass_(password)

	#Get messages from server:
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

	# Concat message pieces:
	messages = ["\n".join(mssg[1]) for mssg in messages]

	#Parse message intom an email object:
	messages = [parser.Parser().parsestr(mssg) for mssg in messages]
	for message in messages:
	    print message['subject']
	print pop_conn.list()[1]
	pop_conn.quit()
