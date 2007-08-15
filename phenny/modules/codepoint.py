#!/usr/bin/env python
"""
codepoint.py - Unicode Utilities
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re

def f_codepoint(self, origin, match, args): 
   """.cp <regexp> - Search for a particular Unicode codepoint."""
   result = []
   pattern = match.group(1)
   try: r_pattern = re.compile(r'(?i)' + pattern)
   except: 
      self.msg(origin.sender, '%r is not a valid regexp.' % pattern)
      return

   if len(pattern) == 4 or (len(pattern) == 5 and pattern.startswith('^')): 
      p = pattern.lstrip('^')
      try: 
         i = int(p, 16)
         if 0xAC00 <= i <= 0xD7A3: 
            uri = 'http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint='
            self.msg(origin.sender, '%s: %s%04X' % (origin.nick, uri, i))
            return 
      except ValueError, e: 
         pass

   UnicodeData = self.data('UnicodeData.txt')
   if UnicodeData is None: return

   for line in UnicodeData.splitlines() + [
      # See Unicode Specification 4.0.1, p.1411
      # kpreid made me do this
      # Cf. http://swhack.com/logs/2006-09-10#T01-37-39
      'BOOP;Betty;So;0;ON;;;;;N;;;;;'
    ]: 
      if r_pattern.search(line): 
         data = line.split(';')
         if data[0] != 'BOOP': 
            uc = int(data[0], 16)
         else: uc = 'BOOP'

         if 0 < uc < 0xFFFF: 
            # Cf. http://swhack.com/logs/2006-05-04#T11-55-01
            codetype = data[3]
            if codetype == '0': 
               encoded = ' (%s)' % unichr(uc).encode('utf-8')
            else: encoded = ' (\xe2\x97\x8c%s)' % unichr(uc).encode('utf-8')
         elif uc == 'BOOP': 
            encoded = u' (\u00F3,\u00F2)'.encode('utf-8')
         else: encoded = ''

         if (data[1] == '<control>') and (len(data) > 10): 
            name = '<control> - ' + data[10]
         else: name = data[1]

         result.append(data[0] + ': ' + name + encoded)
   if not result: 
      if '\\' in pattern: 
         pattern = 'r' + ('%r' % pattern).replace('\\\\', '\\')
      elif "'" in pattern: 
         pattern = '%r' % pattern
      else: pattern = "'%s'" % pattern
      self.msg(origin.sender, 'Sorry, no results found for %s.' % pattern)
      return

   out = ''
   for (i, s) in enumerate(result): 
      if i < 2: out += '%s\n' % s
      elif i == 2: out += '%s \x02[...]\x02\n' % s
   self.msglines(origin.sender, out.splitlines())
f_codepoint.rule = (['cp', 'codepoint'], r'(.*)')
f_codepoint.thread = True

def f_podecoint(self, origin, match, args): 
   """.pc <utf-8> - Discover a utf-8 encoded codepoint."""
   input = match.group(1)
   input = input.decode('utf-8')

   class Blargh: pass
   for character in input[:3]: 
      match = Blargh()
      match.group = lambda *args: r'^%04X\b' % ord(character)
      self.f_codepoint(origin, match, args)
f_podecoint.rule = (['pc', 'podecoint'], r'(.*)')
f_podecoint.thread = True

def f_charinfo(self, origin, match, args): 
   """.char <seq> - Get info about a sequence."""
   import unicodedata
   input = match.group(1)

   chars = {
      '\xa3': u'\u00A3', 
      'E/': u'\u00C9', 
      'a\\': u'\u00E0', 
      'ae': u'\u00E6', 
      'e\\': u'\u00E8', 
      'e/': u'\u00E9', 
      'i/': u'\u00ED', 
      'o^': u'\u00F4', 
      'o:': u'\u00F6', 
      '|': u'\u017F', 
      'long s': u'\u017F', 
      'long-s': u'\u017F', 
      '--': u'\u2014', 
      '->': u'\u2192'
   }

   if chars.has_key(input): 
      char = chars[input]
   else: char = unicode(input, 'utf-8')[:1]

   if char: 
      cp = ord(char)
      name = unicodedata.name(char).title()
      msg = '&#x%04X; - %s (%s)' % (cp, name, char.encode('utf-8'))
      self.msg(origin.sender, msg)
   else: self.msg(origin.sender, '%s: sorry, no such char' % origin.nick)
f_charinfo.rule = (['char', 'charinfo'], r'(.*)')
f_charinfo.thread = True

def f_unicode(self, origin, match, args): 
   import unicodedata
   label = match.group(1).upper()
   r_label = re.compile('\\b' + label.replace(' ', '.*\\b'))
   results = []
   for i in xrange(0xFFFF): 
      try: name = unicodedata.name(unichr(i))
      except ValueError: continue
      if r_label.search(name): 
         results.append((len(name), i))
   if not results: 
      self.msg(origin.sender, 'Error: no results found')
      return
   name, u = sorted(results)[0]
   cp = unichr(u).encode('utf-8')
   msg = 'U+%04X %s (%s)' % (u, unicodedata.name(unichr(u)), cp)
   self.msg(origin.sender, msg)
f_unicode.rule = (['unicode'], r'(.*)')
f_unicode.thread = True
