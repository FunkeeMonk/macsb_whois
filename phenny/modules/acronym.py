#!/usr/bin/env python
"""
acronym.py - Acronym Functionality
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import web

def f_acronym(self, origin, match, args): 
   """.acronym <word> - Make an acronym from <word>."""
   word = match.group(1).lower()
   if not word.isalpha(): 
      err = 'Sorry, words must be alphabetical.'
      self.msg(origin.sender, origin.nick + ': ' + err)
      return 
   acronym = web.get('http://inamidst.com/misc/acronym/' + word)
   self.msg(origin.sender, acronym)
f_acronym.rule = (['acronym'], r'(\S+)')
f_acronym.thread = True
