import urllib2
print urllib2.urlopen('http://ipecho.net/plain').read() # one liner

# If you like visibility
# page = urllib2.urlopen('http://ipecho.net/plain')
# content = page.read()
# print content
