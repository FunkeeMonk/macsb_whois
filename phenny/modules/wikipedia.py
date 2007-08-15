#!/usr/bin/env python

import re, urllib
import web

wikiuri = 'http://en.wikipedia.org/wiki/%s'
wikisearch = 'http://en.wikipedia.org/wiki/Special:Search?' \
                    + 'search=%s&fulltext=Search'

r_tr = re.compile(r'(?ims)<tr[^>]*>.*?</tr>')
r_paragraph = re.compile(r'(?ims)<p[^>]*>.*?</p>|<li(?!n)[^>]*>.*?</li>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')
r_redirect = re.compile(
   r'(?ims)class=.redirectText.>\s*<a\s*href=./wiki/([^"/]+)'
)

abbrs = ['etc', 'ca', 'cf', 'Co', 'Ltd', 'Inc', 'Mt', 'Mr', 'Mrs', 
         'Dr', 'Ms', 'Rev', 'Fr', 'St', 'Sgt', 'pron', 'approx', 'lit'] \
   + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') \
   + list('abcdefghijklmnopqrstuvwxyz')
t_sentence = r'^.{5,}?(?<!\b%s)(?:\.(?= [A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % r')(?<!\b'.join(abbrs))

def unescape(s): 
   s = s.replace('&gt;', '>')
   s = s.replace('&lt;', '<')
   s = s.replace('&amp;', '&')
   s = s.replace('&#160;', ' ')
   return s

def text(html): 
   html = r_tag.sub('', html)
   html = r_whitespace.sub(' ', html)
   return unescape(html).strip()

def search(term): 
   try: import google
   except ImportError, e: 
      print e
      return term

   term = term.replace('_', ' ')
   uri = google.google('site:en.wikipedia.org %s' % term)
   if uri: 
      return uri[len('http://en.wikipedia.org/wiki/'):]
   else: return term

def wikipedia(term, last=False): 
   bytes = web.get(wikiuri % urllib.quote(term))
   bytes = r_tr.sub('', bytes)

   if not last: 
      r = r_redirect.search(bytes[:4096])
      if r: 
         term = urllib.unquote(r.group(1))
         return wikipedia(term, last=True)

   paragraphs = r_paragraph.findall(bytes)

   if not paragraphs: 
      if not last: 
         term = search(term)
         return wikipedia(term, last=True)
      return None

   # Pre-process
   paragraphs = [para for para in paragraphs 
                 if (para and 'technical limitations' not in para 
                          and 'window.showTocToggle' not in para 
                          and 'Deletion_policy' not in para 
                          and 'Template:AfD_footer' not in para 
                          and not (para.startswith('<p><i>') and 
                                   para.endswith('</i></p>'))
                          and not 'disambiguation)"' in para) 
                          and not '(images and media)' in para
                          and not 'This article contains a' in para]

   for i, para in enumerate(paragraphs): 
      paragraphs[i] = text(para).strip()

   # Post-process
   paragraphs = [para for para in paragraphs if 
                 (para and not (para.endswith(':') and len(para) < 150))]

   para = text(paragraphs[0])
   m = r_sentence.match(para)

   if not m: 
      if not last: 
         term = search(term)
         return wikipedia(term, last=True)
      return None
   sentence = m.group(0)

   maxlength = 275
   if len(sentence) > maxlength: 
      sentence = sentence[:maxlength]
      words = sentence[:-5].split(' ')
      words.pop()
      sentence = ' '.join(words) + ' [...]'

   if ((sentence == 'Wikipedia does not have an article with this exact name.')
    or (sentence == 'Wikipedia does not have a page with this exact name.')): 
      if not last: 
         term = search(term)
         return wikipedia(term, last=True)
      return None

   sentence = '"' + sentence.replace('"', "'") + '"'
   return sentence + ' - ' + (wikiuri % term)

def f_wikipedia(self, origin, match, args): 
   origterm = match.group(1)
   term = urllib.unquote(origterm)
   if not term: 
      self.msg(origin.sender, 'Maybe you meant ".wik Zen"?')
      return
   term = term[0].upper() + term[1:]
   term = term.replace(' ', '_')

   try: result = wikipedia(term)
   except IOError: 
      msg = "Can't connect to en.wikipedia.org (%s)" % (wikiuri % term)
      self.msg(origin.sender, msg)
      return

   if result is not None: 
      self.msg(origin.sender, result)
   else: 
      msg = 'Can\'t find anything in Wikipedia for "%s".' % origterm
      self.msg(origin.sender, msg)
f_wikipedia.rule = (['wik', 'wikipedia'], r"(.*)")
f_wikipedia.thread = True
