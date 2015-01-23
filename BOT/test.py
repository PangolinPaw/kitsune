#!/usr/bin/python

# This is version 1

def update():
	os.system('sudo git pull origin master')
	print 'Update complete'

if __name__ == '__main__':
	update()
