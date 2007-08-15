#!/usr/bin/env python
"""
timing.py - Show The Time
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import time

TimeZones = {'KST': 9, 'CADT': 10.5, 'EETDST': 3, 'MESZ': 2, 'WADT': 9, 
             'EET': 2, 'MST': -7, 'WAST': 8, 'IST': 5.5, 'B': 2, 
             'MSK': 3, 'X': -11, 'MSD': 4, 'CETDST': 2, 'AST': -4, 
             'HKT': 8, 'JST': 9, 'CAST': 9.5, 'CET': 1, 'CEST': 2, 
             'EEST': 3, 'EAST': 10, 'METDST': 2, 'MDT': -6, 'A': 1, 
             'UTC': 0, 'ADT': -3, 'EST': -5, 'E': 5, 'D': 4, 'G': 7, 
             'F': 6, 'I': 9, 'H': 8, 'K': 10, 'PDT': -7, 'M': 12, 
             'L': 11, 'O': -2, 'MEST': 2, 'Q': -4, 'P': -3, 'S': -6, 
             'R': -5, 'U': -8, 'T': -7, 'W': -10, 'WET': 0, 'Y': -12, 
             'CST': -6, 'EADT': 11, 'Z': 0, 'GMT': 0, 'WETDST': 1, 
             'C': 3, 'WEST': 1, 'CDT': -5, 'MET': 1, 'N': -1, 'V': -9, 
             'EDT': -4, 'UT': 0, 'PST': -8, 'MEZ': 1, 'BST': 1, 
             'ACS': 9.5, 'ATL': -4, 'ALA': -9, 'HAW': -10, 'AKDT': -8, 
             'AKST': -9, 
             'BDST': 2}

People = {
   'd8uv': 'America/Anchorage', 
   'sbp': 'Europe/London', # Actually UK...
   'crschmidt': 'America/New_York', # Actually Boston...
   'patbam': 'America/New_York', # Actually just nearish to NY
   'chryss': 'Europe/London', 
   'jgalvez': 'America/Sao_Paulo', 
}

def f_time(self, origin, match, args): 
   """.t [ <timezone> ] - Returns the current time"""
   tz = match.group(1) or 'GMT'
   # Personal time zones, because they're rad
   if People.has_key(tz): 
      tz = People[tz]
   elif (not match.group(1)) and People.has_key(origin.nick): 
      tz = People[origin.nick]
   TZ = tz.upper()
   if len(tz) > 30: return

   # self.msg(origin.sender, 'TZ:' + repr(tz) + ':' + repr(TZ))

   if (TZ == 'UTC') or (TZ == 'Z'): 
      msg = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
      self.msg(origin.sender, msg)
   elif TimeZones.has_key(TZ): 
      offset = TimeZones[TZ] * 3600
      timenow = time.gmtime(time.time() + offset)
      msg = time.strftime("%a, %d %b %Y %H:%M:%S " + str(TZ), timenow)
      self.msg(origin.sender, msg)
   elif tz and tz[0] in ('+', '-') and 4 <= len(tz) <= 6: 
      timenow = time.gmtime(time.time() + (int(tz[:3]) * 3600))
      msg = time.strftime("%a, %d %b %Y %H:%M:%S " + str(tz), timenow)
      self.msg(origin.sender, msg)
   else: 
      try: t = float(tz)
      except ValueError: 
         import os, re, subprocess
         r_tz = re.compile(r'^[A-Za-z]+(?:/[A-Za-z_]+)*$')
         if r_tz.match(tz) and os.path.isfile('/usr/share/zoneinfo/' + tz): 
            cmd, PIPE = 'TZ=%s date' % tz, subprocess.PIPE
            proc = subprocess.Popen(cmd, shell=True, stdout=PIPE)
            self.msg(origin.sender, proc.communicate()[0])
         else: 
            error = "Sorry, I don't know about the '%s' timezone." % tz
            self.msg(origin.sender, origin.nick + ': ' + error)
      else: 
         timenow = time.gmtime(time.time() + (t * 3600))
         msg = time.strftime("%a, %d %b %Y %H:%M:%S " + str(tz), timenow)
         self.msg(origin.sender, msg)
f_time.rule = r'^\.(?:t|time)(?: +(\S+))?$'

def f_beats(self, origin, match, args): 
   """.beats - Returns the current internet time"""
   import math
   beats = ((time.time() + 3600) % 86400) / 86.4
   beats = int(math.floor(beats))
   self.msg(origin.sender, '@' + str(beats))
f_beats.rule = (['beats'], None)

def divide(input, by): 
   return (input / by), (input % by)

def tavtime(s=None): 
   if s is None: 
      s = int(time.time())
   else: s = int(s)

   # Four raels (20 days) + one yi (7 hours)
   # -> 1,753,200 seconds
   quadraels, remainder = divide(s, 1753200)

   raels = quadraels * 4
   # How many raels in the remainder? (432,000 seconds)
   extraraels, remainder = divide(remainder, 432000)
   raels += extraraels

   # If it's 4, we're in yi time!
   if extraraels == 4: 
      avis, remainder = divide(remainder, 21600)
      kins, remainder = divide(remainder, 1200)
      minutes, seconds = divide(remainder, 60)
      return '%s yi %s.%s.%s.%s' % (raels, avis, kins, minutes, seconds)

   # How about avis? (21,600 seconds)
   avis, remainder = divide(remainder, 21600)
   # Kins? (1200 seconds)
   kins, remainder = divide(remainder, 1200)

   minutes, seconds = divide(remainder, 60)
   return '%s.%s.%s.%s.%s' % (raels, avis, kins, minutes, seconds)

def f_tavtime(self, origin, match, args): 
   """.tavtime - Return the current tavtime, possibly with yi."""
   self.msg(origin.sender, tavtime())
f_tavtime.rule = (['tavtime'], None)

# d8uv d8uv d8uv d8uv d8uv d8uv d8uv
# d8uv d8uv d8uv d8uv d8uv d8uv d8uv
# d8uv d8uv d8uv d8uv d8uv d8uv d8uv
# d8uv d8uv d8uv d8uv d8uv d8uv d8uv
# d8uv d8uv d8uv d8uv d8uv d8uv d8uv
