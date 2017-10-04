import urllib
import feedparser
import pyttsx
import unicodedata
import time
import logging

try:
	def feedread(link):
		feed = feedparser.parse(link)
		i = 1
		for item in feed["items"]:
			print item["title"]
			engine.say(item["title"])
			summary = item["summary"].split("<")
			print summary[0]
			engine.say(summary[0])
			engine.runAndWait()
			time.sleep(1)
			i+=1
			if i == 6:
				break
except:
	logging.error("Data fetch error.")
  	engine.say("Data fetch error.")
  	engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

print "Top stories."
engine.say("Top stories. ")
engine.runAndWait()
feedread('http://feeds.feedburner.com/NdtvNews-TopStories')

print "Most recent stories."
engine.say("Most recent stories. ")
engine.runAndWait()
feedread('http://timesofindia.feedsportal.com/c/33039/f/533965/index.rss')

print "Indian news. "
engine.say("Indian news. ")
engine.runAndWait()
feedread('http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss')

print "World news."
engine.say("World news. ")
engine.runAndWait()
feedread('http://timesofindia.feedsportal.com/c/33039/f/533917/index.rss')

print "Local news."
engine.say("Local news. ")
engine.runAndWait()
feedread('http://feeds.feedburner.com/News-Karnataka')

print "Sports news."
engine.say("Sports news. ")
engine.runAndWait()
feedread('http://timesofindia.feedsportal.com/c/33039/f/533921/index.rss')