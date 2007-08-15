#!/usr/bin/env python
"""
thanks.py - Thankfulness Functionality
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def f_thanks(self, origin, match, args): 
   self.msg(origin.sender, random.choice(
      ["No problem.", "You're welcome.", "Not at all.", 
       "Don't mention it.", "You're welcome."]
   ))
f_thanks.rule = r'(?i)^(thanks|cheers|ta|thank you),? $nick[!.]?$'
