#!/usr/bin/env python
"""
irc.py - A Utility IRC Bot
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import sys, re, time, traceback
import socket, asyncore, asynchat

class Origin(object): 
   source = re.compile(r'([^!]*)!?([^@]*)@?(.*)')

   def __init__(self, bot, source, args): 
      match = Origin.source.match(source or '')
      self.nick, self.user, self.host = match.groups()

      if len(args) > 1: 
         target = args[1]
      else: target = None

      mappings = {bot.nick: self.nick, None: None}
      self.sender = mappings.get(target, target)

class Bot(asynchat.async_chat): 
   def __init__(self, nick, channels): 
      asynchat.async_chat.__init__(self)
      self.set_terminator('\r\n')
      self.buffer = ''

      self.nick = nick
      self.user = nick
      self.name = nick

      self.verbose = True
      self.channels = channels or []

   def write(self, args, text=None): 
      if text is not None: 
         self.push(' '.join(args) + ' :' + text + '\r\n')
      else: self.push(' '.join(args) + '\r\n')

   def run(self, host, port=6667): 
      self.initiate_connect(host, port)

   def initiate_connect(self, host, port): 
      if self.verbose: 
         message = 'Connecting to %s:%s...' % (host, port)
         print >> sys.stderr, message,
      self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
      self.connect((host, port))
      asyncore.loop()

   def handle_connect(self): 
      if self.verbose: 
         print >> sys.stderr, 'connected!'
      self.write(('NICK', self.nick))
      self.write(('USER', self.user, '+iw', self.nick), self.name)

   def handle_close(self): 
      self.close()
      print >> sys.stderr, 'Closed!'

   def collect_incoming_data(self, data): 
      self.buffer += data

   def found_terminator(self): 
      line = self.buffer
      self.buffer = ''

      if line.startswith(':'): 
         source, line = line[1:].split(' ', 1)
      else: source = None

      if ' :' in line: 
         argstr, text = line.split(' :', 1)
      else: argstr, text = line, ''
      args = argstr.split()

      origin = Origin(self, source, args)
      self.dispatch(origin, tuple([text] + args))

      if args[0] == 'PING': 
         self.write(('PONG', text))
      elif args[0] == '251': 
         self.msg('NickServ', 'IDENTIFY macsb_rocks')
         # Vanilla and ircu/asuka ircds at least seem to require this
         # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
         for channel in self.channels: 
            self.write(('JOIN', channel))
         #self.write(('TOPIC #macsb :#macsb - /msg macsb_whois .whois <nick> to find out more about the devs here.  Update your profile at http://macsb.ironcoder.org/wiki/WhoIsWho for the bot to recognize you.', ''))

   def dispatch(self, origin, args): 
      pass

   def filter(self, text): 
      return True

   def msg(self, recipient, text): 
      # Cf. http://swhack.com/logs/2006-03-01#T19-43-25
      if isinstance(text, unicode): 
         try: text = text.encode('utf-8')
         except UnicodeEncodeError, e: 
            text = e.__class__ + ': ' + str(e)

      if self.filter(text): 
         self.write(('PRIVMSG', recipient), text)
      return text

   def msglines(self, channel, lines): 
      for line in lines: 
         if line: 
            self.msg(channel, line)
         time.sleep(1)

         if len(line) > 50: 
            time.sleep(0.7)

   def notice(self, dest, text): 
      self.write(('NOTICE', dest), text)

   def error(self, origin): 
      try: 
         import traceback
         trace = traceback.format_exc()
         lines = list(reversed(trace.splitlines()))

         report = [lines[0].strip()]
         for line in lines: 
            line = line.strip()
            if line.startswith('File "/'): 
               report.append(line[0].lower() + line[1:])
               break
         else: report.append('source unknown')

         self.msg(origin.sender, report[0] + ' (' + report[1] + ')')
      except: self.msg(origin.sender, "Got an error.")

class TestBot(Bot): 
   def f_ping(self, origin, match, args): 
      delay = m.group(1)
      if delay is not None: 
         import time
         time.sleep(int(delay))
         self.msg(origin.sender, 'pong (%s)' % delay)
      else: self.msg(origin.sender, 'pong')
   f_ping.rule = r'^\.ping(?:[ \t]+(\d+))?$'

def main(): 
   # bot = TestBot('testbot', ['#d8uv.com'])
   # bot.run('irc.freenode.net')
   print __doc__

if __name__=="__main__": 
   main()
