#!/usr/bin/env python
"""
remind.py - The All Important Reminder Function
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import os, re, time, random
import web

maximum = 4
lispchannels = frozenset([
   '#lisp', 
   '#scheme', 
   '#opendarwin', 
   '#macdev', 
   '#fink', 
   '#jedit', 
   '#dylan', 
   '#emacs', 
   '#xemacs', 
   '#colloquy', 
   '#adium', 
   '#growl', 
   '#chicken', 
   '#quicksilver', 
   '#svn', 
   '#slate', 
   '#squeak', 
   '#wiki', 
   '#nebula', 
   '#myko', 
   '#lisppaste', 
   '#pearpc', 
   '#fpc', 
   '#hprog', 
   '#concatenative', 
   '#slate-users', 
   '#swhack', 
   '#ud', 
   '#t', 
   '#compilers', 
   '#erights', 
   '#esp', 
   '#scsh', 
   '#sisc', 
   '#haskell', 
   '#rhype', 
   '#sicp', 
   '#darcs', 
   '#hardcider', 
   '#lisp-it', 
   '#webkit', 
   '#launchd', 
   '#mudwalker', 
   '#darwinports', 
   '#muse', 
   '#chatkit', 
   '#kowaleba', 
   '#vectorprogramming', 
   '#opensolaris', 
   '#oscar-cluster', 
   '#ledger', 
   '#cairo', 
   '#idevgames', 
   '#hug-bunny', 
   '##parsers', 
   '#perl6', 
   '#sdlperl', 
   '#ksvg', 
   '#rcirc', 
   '#code4lib', 
   '#linux-quebec', 
   '#programmering', 
   '#maxima', 
   '#robin', 
   '##concurrency', 
   '#paredit'
])

def loadReminders(fn): 
   result = {}
   f = open(fn)
   for line in f: 
      line = line.strip()
      if line: 
         tellee, teller, verb, timenow, msg = line.split('\t', 4)
         result.setdefault(tellee, []).append((teller, verb, timenow, msg))
   f.close()
   return result

def dumpReminders(fn, data): 
   f = open(fn, 'w')
   for tellee in data.iterkeys(): 
      for remindon in data[tellee]: 
         line = '\t'.join((tellee,) + remindon)
         f.write(line + '\n')
   f.close()
   return True

def initialize(self): 
   self.remindersFilename = os.path.join(self.datadir, 'reminders.db')
   if not os.path.exists(self.remindersFilename): 
      try: f = open(self.remindersFilename, 'w')
      except OSError: pass
      else: 
         f.write('')
         f.close()
   self.reminders = loadReminders(self.remindersFilename) # @@ tell

def f_remind(self, origin, match, args): 
   """tell <nick> <blargh> - I'll remind nick about blargh."""
   # @@ <eaon> sbp: forget the last "tell" because of a typo?
   teller = origin.nick
   verb = [tok for tok in args[0].split() if tok.strip()][1].strip(',:;\t ')

   # @@ Multiple comma-separated tellees? Cf. Terje, #swhack, 2006-04-15
   tellee, msg = tuple(match.groups())
   tellee = tellee.lower().rstrip(',:;')

   if not os.path.exists(self.remindersFilename): 
      return

   if len(tellee) > 20: 
      self.msg(origin.sender, "%s: That nickname is too long." % teller)
      return 

   timenow = time.strftime('%d %b %H:%MZ', time.gmtime())
   if not tellee in (teller.lower(), self.nick, 'me'): # @@
      # @@ <deltab> and year, if necessary
      warn = False
      if not self.reminders.has_key(tellee): 
         self.reminders[tellee] = [(teller, verb, timenow, msg)]
      else: 
         if len(self.reminders[tellee]) >= maximum: 
            warn = True
         self.reminders[tellee].append((teller, verb, timenow, msg))
      # @@ Stephanie's augmentation
      response = "%s: I'll pass that on when %s is around." % (teller, tellee)
      if warn: response += (" I'll have to use a pastebin, though, so your " + 
                            "message may get lost.")

      rand = random.random()
      if rand > 0.9999: response = "yeah, yeah"
      elif rand > 0.999: response = "%s: yeah, sure, whatever" % teller

      self.msg(origin.sender, response)
   elif teller.lower() == tellee: 
      self.msg(origin.sender, "You can %s yourself that." % verb)
   else: self.msg(origin.sender, "Hey, I'm not as stupid as Monty you know!")

   dumpReminders(self.remindersFilename, self.reminders) # @@ tell
# The + is specifically for jill's double-spacing ways
# I.e. to make phenny love jill as the rest of us do.
# Cf. http://swhack.com/logs/2004-06-30#T06-59-10
f_remind.rule = ('$nick', ['tell', 'ask'], r'(\S+) (.*)')

def getReminders(phenny, channel, key, tellee): 
   lines = []
   template = "%s: %s <%s> %s %s %s"
   today = time.strftime('%d %b', time.gmtime())

   for (teller, verb, datetime, msg) in phenny.reminders[key]: 
      if datetime.startswith(today): 
         datetime = datetime[len(today)+1:]
      lines.append(template % (tellee, datetime, teller, verb, tellee, msg))

   try: del phenny.reminders[key]
   except KeyError: phenny.msg(channel, 'Er...')
   return lines

def f_privremind(self, origin, match, args): 
   if len(args) != 3: return
   text, mtype, channel = args

   if not origin: return
   tellee = origin.nick

   if not os.path.exists(self.remindersFilename): 
      return

   reminders = []
   remkeys = list(reversed(sorted(self.reminders.keys())))
   for remkey in remkeys: 
      if not remkey.endswith('*'): 
         if tellee.lower() == remkey: 
            reminders.extend(getReminders(self, channel, remkey, tellee))
      elif tellee.lower().startswith(remkey.rstrip('*')): 
         reminders.extend(getReminders(self, channel, remkey, tellee))

   self.msglines(channel, reminders[:maximum])
   if reminders[maximum:]: 
      try: 
         if origin.sender in lispchannels: 
            chan = origin.sender
         else: chan = 'None'

         result = web.post('http://paste.lisp.org/submit', 
            {'channel': chan, 
             'username': self.nick, 
             'title': 'Further Messages for %s' % tellee, 
             'colorize': 'None', 
             'text': '\n'.join(reminders[maximum:]) + '\n'
            }
         )
         uris = re.findall('http://paste.lisp.org/display/\d+', result)
         uri = list(reversed(uris)).pop()
         if not origin.sender in lispchannels: 
            message = '%s: see %s for further messages' % (tellee, uri)
            self.msg(channel, message)
      except: self.msg(channel, '(Some messages were elided and lost...)')

   if len(self.reminders.keys()) != remkeys: 
      dumpReminders(self.remindersFilename, self.reminders) # @@ tell
f_privremind.rule = r'(.*)'
