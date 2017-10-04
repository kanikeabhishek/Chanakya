import time
import pyttsx
import os
import logging

try:
	def replace_special_chars(ip):
		invalid_list = [' ','(',')','[',']']
		for punct in invalid_list:
			ip.replace(punct,'\\'+punct)
		return ip

	def select_file(ip, search_type = "directory"):
		if search_type == "file":
			ans = os.popen("locate /home/*" + ip + "*")
		else:
			ans = os.popen("locate -b /home/*" + ip + "*" )
		locations = ans.read().split("\n")
		locations.remove("")
		if locations == []:
			engine.say("No such file or directory found. ")
			print "No such file or directory found. "
			engine.runAndWait()
			return None
		option = 0
		i = 1
		if len(locations) > 1:
			print "There are multiple files "
			engine.say("There are multiple files ")
			engine.runAndWait()
			for num in range(0,len(locations)):
				print i, ". ", locations[num]
				engine.say(str(i) + ") "+ locations[num])
				engine.runAndWait()
				i+=1		
			engine.say("select the file on which you want to read - ")
			engine.runAndWait()
			option = int(raw_input("select the file on which you want to read - "))
			if option <= len(locations):
				print "Selected file ", locations[option-1]
				engine.say("Selected file "+ locations[option-1])
				engine.runAndWait()
			else:
				print "Selecting first by default"
				engine.say("Selecting first by default. ")
				engine.runAndWait()
		return_opt = locations[option-1]
		return return_opt
except:
	logging.error("Error in file selection.")
  	engine.say("Error in file selection.")
  	engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

try:
	engine.say("Tell me the name of the file")
	engine.runAndWait()
	ip = raw_input("Tell me the name of the file - ")
	ip = replace_special_chars(ip)
	if os.path.isdir(ip) == True:
		source = select_file(ip)
	else:
		source = select_file(ip,"file")

	if source == None:
		exit()

	print "Contents of file are "
	engine.say("Contents of file are ")
	engine.runAndWait()
	time.sleep(2)

	f = open(source,'r')
	content = f.read()
	print content
	engine.say(content)
	engine.runAndWait()
except:
	logging.error("Error in reading file contents.")
	engine.say("Error in reading file contents.")
	engine.runAndWait()