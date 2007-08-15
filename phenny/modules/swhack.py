#!/usr/bin/env python
"""
swhack.py - Swhack Log Tailer
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re, urllib

def formatnumber(n): 
   parts = list(str(n))
   for i in range((len(parts) - 3), 0, -3):
      parts.insert(i, ',')
   return ''.join(parts)

def f_swhacktail(self, origin, match, args): 
   """.swhack <s> - Search for <s> in Swhack's logs."""
   # Check that we're in #swhack or #inamidst
   if not (origin.sender in ['#swhack', '#inamidst', '#d8uv.org']): 
      return

   pattern = match.group(1)

   # Compile the regexp given, if we can, with case-insensitive flag
   try: re.compile('(?i)' + pattern)
   except Exception, e: 
      msg = origin.nick + ": %r isn't a valid regexp (%s)." % (pattern, e)
      self.msg(origin.sender, msg)
      return

   u = urllib.urlopen('http://swhack.com/logs/tail', data=pattern)
   result = u.read()
   u.close()

   results = result.splitlines()
   if results: 
      self.msg(origin.sender, origin.nick + ': ' + results[0])
      for line in results[1:]: 
         self.msg(origin.sender, '[off] ' + line)
   else: 
      msg = 'No results for "%s".' % pattern
      self.msg(origin.sender, origin.nick + ': ' + msg)
f_swhacktail.rule = (['swhack', 'tail'], r'(.*)')
f_swhacktail.thread = True

def f_swhackorigin(self, origin, match, args):
   """.origin <nick> - Find when <nick> first joined Swhack."""
   # Check that we're in #swhack or #inamidst
   if not (origin.sender in ['#swhack', '#inamidst']):
      return

   nickname = match.group(1)
   if len(nickname) > 20: return

   u = urllib.urlopen('http://swhack.com/logs/origin', nickname)
   bytes = u.read()
   u.close()

   lines = bytes.splitlines()
   if len(lines) == 0: 
      self.msg(origin.sender, "Can't find info about %s*." % nickname)
   else: 
      date = lines[0][:19]
      i = lines[0].find('<')
      j = lines[0].find('>')
      nickname = lines[0][i+1:j]
      if len(lines) == 1: 
         msg = "First saw %s on #swhack at %s, saying %r"
         saying = lines[0][lines[0].find('> ')+2:]
      else: 
         msg = "First saw %s on #swhack at %s, who then first said %r"
         saying = lines[1][lines[1].find('> ')+2:]
      uri = date.replace(' ', '#T').replace(':', '-')
      uri = 'http://swhack.com/logs/' + uri
      msg = msg + (' (see %s)' % uri)
      self.msg(origin.sender, msg % (nickname, date, saying))
f_swhackorigin.rule = (['origin'], r'(.*)')
f_swhackorigin.thread = True

def f_swhackcount(self, origin, match, args):
   """.swhackcount <nick> - Count <nick>'s words on Swhack."""
   # Check that we're in #swhack or #inamidst
   if not (origin.sender in ['#swhack', '#inamidst']):
      return

   nickname = match.group(1)
   if len(nickname) > 20: return

   u = urllib.urlopen('http://swhack.com/count', nickname)
   bytes = u.read()
   u.close()

   n = bytes.strip()
   n = formatnumber(n)

   self.msg(origin.sender, '%s: %s words' % (nickname, n))
f_swhackcount.rule = (['swhackcount'], r'(.*)')
f_swhackcount.thread = True

def f_swhackcount2007(self, origin, match, args):
   """.swhackcount2007 <nick> - Count <nick>'s words on Swhack."""
   # Check that we're in #swhack or #inamidst
   if not (origin.sender in ['#swhack', '#inamidst']):
      return

   nickname = match.group(1)
   if len(nickname) > 20: return

   u = urllib.urlopen('http://swhack.com/count2007', nickname)
   bytes = u.read()
   u.close()

   n = bytes.strip()
   n = formatnumber(n)

   self.msg(origin.sender, '%s: %s words' % (nickname, n))
f_swhackcount2007.rule = (['swhackcount2007'], r'(.*)')
f_swhackcount2007.thread = True

def f_wordlength2007(self, origin, match, args):
   """.wordlength2007 <nick> - Count <nick>'s wordlength on Swhack."""
   # Check that we're in #swhack or #inamidst
   if not (origin.sender in ['#swhack', '#inamidst']):
      return

   nickname = match.group(1)
   if len(nickname) > 20: return

   u = urllib.urlopen('http://swhack.com/wordlength2007', nickname)
   bytes = u.read()
   u.close()

   n = bytes.strip()

   self.msg(origin.sender, '%s: average %s bytes/word' % (nickname, n))
f_wordlength2007.rule = (['wordlength2007'], r'(.*)')
f_wordlength2007.thread = True
