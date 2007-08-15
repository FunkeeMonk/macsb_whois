#!/usr/bin/env python
"""
ping.py - Ping Functionality
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def f_ping(self, origin, match, args): 
   self.msg(origin.sender, 'pong')
f_ping.rule = ('$nick', ['ping'], None)

# @@ Make this obsolete?
def f_pong(self, origin, match, args): 
   msg = random.choice(['er... ping?', 'ping? pang?', 'hmm?'])
   self.msg(origin.sender, msg)
f_pong.rule = ('$nick', ['pong'], None)
