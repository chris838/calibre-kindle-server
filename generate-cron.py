#!/usr/bin/python

''' Create and install a .cron table using the current folder and contents of settings.cfg. '''

import subprocess
import ConfigParser
import os


# Load config settings
config = ConfigParser.ConfigParser()
config.read('settings.cfg')


# Work out current directory
delivery_script_path = os.path.join( os.getcwd(), 'deliver.py' )
rp_script_path = os.path.join( os.getcwd(), 'proces-recipes.py' )

# Generate the delivery crontab row
idle_start = float( config.get('Delivery', 'idle_time_start') )
idle_end = float( config.get('Delivery', 'idle_time_end') )
idle_time = 0
if (idle_start > idle_end) : 
    idle_time = (24 - idle_start) + idle_end
else : 
    idle_time = idle_end - idle_start
active_time = 24 - idle_time
delivery_frequency = int( config.get('Delivery', 'frequency') )
delivery_period = active_time / delivery_frequency
delivery_rows = ''
for i in range(0, delivery_frequency) :
    num_mins = int( round( ( (idle_end + i*delivery_period) % 24) * 60) )
    h, m = divmod(num_mins, 60)
    delivery_row = str(m) + ' ' + str(h) + ' * * *    ' + delivery_script_path
    delivery_rows += delivery_row + '\n'


# Generate the recipe processing crontab row
rp_frequency = int( config.get('Recipe processing', 'frequency') )
mins_str = '0'
for i in range(1, rp_frequency) :
    mins_str += ','
    num_mins = int(round( (60 / rp_frequency)*i ))
    mins_str += str(num_mins)
rp_rows = mins_str + ' * * * *     ' + rp_script_path
rp_rows += '\n'


# Generate the .cron file
cron_file = open('calibre-kindle.cron', 'w') 
cron_str = '''# Autogenerated crontab schedule for Calibre Kindle Server

SHELL=/bin/bash
PATH=/bin:/usr/bin:/usr/local/bin

# m h  d m y	command
'''

cron_str += delivery_rows
cron_str += rp_rows

cron_file.write( cron_str )


# Run crontab on the .cron file to install
