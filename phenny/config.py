#!/usr/bin/env python
"""
config.py - Configuration File
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

# Default nickname for phenny
nick = 'macsb_whois'

# Server to run phenny on
host = 'irc.freenode.net'

# Phenny's current owner
# Change this to your own nickname!
owner = 'FunkeeMonk'

# Directory to store all the data. Must be writable
datadir = '/Users/funkeemonk/Desktop/IRC Bot'

# Channels for phenny to join 
channels = [
	'#macsb'
]

# Channels for phenny to join in test mode
testchannels = [
   '#testphenny'
]

# Delay before reconnecting, in seconds
delay = 10

# [EOF]
