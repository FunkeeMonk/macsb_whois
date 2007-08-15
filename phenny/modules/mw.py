#!/usr/bin/env python
"""
mw.py - Interface M-W
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re
import web

def unescape(s): 
   s = s.replace('&gt;', '>')
   s = s.replace('&lt;', '<')
   s = s.replace('&amp;', '&')
   return s

def f_mw(self, origin, match, args): 
   """.mw <word> - Search for the definition of word on m-w."""
   # @@ get her to say when she can't find a definition
   uri = "http://www.m-w.com/cgi-bin/dictionary?book=Dictionary&va="
   s = web.get(uri + match.group(1))

   # Munge, munge, munge...
   s = re.sub('<(?!\!)[^>]+>', '', s)
   s = re.sub('[\t ]+', ' ', s)

   main = re.compile('(?ims)^\r?Main Entry: (\S+)').findall(s)
   main = unescape(main.pop().strip('0123456789'))

   pron = re.compile('(?m)^Pronunciation: (\S+)').findall(s)
   pron = unescape(pron.pop())

   funk = re.compile('(?m)^Function: (\S+)').findall(s)
   funk = unescape(funk.pop())
   entry = '%s /%s/, %s' % (main, pron, funk)

   r_ety = '(?sm)^Etymology: ([^\r\n]*)\r\n([^\r\n]*)'
   bits = re.compile(r_ety).findall(s)
   etym, entr = tuple(bits.pop())

   result = []
   result.append('Entry: ' + entry)
   # result.append('Etymology: ' + unescape(etym))
   result.append('Entry: ' + unescape(entr)[:180] + ' [...]')
   self.msglines(origin.sender, result)

def f_safemw(self, origin, match, args): 
   try: f_mw(self, origin, match, args)
   except IndexError: 
      self.msg(origin.sender, '%s: definition not found' % match.group(1))
f_safemw.rule = (['mw'], r'(\w+)')
f_safemw.thread = True
