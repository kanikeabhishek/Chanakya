import urllib
import feedparser
import pyttsx
import unicodedata
import time

try:
	def feedread(link):
		feed = feedparser.parse(link)
		i = 1
		for item in feed["items"]:
			print item["title"]
			engine.say(item["title"])
			engine.runAndWait()
			time.sleep(1)
			i+=1
			if i == 8:
				break
except:
	logging.error("Feed parse error.")
  	engine.say("Feed parse error.")
  	engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

try:
	engine.say("Tell me the category, Top Stories, Most Recent Stories, Indian news, World news, Local News or Sports news")
	engine.runAndWait()
	choice = raw_input('1.Top Stories\t2.Most Recent Stories\t3.Indian news\n4.World news\t5.Local News\t6.Sports news - ')
	url = ''

	if choice.lower() == "top Stories":
		url = 'http://feeds.feedburner.com/NdtvNews-TopStories'
	elif choice.lower() == "most recent stories" or choice.lower() == "most recent" or choice.lower() == "recent" :
		url = 'http://timesofindia.feedsportal.com/c/33039/f/533965/index.rss'
	elif choice.lower() == "indian news" or choice.lower() == "indian" :
		url = 'http://timesofindia.feedsportal.com/c/33039/f/533916/index.rss'
	elif choice.lower() == "world news" or choice.lower() == "world":
		url = 'http://timesofindia.feedsportal.com/c/33039/f/533917/index.rss'
	elif choice.lower() == "local news" or choice.lower() == "local":
		url = 'http://feeds.feedburner.com/News-Karnataka'
	elif choice.lower() == "sports news" or choice.lower() == "sports":
		url = 'http://timesofindia.feedsportal.com/c/33039/f/533921/index.rss'
	else:
		print "Incorrect option, choosing Top stories as default. "
		engine.say("Incorrect option, choosing Top stories as default. ")
		engine.runAndWait()

	feedread(url)
except:
	logging.error("Feed parse error.")
  	engine.say("Feed parse error.")
  	engine.runAndWait()