#!/usr/bin/env python
"""
streetmap.py - Streetmap Interface
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re
import web

def f_map(self, origin, match, args): 
   """.map <postcode> - Get a streetmap URI for UK <postcode>."""
   # 2004-07-13 17:26Z <qopi> tell sbp` that a really nice phenny 
   # feature would be .map postcode - it would output a tinyurl for 
   # streetmap, which would be very cool methinks

   postcode = match.group(1)
   uri = 'http://www.streetmap.co.uk/newsearch.srf'
   data = {"mapp": "newmap", 
           "searchp": "newsearch", 
           "name": postcode, 
           "type": "PostCode"}
   data = web.urllib.urlencode(data)

   u = web.urllib.urlopen(uri, data)
   info = u.info()
   if not isinstance(info, list): 
      s = u.read()
   u.close()

   if not isinstance(info, list): 
      r_use = re.compile(r'(?ism)use[\s\r\n]+<a[\s\r\n]+href="([^"]+)"')
      m = r_use.search(s)
      if m: 
         result = unescape(m.group(1))
         self.msg(origin.sender, "%s: %s" % (postcode, result))
      else: 
         msg = "%s: sorry, can't get the URI." % postcode
         self.msg(origin.sender, msg)
   else: 
      result = 'http://www.streetmap.co.uk/' + info[0].get('Location')
      self.msg(origin.sender, "%s: %s" % (postcode, result))
f_map.rule = (['map', 'streetmap'], r'(.*)')
f_map.thread = True
