#!/usr/bin/env python
"""
devoice.py - For devoicing folk
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

nicks = ['sbp', 'xover', 'd8uv', 'AaronSw', 'kandinski', 'datum', 
         'Morbus', 'crschmidt', 'deltab']
nicks = frozenset(nicks)

def f_devoice(self, origin, match, args): 
   try: text, mode, chan, flags, nick = tuple(args)
   except: return
   if chan == '#swhack': 
      if (nick in nicks) and (flags == '+v'): 
         self.msg('ChanServ', 'V %s -%s' % (chan, nick))
f_devoice.rule = r'(.*)'
f_devoice.command = 'MODE'

# So e.g. for join: 
# def f_join(self, origin, match, args): 
#    self.msg(origin.sender, "%s has joined. args: %s" % args)
# f_join.rule = '(.*)'
# f_join.command = 'JOIN'
