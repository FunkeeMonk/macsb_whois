#!/usr/bin/env python
"""
wordnet.py - Wordnet Interface
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import re
import web

formuri = 'http://wordnet.princeton.edu/perl/webwn?s='

r_li = re.compile(r'(?ims)<li>.*?</li>')
r_tag = re.compile(r'<[^>]+>')
r_parens = re.compile(r'(?<=\()(?:[^()]+|\([^)]+\))*(?=\))')
r_word = re.compile(r'^[A-Za-z0-9\' -]+$')

def f_wordnet(self, origin, match, args): 
   """.w <word> - Returns the definition of <word> using Wordnet."""
   command = args[0].split()[0].lstrip('.')
   term = match.group(1)

   if origin.sender != '#inamidst': 
      if not r_word.match(term): 
         msg = "Words must match the regexp %s" % r'^[A-Za-z0-9\' -]+$'
         self.msg(origin.sender, origin.nick + ": " + msg)
         return
      if ('--' in term) or ("''" in term) or ('  ' in term): 
        self.msg(origin.sender, origin.nick + ": That's not in WordNet.")
        return

   bytes = web.get(formuri + web.urllib.quote(term)) # @@ ugh!
   items = r_li.findall(bytes)

   nouns, verbs, adjectives = [], [], []
   for item in items: 
      item = r_tag.sub('', item)
      chunks = r_parens.findall(item)
      # self.msg(origin.sender, item)
      if len(chunks) < 2: continue

      kind, defn = chunks[0], chunks[1]
      if command != 'wordnet': 
         defn = defn.split(';')[0]
      if not defn: continue
      defn = defn[0].upper() + defn[1:]

      if kind == 'n': 
         nouns.append(defn)
      elif kind == 'v': 
         verbs.append(defn)
      elif kind == 'adj': 
         adjectives.append(defn)

   if not (nouns or verbs or adjectives): 
      self.msg(origin.sender, "I couldn't find '%s' in WordNet." % term)
      return

   while len(nouns + verbs + adjectives) > 3: 
      if len(nouns) >= len(verbs) and len(nouns) >= len(adjectives): 
         nouns.pop()
      elif len(verbs) >= len(nouns) and len(verbs) >= len(adjectives): 
         verbs.pop()
      elif len(adjectives) >= len(nouns) and len(adjectives) >= len(verbs): 
         adjectives.pop()

   if adjectives: 
      adjectives[-1] = adjectives[-1] + '.'
   elif verbs: 
      verbs[-1] = verbs[-1] + '.'
   elif nouns: 
      nouns[-1] = nouns[-1] + '.'

   for (i, defn) in enumerate(nouns): 
      self.msg(origin.sender, '%s n. %r: %s' % (term, i+1, defn))
   for (i, defn) in enumerate(verbs): 
      self.msg(origin.sender, '%s v. %r: %s' % (term, i+1, defn))
   for (i, defn) in enumerate(adjectives): 
      self.msg(origin.sender, '%s a. %r: %s' % (term, i+1, defn))
f_wordnet.rule = (['w', 'wn', 'wordnet'], r'(.*)')
f_wordnet.thread = True
