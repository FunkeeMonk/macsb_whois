#!/usr/bin/env python
"""
thesaurus.py - Thesaurus Functionality
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re, textwrap
import web

def f_thesaurus(self, origin, match, args): 
   """.thesaurus <word> - Get <word>'s synonyms."""
   # 2004-07-13 17:10Z <evangineer> tell sbp` can we have a .thesaurus 
   # or .synonym feature for phenny that just outputs the synonyms please?
   word = match.group(1)
   uri = 'http://thesaurus.reference.com/search?q=' + web.urllib.quote(word)
   s = web.get(uri)

   striphtml = lambda s: re.sub(r'<[^!?>][^>]*>', '', s)
   r_thesaurus = re.compile(r'<b>Synonyms:</b>[^\r\n]+<td>([^\r\n]*)</td>')
   m = r_thesaurus.search(s)
   if m: 
      result = m.group(1)
      result = striphtml(result)[:500]
      result = ["%s synonyms: %s" % (word, line)
                for line in textwrap.wrap(result, 200)][:2]
      self.msglines(origin.sender, result)
   else: 
      msg = "%s: sorry, no synonyms found for %s"
      self.msg(origin.sender, msg % (origin.nick, word))
f_thesaurus.rule = (['thesaurus', 'synonym'], r'(\w+)')
f_thesaurus.thread = True
