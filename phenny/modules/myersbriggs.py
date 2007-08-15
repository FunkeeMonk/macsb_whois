#!/usr/bin/env python
"""
myersbriggs.py - Find Your Myers-Briggs Type
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

types = [
   'ISTJ', 'ISFJ', 'INFJ', 'INTJ', 
   'ISTP', 'ISFP', 'INFP', 'INTP', 
   'ESTP', 'ESFP', 'ENFP', 'ENTP', 
   'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]

def f_myersbriggs(self, origin, match, args):
   """.myersbriggs - Find your Myers-Briggs Type."""
   nick = match.group(1) or origin.nick
   if nick == 'sbp': 
      mtype = 'IUNO'
   elif nick == 'xover': 
      mtype = 'EXPN'
   elif nick == 'deltab': 
      mtype = 'MYST'
   else: 
      num = sum(ord(c) for c in nick)
      index = num % 16
      mtype = types[index]

   if origin.nick == nick: 
      msg = '%s: Your Myers-Briggs type is %s' % (origin.nick, mtype)
      self.msg(origin.sender, msg)
   else: 
      msg = "%s: %s's Myers-Briggs type is %s" % (origin.nick, nick, mtype)
      self.msg(origin.sender, msg)
# f_myersbriggs.rule = (['myersbriggs'], None)
f_myersbriggs.rule = r'^\.myersbriggs(?: +(\S+))?$'
