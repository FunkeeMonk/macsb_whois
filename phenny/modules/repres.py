#!/usr/bin/env python
"""
repres.py - Get Byte Representations
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

def f_representation(self, origin, match, args): 
   """.repres <str> - Return the representation of <str>."""
   self.msg(origin.sender, '%r' % match.group(1))
f_representation.rule = (['bytes', 'octets', 'repres', 'repr'], r'(.*)')
