#!/usr/bin/env python

import re, urllib
import web

def language(phrase): 
   languages = {
      'english': 'en', 
      'french': 'fr', 
      'rumantsch': 'fr', 
      'bosnian': 'fr', 
      'spanish': 'es', 
      'romanian': 'es', 
      'portuguese': 'pt', 
      'german': 'de', 
      'italian': 'it', 
      'korean': 'ko', 
      'japanese-shift_jis': 'ja', 
      'unknown': 'ja'
   }
 
   query = urllib.quote(phrase)
   bytes = web.get('http://ziu.let.rug.nl/vannoord_bin/tc?a1=' + query)
   for line in bytes.splitlines(): 
      if '<pre>' in line: 
         language = line[line.find('<pre>') + 5: line.find('</pre>')]
         return languages[language.strip(' \t').lower()]
   return None

r_translation = re.compile(r'<div style=padding:10px;>([^<]+)</div>')

def translate(phrase, lang): 
   babelfish = 'http://world.altavista.com/tr'
   form = {
      'doit': 'done', 
      'intl': '1', 
      'tt': 'urltext', 
      'trtext': phrase, 
      'lp': lang + '_en'
   }

   bytes = web.post(babelfish, form)
   m = r_translation.search(bytes)
   if m: 
      translation = m.group(1)
      translation = translation.replace('\r', '')
      return translation.replace('\n', '')
   return None

def f_translate(self, origin, match, args): 
   """phenny: "<phrase>"? - Translate <phrase>"""
   phrase = match.group(2)

   # if len(phrase) < 15: 
   #    self.msg(origin.sender, origin.nick + ': Phrase must be >= 15 chars.')
   #    return # Unable to guess the language
   try: length = len(phrase.decode('utf-8'))
   except: length = len(phrase)

   if (length > 200) and (origin.nick != 'sbp'): 
      self.msg(origin.sender, origin.nick + ': Phrase must be <= 200 chars.')
      return # Too much input

   try: # thanks to nicomen! cf. http://utilitybase.com/paste/3544
      mlang = match.group(1)
      if mlang: 
         lang = mlang
      else: lang = language(phrase)
   except KeyError, e: 
      msg = "Hmm, got %s..." % str(e).split().pop()
      self.msg(origin.sender, origin.nick + ": " + msg)
      return

   if lang is None: return

   translation = translate(phrase, lang)
   if translation is not None: 
      msg = '"%s" (%s)' % (translation, lang)
      self.msg(origin.sender, origin.nick + ': ' + msg)
f_translate.rule = r'^$nick[,:] +(?:([a-z]{2}) +)?"(.+)"\? *$'
f_translate.thread = True
