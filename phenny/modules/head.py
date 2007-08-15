#!/usr/bin/env python
"""
head.py - HTTP HEAD Utilities
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import web

def f_httphead(self, origin, match, args): 
   """.head <URI> <FieldName>? - Perform an HTTP HEAD on URI."""
   uri = match.group(1)
   header = match.group(2)

   try: info = web.head(uri)
   except IOError: 
      self.msg(origin.sender, "Can't connect to %s" % uri)
      return

   if not isinstance(info, list): 
      info = dict(info)
      info['Status'] = '200'
   else: 
      newInfo = dict(info[0])
      newInfo['Status'] = str(info[1])
      info = newInfo

   if header is None: 
      msg = 'Status: %s (for more, try ".head uri header")' % info['Status']
      self.msg(origin.sender, msg)
   else: 
      headerlower = header.lower()
      if info.has_key(headerlower): 
         self.msg(origin.sender, header + ': ' + info.get(headerlower))
      else: 
         msg = 'There was no %s header in the response.' % header
         self.msg(origin.sender, msg)
f_httphead.rule = (['head'], r'(\S+)(?: +(\S+))?')
f_httphead.thread = True
