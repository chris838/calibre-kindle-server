#!/usr/bin/python

''' Process a recipe by downloading and formatting as an ebook, then sending via SMTP '''

import subprocess
import sys
import os
import filecmp
import json


# Deliver to this address
kindle_address = "chrish_71@kindle.com"

# SMTP account settings for outgoing mail
smtp_server = 'smtp.gmail.com'
smtp_port = '587'
smtp_username = 'calibre.kindle.server@gmail.com'
smtp_password = 'password_in_plaintext_please_dont_steal_my_gmail_account_git_users'

# Path to directories
log_dir = 'logs'
recipe_dir = 'recipes'
ebook_dir = 'ebooks'

# Get command line argument for name of recipe
recipe_name = sys.argv[1]

# Output will be redirected to files when run from cron
#sys.stdout = open( os.path.join( log_dir,'py_out.log'), 'w')
#sys.stderr = open( os.path.join( log_dir,'py_err.log'), 'w')
out_file = open( os.path.join( log_dir, 'out.log'), "w")
err_file = open( os.path.join( log_dir, 'err.log'), "w")
       
# Get name of input and output files
ebook = recipe_name + '.mobi'
recipe = recipe_name + '.recipe'

# If old file exists, delete it
if os.path.exists( os.path.join(ebook_dir, 'old', ebook) ) :
    subprocess.call( ['rm', os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# If current file exists, move it to old folder
if os.path.exists( os.path.join(ebook_dir, ebook) ) :
    subprocess.call( ['mv', 
                      os.path.join(ebook_dir, ebook), 
                      os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# Build command list
command_list = ['ebook-convert',
os.path.join( recipe_dir, recipe ),
os.path.join( ebook_dir, ebook ),
'-vv',
'--output-profile', 'kindle']

# Download and format using calibre's command line convert tool
subprocess.call( command_list, stdout=out_file, stderr=err_file )

# If we have downloaded a newer copy :
if True : # not sure how to check this

    print "Sending " + ebook + " over email"

    # Send it over email
    command_list = ['calibre-smtp',
    '-vv',
    '--attachment', os.path.join( ebook_dir, ebook),
    '--subject', 'x',
    '--password', smtp_password,
    '--port', smtp_port,
    '--relay', smtp_server,
    '--username', smtp_username,
    smtp_username,
    kindle_address,
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )

