#!/usr/bin/python

''' Deliver all ebooks to the Kindle via e-mail '''

from subprocess import call
import ConfigParser

# Load config settings
config = ConfigParser.ConfigParser()
config.read('settings.cfg')


call(["calibre-smtp", "-h"])

