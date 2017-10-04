#!/usr/bin/python
import json
import urllib
import lxml.html
import re
import sys
import unicodedata
import time
import pyttsx
import logging

try:
  def showsearch(searchfor):
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    html_symbols = ["&#39;","&quot;","&amp","&nbsp"]
    subs = ["'","","&"," "]
    for h in hits:
      title_var = unicodedata.normalize('NFKD', re.sub('<[^<]+?>|&+;', '', h['title'])).encode('ascii','ignore')
      for entry in range(0,len(html_symbols)-1):
        title_var = title_var.replace(html_symbols[entry],subs[entry])
      print 'Title - '+title_var
      engine.say('Title - '+title_var)
      content_var = unicodedata.normalize('NFKD', re.sub('<[^<]+?>|&+;', '', h['content'])).encode('ascii','ignore')
      for entry in range(0,len(html_symbols)-1):
        content_var = content_var.replace(html_symbols[entry],subs[entry])
      print 'content - '+content_var
      engine.say('content - '+content_var)
      engine.runAndWait()
      time.sleep(1.5)
except:
  logging.error("Error in searching online.")
  engine.say("Error in searching online.")
  engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

query = sys.argv[1]
showsearch(query)