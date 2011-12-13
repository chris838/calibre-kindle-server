#!/usr/bin/python

''' Deliver all ebooks to the Kindle via e-mail '''

import subprocess
import ConfigParser
import sys
import os


# Load config settings
config = ConfigParser.ConfigParser()
config.read('settings.cfg')


# Output will be redirected to files when run from cron
log_dir = config.get('General', 'log_dir')
sys.stdout = open( os.path.join(log_dir,'delivery_py_out.log'), 'w')
sys.stderr = open( os.path.join(log_dir,'delivery_py_err.log'), 'w')
out_file = open( os.path.join(log_dir, 'delivery_out.log'), "w")
err_file = open( os.path.join(log_dir, 'delivery_err.log'), "w")


# Open ebooks directory and loop through all entries
ebooks_dir = config.get('General', 'ebook_dir')
recipes = os.listdir(ebooks_dir)
for recipe in recipes:

    # Build command list
    command_list = ['calibre-smtp',
    '-vv',
    '--attachment', os.path.join( ebooks_dir, recipe),
    '--subject', 'convert',
    '--password', config.get('Delivery', 'smtp_password'),
    '--port', config.get('Delivery', 'smtp_port'),
    '--relay', config.get('Delivery', 'smtp_server'),
    '--username', config.get('Delivery', 'smtp_username'),
    config.get('Delivery', 'smtp_username'),
    config.get('Delivery', 'kindle_address'),
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )
