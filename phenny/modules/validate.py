#!/usr/bin/env python
"""
validate.py - Validate a URI
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import web

def f_validate(self, origin, match, args): 
   """.val <URI> - Validate <URI> using validator.w3.org."""
   # @@ <redmonk> phenny: val http://redmonk.net
   uri = match.group(1)
   path = '/check?uri=%s;output=xml' % web.urllib.quote(uri)
   info = web.head('http://validator.w3.org' + path)

   result = uri + ' is '

   if isinstance(info, list): 
      self.msg(origin.sender, "Got HTTP response %s" % info[1])
      return

   if info.has_key('X-W3C-Validator-Status'): 
      result += str(info['X-W3C-Validator-Status'])
      if info['X-W3C-Validator-Status'] != 'Valid': 
         if info.has_key('X-W3C-Validator-Errors'): 
            n = int(info['X-W3C-Validator-Errors'].split(' ')[0])
            if n != 1: 
               result += ' (%s errors)' % n
            else: result += ' (%s error)' % n
   else: result += 'Unvalidatable: no X-W3C-Validator-Status'

   self.msg(origin.sender, ' ' + result)
f_validate.rule = (['v', 'val', 'validate'], r'(.*)')
f_validate.thread = True
