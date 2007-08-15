# Makefile for phenny
# Author: Sean B. Palmer, inamidst.com

all: phenny.tar.gz

clean: 
	# This may give lots of errors
	-archive -m phenny.tar.gz
	-mv -i phenny-*.tar.gz ../odds
	-rm phenny.tar.gz

phenny.tar.gz: clean
	# Create a new phenny.tar.gz archive
	cd .. && \
	   tar -cf phenny.tar `cat phenny/manifest` && \
	   gzip -9 phenny.tar && \
	   mv -i phenny.tar.gz phenny/

# [EOF]
