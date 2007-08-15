#!/usr/bin/env python
"""
reload.py - Reload Modules Dynamically
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import irc

def f_reload(self, origin, match, text): 
   name = match.group(1)
   module = getattr(__import__('modules.' + name), name)
   reload(module)

   if hasattr(module, '__file__'): 
      import os.path, time
      mtime = os.path.getmtime(module.__file__)
      modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))
   else: modified = 'unknown'

   self.register(vars(module))
   self.bindrules()

   msg = '%r (version: %s)' % (module, modified)
   self.msg(origin.sender, origin.nick + ': ' + msg)
f_reload.rule = ('$nick', ['reload'], r'(\S+)')
