import pywapi
import string
import sys
import sqlite3
import pyttsx
import unicodedata
import logging
 
try:
  engine = pyttsx.init()
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate-40)

  engine.say("Do you want me to fetch weather updates for your default location")
  engine.runAndWait()
  response = raw_input("Do you want me to fetch weather updates for your default location - ")
  
  yes_options = ["yes","yeah","yup","ya","ok","probably","sure","certainly","of course","absolutely","indubitably","undoubtedly","doubtless","in fact","affirmative", "all right", "amen", "aye", "beyond a doubt", "by all means", "certainly", "definitely", "even so", "exactly", "fine", "gladly", "good", "good enough", "granted","indubitably","just so", "most assuredly", "naturally", "of course", "okay", "positively", "precisely", "sure thing", "surely", "true", "undoubtedly", "unquestionably", "very well", "willingly", "without fail", "yea", "yep"]

  if response.lower() in yes_options:
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    
    user_id = sys.argv[1]

    for row in c.execute("select location from users where user_id = ?",(user_id)):
      city = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')

  else:
    engine.say("Enter city name")
    engine.runAndWait()
    city = raw_input("Enter city name: ")
    
  #this will give you a dictionary of all cities in the world with this city's name Be specific (city, country)!
  lookup = pywapi.get_location_ids(city)
  if lookup == {}:
    print "No city found"
  else:
    count = 1
    #workaround to access last item of dictionary
    for i in lookup.keys():
      if count == 1:
	location_id = i
	count = 2
    
    #location_id now contains the city's code
    weather_com_result = pywapi.get_weather_from_weather_com(location_id)

    print "It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "C now in " + lookup[location_id]
    engine.say("It is ") 
    engine.say(string.lower(weather_com_result['current_conditions']['text']))  
    engine.say(" and ")
    engine.say(weather_com_result['current_conditions']['temperature'])
    engine.say("C now in " )
    engine.say(lookup[location_id])
    engine.runAndWait()
    
except:
  logging.error("Weather fetch error.")
  engine.say("Weather fetch error.")
  engine.runAndWait()