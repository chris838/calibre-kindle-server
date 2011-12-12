#!/usr/bin/python

''' Deliver all ebooks to the Kindle via e-mail '''

import subprocess
import ConfigParser
import shlex

# Load config settings
config = ConfigParser.ConfigParser()
config.read('settings.cfg')


# Build command list
command_list = ['calibre-smtp',
'-vv',
'--attachment', 'ebooks/test.txt',
'--subject', 'convert',
'--password', config.get('Delivery', 'smtp_password'),
'--port', config.get('Delivery', 'smtp_port'),
'--relay', config.get('Delivery', 'smtp_server'),
'--username', config.get('Delivery', 'smtp_username'),
config.get('Delivery', 'smtp_username'),
config.get('Delivery', 'kindle_address'),
'Automated message sent from Calibre Kindle Server']


# Send email using calibre's command line SMTP tool
subprocess.call( command_list )
