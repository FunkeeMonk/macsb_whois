#!/usr/bin/env python
"""
monty.py - Converse with Monty
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

def f_tauntmonty(self, origin, match, args): 
   text = args[0]
   if (origin.nick == 'Monty') and (origin.sender == '#swhack'): 
      reply = None
      if text.startswith('Thank goodness'): 
         reply = "Be quiet, Monty."
      elif text.endswith('price of fish?'): 
         reply = "Hush there, Monty."
      elif text.endswith('how ya doing?'): 
         reply = "Monty: shh, don't let anyone know you're around!"
      if reply: self.msg(origin.sender, reply)
f_tauntmonty.rule = r'.*(?:Thank goodness|price of fish|how ya doing).*'
