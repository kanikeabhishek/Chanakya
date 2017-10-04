#!/usr/bin/python
from xml.etree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
import getpass
import sqlite3
import unicodedata
import re
import pyttsx
import logging

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

class CalendarExample:
  event_titles = []
  try:
    def __init__(self, email, password):
      self.cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
      self.cal_client.ClientLogin(email, password, self.cal_client.source);
  except:
    logging.error("Error in init !")
    engine.say("Error in init ")
    engine.runAndWait()
  
  try:
    def _PrintOwnCalendars(self):
      feed = self.cal_client.GetOwnCalendarsFeed()
  except:
    logging.error("Error in print calendars !")
    engine.say("Error in printing calendar ")
    engine.runAndWait()

  try:
    def _PrintAllEventsOnDefaultCalendar(self):
      feed = self.cal_client.GetCalendarEventFeed()
      print 'Events on Primary Calendar: %s' % (feed.title.text,)
      engine.say("Events on Primary Calendar "+ feed.title.text)
      engine.runAndWait()
      for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
	self.event_titles.append(an_event.title.text)
	print '\t%s' % (an_event.title.text)

    def _FullTextQuery(self, text_query='Cricket'):
      print 'Full text query for events on Primary Calendar: \'%s\'' % (
	  text_query,)
      engine.say('Full text query for events on Primary Calendar ' + text_query)
      engine.runAndWait()
      query = gdata.calendar.client.CalendarEventQuery(text_query=text_query)
      feed = self.cal_client.GetCalendarEventFeed(q=query)
      for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
	print '\t\t %s' % (an_event.content.text,)
	engine.say(str(an_event.content.text))
	engine.runAndWait()
	for a_when in an_event.when:
	  print '\t\tStart time: %s' % (a_when.start,)
	  print '\t\tEnd time:   %s' % (a_when.end,)
	  engine.say("Start time "+ a_when.start)
	  engine.say("End time "+ a_when.end)
	  engine.runAndWait()
  except:
    logging.error("Error in event display !")
    engine.say("Error in event display.")
    engine.runAndWait()

  try:
    def _InsertEvent(self, title='Tennis with Beth',content='Meet for a quick lesson', where='On the courts',start_time=None,end_time=None, recurrence_data=None):
      event = gdata.calendar.data.CalendarEventEntry()
      event.title = atom.data.Title(text=title)
      event.content = atom.data.Content(text=content)
      event.where.append(gdata.data.Where(value=where))

      if recurrence_data is not None:
	# Set a recurring event
	event.recurrence = gdata.data.Recurrence(text=recurrence_data)
      else:
	if start_time is None:
	  # Use current time for the start_time and have the event last 1 hour
	  start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
	  end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + 3600))
	  event.when.append(gdata.data.When(start=start_time, end=end_time))

      new_event = self.cal_client.InsertEvent(event)

      return new_event

    def _InsertSingleEvent(self, title='One-time Tennis with Beth',content='Meet for a quick lesson', where='On the courts',start_time=None, end_time=None):
      engine.say("Enter the event/reminder title")
      engine.runAndWait()
      title = raw_input("Enter the event/reminder title - ")
      
      engine.say("Enter the content of the event/remainder")
      engine.runAndWait()
      content = raw_input("Enter the content of the event/remainder - ")
      
      engine.say("Enter the start time of the event (yyyy-mm-dd)")
      engine.runAndWait()
      start_time = raw_input("Enter the start time of the event (yyyy-mm-dd) - ")
      
      engine.say("Enter the end time of the event (yyyy-mm-dd)")
      engine.runAndWait()
      end_time = raw_input("Enter the end time of the event (yyyy-mm-dd) - ")
    
      new_event = self._InsertEvent(title, content, where, start_time, end_time,
	  recurrence_data=None)

      print 'New single event inserted: %s' % (new_event.id.text,)
      return new_event  
  except:
    logging.error("Error in inserting !")
    engine.say("Error in inserting. ")
    engine.runAndWait()
    
  try:
    def _DeleteEvent(self, event):
      self.cal_client.Delete(event.GetEditLink().href)

    def Run(self, delete='false'):
      while 1:
        engine.say("Tell me an action, view calendar contents, insert reminder, delete reminder or terminate calendar")
        engine.runAndWait()
        choice = raw_input("Tell me an action, view calendar contents, insert reminder, delete reminder or terminate calendar - ")

        view_gen1 = re.match(r'(.*)view(.*)',choice)
        view_gen2 = re.match(r'(.*)look(.*)',choice)
        insert_gen1 = re.match(r'(.*)add(.*)',choice)
        insert_gen2 = re.match(r'(.*)insert(.*)',choice)
        delete_gen1 = re.match(r'(.*)remove(.*)',choice)
        delete_gen2 = re.match(r'(.*)delete(.*)',choice)
        terminate_gen1 = re.match(r'(.*)end(.*)',choice)
        terminate_gen2 = re.match(r'(.*)terminate(.*)',choice)

        if view_gen1 or view_gen2:
          # Lists the calendar
          self._PrintOwnCalendars()
          # Lists All the events of the calendar
          self._PrintAllEventsOnDefaultCalendar()
          # Lists the details of each event in the calendar
          for text_query in self.event_titles:
	    self._FullTextQuery(text_query)

        elif insert_gen1 or insert_gen2:
          # Inserting and updating events
          see = self._InsertSingleEvent()
	  # By default i have added event as the reminder
	  

        elif delete_gen1 or delete_gen2:
          # Deletion of the event
          feed = self.cal_client.GetCalendarEventFeed()
          title = ""
          title = raw_input("Enter the title which is to be deleted - ")
          for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
	    if an_event.title.text.lower() == title:
	      self.cal_client.Delete(an_event)
        
        elif terminate_gen1 or terminate_gen2:
          break
  except:
    logging.error("Error in deletion !")
    engine.say("Error in deletion.")
    engine.runAndWait()

def main():
  delete = 'false'

  conn = sqlite3.connect('jarvis.db')
  c = conn.cursor()

  user_id = sys.argv[1]

  for row in c.execute("select gmail from users where user_id = ?",(user_id)):
    usr = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  for row in c.execute("select password from users where user_id = ?",(user_id)):
    pw = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')

  sample = CalendarExample(usr, pw)
  sample.Run(delete)

if __name__ == '__main__':
  main()