#!/usr/bin/env python
# Mainly copied from wikipedia.py

import re, urllib
import web

jargonuri = 'http://www.catb.org/jargon/html/%s/%s.html'

r_tr = re.compile(r'(?ims)<tr[^>]*>.*?</tr>')
r_link = re.compile(r'href=[\'"]?([^\'"]+)')
r_paragraph = re.compile(r'(?ims)<p[^>]*>.*?</p>|<li(?!n)[^>]*>.*?</li>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')

abbrs = ['etc', 'cf', 'Co', 'Ltd', 'Inc', 'Mt', 'Mr', 'Mrs', 
         'Dr', 'Ms', 'Rev', 'Fr', 'St'] \
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

def jargon(term): 
   bytes = web.get(jargonuri % (term[0].upper(), urllib.quote(term)))
   bytes = r_tr.sub('', bytes)

   paragraphs = r_paragraph.findall(bytes)
   if not paragraphs: 
      return None

   # Pre-process
   paragraphs = [para for para in paragraphs 
                 if (para and 'technical limitations' not in para 
                          and 'window.showTocToggle' not in para
                          and not (para.startswith('<p><i>') and 
                                   para.endswith('</i></p>'))
                          and not 'disambiguation)"' in para)]

   for i, para in enumerate(paragraphs): 
      paragraphs[i] = text(para).strip()

   # Post-process
   paragraphs = [para for para in paragraphs if 
                 (para and not (para.endswith(':') and len(para) < 150))]

   para = text(paragraphs[0])
   m = r_sentence.match(para)

   if not m: 
      return None
   sentence = m.group(0)

   maxlength = 275
   if len(sentence) > maxlength: 
      sentence = sentence[:maxlength]
      words = sentence[:-5].split(' ')
      words.pop()
      sentence = ' '.join(words) + ' [...]'

   sentence = '"' + sentence.replace('"', "'") + '"'
   return sentence + ' - ' + (jargonuri % (term[0].upper(), term))

def f_jargon(self, origin, match, args): 
   term = match.group(1)
   try: result = jargon(term)
   except IOError: 
      args = (term[0].upper(), term)
      msg = "Can't connect to www.catb.org (%s)" % (jargonuri % args)
      self.msg(origin.sender, msg)
      return

   if result is not None: 
      self.msg(origin.sender, result)
   else: 
      msg = 'Can\'t find anything in the Jargon File for "%s".' % term
      self.msg(origin.sender, msg)
f_jargon.rule = (['jargon'], r"(.*)")
f_jargon.thread = True

def main(): 
   import sys
   term = urllib.unquote(sys.argv[1])
   print jargon(term)

if __name__=="__main__": 
   main()
