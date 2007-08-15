#!/usr/bin/env python
"""
timer.py - Timer Functionality
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import time

def f_timer(self, origin, match, args): 
   """remind me in <hours>:<mins>:<secs> ... - Set a timer."""
   hours, mins, secs = map(int, match.groups())
   if hours > 24: return
   if mins > 59: return
   if secs > 59: return

   seconds = (hours * 3600) + (mins * 60) + secs
   self.msg(origin.sender, '%s: sure' % origin.nick)
   time.sleep(seconds)
   self.msg(origin.sender, "<%s> %s" % (origin.nick, args[0]))
# f_timer.rule = r'(?i)^$nick[:,] +remind me in (\d+):(\d+):(\d+) .*$'
# f_timer.thread = True
