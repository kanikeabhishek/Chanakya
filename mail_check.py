import imaplib
import getpass
import sqlite3
import sys
import unicodedata
import string , re
import pyttsx,time
import logging

try:
  def count(user_id):
    folderStatus, UnseenInfo = imap.status('INBOX', "(UNSEEN)")
    NotReadCounter = int(UnseenInfo[0].split()[2].strip(').,]'))
    if NotReadCounter == 0:
      print "There are no unread mails "
      engine.say("There are no unread mails ")
      engine.runAndWait()
      exit()
    elif NotReadCounter == 1:
      print "Number of unread mail is -",NotReadCounter
      engine.say("Number of unread mail is ")
      engine.say(NotReadCounter)
      engine.runAndWait()
    else:
      print "Number of unread mails are -",NotReadCounter
      engine.say("Number of unread mails are ")
      engine.say(NotReadCounter)
      engine.runAndWait()

  def display(user_id):
    imap.select(readonly=1)
    retcode,messages = imap.search(None, 'UNSEEN')
    if retcode == 'OK':
      for message in messages[0].split(' '):
	(ret, mesginfo) = imap.fetch(message, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
	if ret == 'OK':
	  from_info = str(mesginfo[0]).split(',')
	  processed = from_info[1].replace("\\r\\n","")
	  proc = processed.replace(")","")
	  print proc
	  engine.say(proc)
	  engine.runAndWait()
	  time.sleep(1)

except:
  logging.error("Error in reading mails.")
  engine.say("Error in reading mails.")
  engine.runAndWait()

try:
  engine = pyttsx.init()
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate-40)

  conn = sqlite3.connect('jarvis.db')
  c = conn.cursor()

  user_id = sys.argv[1]

  for row in c.execute("select gmail from users where user_id = ?",(user_id)):
    usr = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  for row in c.execute("select password from users where user_id = ?",(user_id)):
    pwd = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')

  imap_host = 'imap.gmail.com'
  imap = imaplib.IMAP4_SSL(imap_host)
  imap.login(usr,pwd)

  count(user_id)
  display(user_id)

  imap.close()
  imap.logout()
except:
  logging.error("Error in data extraction and Gmail authentication.")
  engine.say("Error in data extraction and Gmail authentication.")
  engine.runAndWait()