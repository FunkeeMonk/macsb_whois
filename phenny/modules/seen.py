#!/usr/bin/env python
"""
seen.py - Tell Who's Been Online
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import time

def f_seen(self, origin, match, args): 
   """.seen <nick> - Reports when <nick> was last seen."""
   nick = match.group(1).lower()
   if self.seen.has_key(nick): 
      channel, t = self.seen[nick]
      t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))
      msg = "I last saw %s at %s on %s" % (nick, t, channel)
      self.msg(origin.sender, str(origin.nick) + ': ' + msg)
   else: self.msg(origin.sender, "Sorry, I haven't seen %s around." % nick)
f_seen.rule = (['seen'], r'(\S+)')

def f_note(self, origin, match, args): 
   if not origin: return

   if not hasattr(self, 'seen'): 
      self.seen = {}
   if (len(args) > 2) and args[2].startswith('#'): 
      if args[2] != '#inamidst': # Come to #inamidst to be transparent!
         self.seen[origin.nick.lower()] = (args[2], time.time())

   if not hasattr(self, 'chanspeak'): 
      self.chanspeak = {}
   if (len(args) > 2) and args[2].startswith('#'): 
      self.chanspeak[args[2]] = args[0]
f_note.rule = r'(.*)'
