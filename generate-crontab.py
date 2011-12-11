#!/usr/bin/python

''' Deliver all ebooks to the Kindle via e-mail '''

# Load config settings
include "config.h"

from subprocess import call

call('calibre-smtp', '-h')

