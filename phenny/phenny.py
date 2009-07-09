#!/usr/bin/env python
"""
phenny.py - Phenny
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import sys, os, re, time, threading, optparse
import irc

if sys.version_info < (2, 4): 
   from sets import Set as set
   def sorted(seq): 
      seq.sort()
      return seq

   msg = "Requires Python 2.4; some modules may be broken."
   print >> sys.stderr, msg

class Phenny(irc.Bot): 
   def __init__(self, nick, password, channels, protect=False): 
      if ('#inamidst' in channels) and (not nick in ('phenny', 'phennytest')): 
         msg = "Error: Don't forget to edit config.py with your own settings!" 
         print >> sys.stderr, msg
         sys.exit(1)

      irc.Bot.__init__(self, nick, password, channels)
      self.protect = protect
      self.initialize()

   def initialize(self): 
      self.datadir = datadir

      # [01:50] <crschmidt> it'd be nice to be able to tell phenny not to load
      # certain modules somehow
      # [01:50] <crschmidt> that way i could centralize all my modules in one
      # place
      # [01:50] <crschmidt> symlink my modules dir
      # [01:50] <crschmidt> and have an exclude
      # [02:05] <sbp> I... wow, you're a phenny poweruser

      modules = []
      moduledir = os.path.join(progdir, 'modules')
      for filename in sorted(os.listdir(moduledir)): 
         if filename.endswith('.py') and not filename.startswith('_'): 
            name, ext = os.path.splitext(os.path.basename(filename))
            try: module = getattr(__import__('modules.' + name), name)
            except Exception, e: 
               print >> sys.stderr, "Error loading %s: %s" % (name, e)
            else: 
               if hasattr(module, 'initialize'): 
                  module.initialize(self)
               self.register(vars(module))
               modules.append(name)
      if modules: 
         print >> sys.stderr, 'Registered modules:', ', '.join(modules)

      self.stats = {}
      self.msgstack = []
      self.bindrules()

   def register(self, variables): 
      for name, obj in variables.iteritems(): 
         if hasattr(obj, 'rule'): 
            def wrapper(origin, match, args, self=self, obj=obj): 
               obj(self, origin, match, args)
            for key, value in vars(obj).iteritems(): 
               setattr(wrapper, key, value)
            if hasattr(obj, '__doc__'): 
               wrapper.__doc__ = obj.__doc__
            setattr(self, name, wrapper)

   def bindrules(self): 
      self.short = {}
      self.long = {}
      self.regexps = []
      self.always = []
      self.doc = {}

      for name in dir(self): 
         method = getattr(self, name)
         if hasattr(method, 'rule'): 
            rule = getattr(method, 'rule')

            if hasattr(method, '__doc__'): 
               if method.__doc__: 
                  self.doc[name] = method.__doc__
            thread = hasattr(method, 'thread')

            if hasattr(method, 'command'): 
               command = method.command
            else: command = 'PRIVMSG'

            opts = {'thread': thread, 'command': command}

            if isinstance(rule, tuple): 
               # 1) e.g. (['cp', 'codepoint'], r'(.*)')
               if isinstance(rule[0], list): 
                  if rule[1] is not None: 
                     regexp = re.compile(rule[1])
                  else: regexp = None

                  for short in rule[0]: 
                     self.short[short] = (regexp, method, opts)

               # 2) e.g. ('$nick', ['tell', 'ask'], r'(\S+) (.*)')
               elif isinstance(rule[0], basestring): 
                  if rule[2] is not None: 
                     regexp = re.compile(rule[2])
                  else: regexp = None

                  for long in rule[1]: 
                     self.long[long] = (regexp, method, opts)

            # 3) e.g. r'(.*)'
            elif isinstance(rule, basestring): 
               nick = self.nick.lower()
               nickpat = ''.join('[%s%s]' % (c, c.upper()) for c in nick)
               rule = rule.replace('$nick', nickpat)
               if rule == r'(.*)': 
                  self.always.append((method, opts))
               else: self.regexps.append((re.compile(rule), method, opts))

   def call(self, method, origin, match, args): 
      try: method(origin, match, args)
      except Exception, e: 
         self.error(origin)

   def do(self, command, opts, method, origin, match, args): 
      if len(args) > 1: 
         command = args[1] # Workaround...

      if match and (command == opts.get('command')): 
         if opts.get('thread'): 
            targs = (method, origin, match, args)
            t = threading.Thread(target=self.call, args=targs)
            t.start()
         elif self.protect: 
            self.call(method, origin, match, args)
         else: method(origin, match, args)

   def dispatch(self, origin, args): 
      text, command = args[0], args[1]

      if text.startswith('.'): 
         i = text.find(' ')
         if i < 0: i = len(text)

         short = text[1:i] # overslicing is no problem
         if self.short.has_key(short): 
            regexp, method, opts = self.short[short]
            arg = text[i+1:].lstrip(' \t')

            if regexp is not None: 
               match = regexp.match(arg)
            else: match = True

            self.do(command, opts, method, origin, match, args)

      elif (text.lower().startswith(self.nick.lower() + ': ') or 
            text.lower().startswith(self.nick.lower() + ', ')): 
         rest = text[len(self.nick) + 2:].lstrip(' ')

         i = rest.find(' ')
         if i < 0: i = len(rest)

         long = rest[:i].rstrip('?!')
         if self.long.has_key(long): 
            regexp, method, opts = self.long[long]
            arg = rest[i+1:].lstrip(' \t')

            if regexp is not None: 
               match = regexp.match(arg)
            else: match = True

            self.do(command, opts, method, origin, match, args)

      for (regexp, method, opts) in self.regexps: 
         match = regexp.match(text)
         self.do(command, opts, method, origin, match, args)

      for (method, opts) in self.always: 
         match = True
         command = opts.get('command')
         self.do(command, opts, method, origin, match, args)

   def filter(self, text): 
      # Flood protection
      if self.msgstack.count(text) >= 5: 
         text = '...'
      if self.msgstack.count('...') >= 2: 
         if text == '...': 
            return False
      if len(''.join(self.msgstack[:-3])) > 200: 
         time.sleep(2)

      self.msgstack = self.msgstack[-9:]
      self.msgstack.append(text)
      return True

   def data(self, fn): 
      path = os.path.join(self.datadir, fn)
      if os.path.exists(path): 
         f = open(path, 'rb')
         bytes = f.read()
         f.close()
         return bytes
      else: return None

   def debug(self): 
      print sys.stderr, vars(phenny)
      for command in phenny.rules.keys(): 
         for (method, pattern) in phenny.rules[command]: 
            print >> sys.stderr, method, pattern.pattern

def doubleFork(): 
   # http://swhack.com/logs/2004-05-12#T10-20-11
   # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
   if not hasattr(os, 'fork'): 
      # Cf. http://wpc.pastebin.com/675879
      # and http://swhack.com/logs/2006-04-22#T21-47-07
      return False

   try: 
      pid = os.fork()
      if pid > 0: sys.exit(0)
   except OSError, e: 
      raise OSError("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
   os.chdir("/")
   os.setsid()
   os.umask(0)
   try: 
      pid = os.fork()
      if pid > 0: 
         print "Daemon PID %d" % pid
         sys.exit(0)
   except OSError, e: 
      raise OSError("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
   return True

def run(host, nick, password, channels, protect): 
   phenny = Phenny(nick, password, channels=channels, protect=protect)
   phenny.run(host)

def main(argv=None): 
   parser = optparse.OptionParser(usage='%prog [options]')
   parser.add_option("-n", "--nick", dest="nick", default=False, 
                     help="provides a nickname for the bot")
   parser.add_option("-w", "--password", dest="password", default=False, 
                     help="provides a password for NICKSERV identification for the bot")
   parser.add_option("-t", "--test", dest="test", 
                     action="store_true", default=False, 
                     help="enter testing mode")
   parser.add_option("-p", "--protect", dest="protect", 
                     action="store_true", default=False, 
                     help="protect from errors")
   parser.add_option("-d", "--data", dest="data", default=False, 
                     help="the directory in which to store data")
   options, args = parser.parse_args(argv)

   import config
   global datadir
   global progdir

   nick = options.nick or config.nick
   password = options.password or config.password
   datadir = options.data or config.datadir
   progdir = config.progdir

   if not os.path.isdir(progdir):
      raise IOError("%s is not a directory" % progdir)

   if not os.path.isdir(datadir): 
      raise IOError("%s is not a directory" % datadir)

   # Augment the nickname when testing
   if options.test: 
      nick += 'test'
      protect = options.protect
   else: protect = True

   # Get the channels from args and config
   channels = set()

   for channel in args: 
      if not channel.startswith('#'): 
         channel = '#' + channel
      channels.add(channel)

   if not options.test: 
      channels.update(config.channels)
   else: channels.update(config.testchannels)

   channels = list(channels)

   # Do the double fork trick to prevent having to nohup
   if not options.test: 
      try: result = doubleFork()
      except OSError: pass
      else: 
         if result is False: 
            print >> sys.stderr, "Warning: Couldn't double fork"

   # This bit thanks to Nicolas Mendoza, 2007-05-23
   # Cf. http://utilitybase.com/paste/3519
   while True: 
      run(config.host, nick, password, channels, protect)
      print >> sys.stderr, 'Disconnected; reconnect in', config.delay, 'secs'
      time.sleep(config.delay)

if __name__=="__main__": 
   main()
