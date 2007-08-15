#!/usr/bin/env python
# Mainly copied from jargon.py

import re, urllib
import web

inline = '(%s)' % '|'.join([
   'a', 'abbr', 'acronym', 'b', 'basefont', 'bdo', 'big', 'br', 'cite', 
   'code', 'dfn', 'em', 'font', 'i', 'img', 'input', 'kbd', 'label', 'q', 's', 
   'samp', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 
   'textarea', 'tt', 'u', 'var'
])

objs = '(%s)' % '|'.join([
   'script', 'style'
])

r_inline = re.compile(r'(?i)</?%s\b[^>]*>' % inline)
r_objects = re.compile(r'(?ims)<%s\b[^>]*>.*?</%s\b[^>]*>' % (objs, objs))
r_tag = re.compile(r'<[^>]+>')
r_text = re.compile(r'[^|]{50,}')
r_ws = re.compile(r'[ \t\r\n]+')
r_pipes = re.compile(r' (?:\| )+')

r_entity = re.compile(r'(&[A-Za-z0-9#]+;)')

def entityToUTF8(m): 
   from htmlentitydefs import name2codepoint
   entity = m.group(1)
   if entity.startswith('&#x'): 
      cp = int(entity[3:-1], 16)
      return unichr(cp).encode('utf-8')
   elif entity.startswith('&#'): 
      cp = int(entity[2:-1])
      return unichr(cp).encode('utf-8')
   else: 
      char = name2codepoint[entity[1:-1]]
      return unichr(char).encode('utf-8')

def extract(uri): 
   bytes = web.get(uri)
   bytes = r_inline.sub('', bytes)
   bytes = r_objects.sub(' | ', bytes)
   bytes = r_tag.sub(' | ', bytes)
   bytes = r_ws.sub(' ', bytes)
   for nugget in r_text.findall(bytes): 
      nugget = nugget.strip(' ')
      nugget = r_entity.sub(entityToUTF8, nugget)

      if len(nugget) > 200: 
         return '"' + nugget[:200] + '[...]"'
      else: return '"' + nugget + '"'
   return '"' + r_pipes.sub(' \xC2\xB7 ', bytes[:100].strip(' |')) + '"'

def f_extract(self, origin, match, args): 
   uri = match.group(1)
   if not ':' in uri: 
      uri = 'http://' + uri

   try: result = extract(uri)
   except IOError: 
      msg = "Can't connect to server (%s)" % (uri)
      self.msg(origin.sender, msg)
      return

   if result is not None: 
      self.msg(origin.sender, origin.nick + ': ' + result)
   else: 
      msg = "Can't get a snippet for that URI."
      self.msg(origin.sender, origin.nick + ': ' + msg)
f_extract.rule = (['web'], r"(.*)")
f_extract.thread = True

def main(): 
   import sys
   term = urllib.unquote(sys.argv[1])
   print extract(term)

if __name__=="__main__": 
   main()
