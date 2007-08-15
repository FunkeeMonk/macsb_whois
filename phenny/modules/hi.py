#!/usr/bin/env python
"""
hi.py - Perform Greetings
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def f_hi(self, origin, match, args): 
   reply = random.choice(['Hi', 'Hi', 'Hi', 'Hey', 'Hey', 'Hello'])
   self.msg(origin.sender, '%s %s.' % (reply, origin.nick))
f_hi.rule = r"(?i)^(hi|hey|hello|welcome),? $nick\!?$"

def f_exclaim(self, origin, match, args): 
   self.msg(origin.sender, origin.nick + '!')
f_exclaim.rule = r"(?i)^$nick!$"
