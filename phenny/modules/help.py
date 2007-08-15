#!/usr/bin/env python
"""
help.py - Help Facilities
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

def f_chelp(self, origin, match, args): 
   command = match.group(1).rstrip('?!')
   if self.doc.has_key('f_' + command): 
      self.msg(origin.sender, '%r' % self.doc['f_' + command])
   elif self.doc.has_key(command): 
      self.msg(origin.sender, '%r' % self.doc[command])
   else: self.msg(origin.sender, "Sorry, no documentation for %s." % command)

def f_help(self, origin, match, args): 
   if (not args[0].startswith(self.nick)) and origin.sender.startswith('#'): 
      return

   if match.group(1): 
      f_chelp(self, origin, match, args)
      return
   result = ["Hi, I'm %s (a http://inamidst.com/phenny/)" % self.nick]

   keys = []
   for key in sorted(self.doc.keys()): 
      if key.startswith('f_'): 
         key = key[2:]
      keys.append(key)

   result.append('Commands: ' + ', '.join(keys))
   try: 
      import config
      if hasattr(config, 'owner'): 
         owner = config.owner
      else: owner = 'sbp'
   except ImportError: 
      owner = 'sbp'
   result.append(('Try "%s: help command?" if stuck. ' % self.nick) + 
                  'My owner is %s.' % owner)
   self.msglines(origin.sender, result)
f_help.rule = ('$nick', ['help'], r'(.*)')
