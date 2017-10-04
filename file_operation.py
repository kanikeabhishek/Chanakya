import os
import pyttsx
import shutil

two_file = ['move', 'copy']
one_file = ['rename', 'delete']

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
			ans = os.popen("locate -b /home/*" + ip + "*")
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
			engine.say("select the file on which you want to perform " + file_op + " operation - ")
			engine.runAndWait()
			option = int(raw_input("select the file on which you want to perform " + file_op + " operation - "))
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
	logging.error("File selection error.")
  	engine.say("File selection error.")
  	engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

try:
	engine.say("Tell me a file operation, copy, move, rename or delete")
	engine.runAndWait()
	file_op = raw_input("Tell me a file operation, copy, move, rename or delete - ")
	if file_op == "copy" or file_op == "move" or file_op == "delete" or file_op == "rename":
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

		if file_op in two_file:
			engine.say("Tell me the name of the folder where you want to " + file_op + " the file ")
			engine.runAndWait()
			ip = raw_input("Tell me the name of the folder where you want to " + file_op + " the file - ")
			destination = select_file(ip)

			if destination == None:
				exit()

			if str(file_op) == "move":
				os.system("cp " + source + " " + destination)
				os.system("rm " + source)
			elif str(file_op) == "copy":
				os.system("cp " + source + " " + destination)
		else:
			if str(file_op) == "rename":
				engine.say( "Tell me the new name of the file")
				engine.runAndWait()
				new_file_name = raw_input("Tell me the new name of the file - ")
				new_file_path = str(source[0:len(source)-len(ip)] + new_file_name)
				os.system("mv " + source + " " + new_file_path)
			elif str(file_op) == "delete":
				os.system("rm " + source)
		print "Operation successful"
		engine.say("Operation successful")
		engine.runAndWait()

	else:
		print "Incorrect operation given"
		engine.say("Incorrect operation given")
		engine.runAndWait()
		exit()
except:
	logging.error("Operational error.")
  	engine.say("Operational error.")
  	engine.runAndWait()