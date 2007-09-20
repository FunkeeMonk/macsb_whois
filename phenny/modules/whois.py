#!/usr/bin/env python

import re, urllib, string
import web
from BeautifulSoup import BeautifulSoup
#import logging

#logger = logging.getLogger('macsb_whois')
#hdlr = logging.FileHandler('/Users/funkeemonk/Desktop/macsb_whois.log') # TODO: Don't hardcode this
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)

def remove_link_html(self, original):
	if original == None:
		return ''
		
	anchor = original.a
	if anchor == None:
		return original.next.strip()
	else:
		return anchor.string
	
def f_whois(self, origin, match, args): 
	""".whois [ <handle> ] - Reveals who the person is in Real Life using the table at http://macsb.ironcoder.org/wiki/WhoIsWho ."""
	
	sendto = None
	if origin.nick == origin.sender: #Private message
		sendto = origin.nick
	else:
		sendto = origin.sender
	
	handle = string.split(args[0], " ")[1]
	
	if handle == 'macsb_whois':
		self.msg(sendto, 'Hi, i\'m the #macsb whois robot! I grab my data from http://macsb.ironcoder.org/wiki/WhoIsWho , so if you\'re a Mac small business developer, be sure to add your information on that page.')
		self.msg(sendto, 'I\'m created by FunkeeMonk, so please send feedback regarding me to him. You can also find out more about my creator at http://www.funkeemonk.com/blog')
		return
		
	s = web.get('http://macsb.ironcoder.org/wiki/WhoIsWho')
#	s = open('/Users/funkeemonk/Desktop/IRC Bot/macsb.htm')

	# Uncomment this to enable logging
	#logger.info(origin.nick + ' requested information for ' + handle)
	
	soup = BeautifulSoup(s)

	tr = soup.findAll('tr')
	
	for i in tr:
		if len(i) > 1:
			name = remove_link_html(self, i.contents[1]) #Handle
				
			if name.strip('_').upper() == handle.strip('_').upper():
				msg = name + ' is '
				url = ''
				
 				msg = msg + remove_link_html(self, i.contents[2]) #Real name
				
				if len(i) > 2: #Website/Blog URL
					if i.contents[3]:
						anchor = i.contents[3].a
						try:
							url = anchor['href']
						except:
							url = ''
					
				if len(i) > 3: #Product Names
					product_names = []
					number_of_product_names = len(i.contents[4])
					product = i.contents[4].next
					num = 0
					while num != number_of_product_names:
						try:
							a = product.a
							number_of_product_names = number_of_product_names + 1
						except:
							product_names.append(product.strip())
						
						num = num + 1						
						product = product.next
																
				if len(product_names) > 0:
					msg = msg + ' ('
									
					for product in product_names:
						msg = msg + " " + product

					msg = msg + ')'
					
				if url:
					msg = msg + ' - ' + url
				
				self.msg(sendto, msg)

				return
#				print msg

	self.msg(sendto, 'Can\'t find information for \'' + handle + '\' at ' + 'http://macsb.ironcoder.org/wiki/WhoIsWho')

f_whois.rule = (['whois', 'who'], r'(\w+)')
f_whois.thread = True

def main(): 
	f_whois(0, 0, 0, ('.whois dchest', 'PRIVMSG', '#testphenny'))

if __name__=="__main__": 
   main()
