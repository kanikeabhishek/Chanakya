import sqlite3
import pyttsx
import logging
import random
import unicodedata
import sys
import subprocess
import os

def replace_special_chars(ip):
	invalid_list = [' ','(',')','[',']']
	for punct in invalid_list:
		ip.replace(punct,'\\'+punct)
	return ip

def music_locate(song):
	global global_songs
	global likes
	path = []
	flag_file_found = False
	
	song = replace_special_chars(song)

	if not (os.system("echo " + song + " | grep http")):
		return song

	proc = subprocess.Popen(["locate /home/*"+song+"*"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	multiple_files = out.split("\n")
	multiple_files.remove("")

	for indv_path in multiple_files:
	   if indv_path != '':
	   	indv_path = replace_special_chars(indv_path)
		if not os.system(" file "+ indv_path + " | grep mp3"): # Tags only audio files
			flag_file_found = True
			path.append(indv_path) # If multiple audio files exists under same name prompt the user to select from them
		else:
			continue
	if flag_file_found == True: 
		global_songs.append(song)
		likes.remove(song)

global_songs = []

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

conn = sqlite3.connect('jarvis.db')
c = conn.cursor()

user_id = sys.argv[1]

yes_options = ["yea","yes","yeah","yup","ya","ok","probably","sure","certainly","of course","absolutely","indubitably","undoubtedly","doubtless","in fact","affirmative", "all right", "amen", "aye", "beyond a doubt", "by all means", "certainly", "definitely", "even so", "exactly", "fine", "gladly", "good", "good enough", "granted","indubitably","just so", "most assuredly", "naturally", "of course", "okay", "positively", "precisely", "sure thing", "surely", "true", "undoubtedly", "unquestionably", "very well", "willingly", "without fail", "yea", "yep"]

assurance = ["You sound a little off today.","Why is that you are sad today?","You are not in a good mood."]
integer = random.randint(1,3)
integer = integer - 1

print assurance[integer]
engine.say(assurance[integer])
engine.runAndWait()

engine.say("I have compiled some stuff for you.Do you want me to take you through?")
engine.runAndWait()
opt = raw_input("I have compiled some stuff for you.Do you want me to take you through? - ")

likes = []

for i in yes_options:
	if i in opt.lower():
		for row in c.execute("select like from likes where unique_user_id = ?",(user_id)):
			name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
			likes.append(name)

		for name in likes:
			music_locate(name)

		music_choice = random.randint(1,len(global_songs))
		music_choice = music_choice -1
		search_choice = random.randint(1,len(likes))
		search_choice = search_choice - 1

		song = global_songs[music_choice]
		search_query = likes[search_choice]

		engine.say("Do you want me to play a song which you like? ")
		engine.runAndWait()
		option = raw_input("Do you want me to play a song which you like? - ")
		for i in yes_options:
			if i in option.lower():
				os.system("python emotional_music.py " + song)
		engine.say("Do you want me to search online about some stuff which you like? ")
		engine.runAndWait()
		option = raw_input("Do you want me to search online about some stuff which you like? - ")
		for i in yes_options:
			if i in option.lower():
				os.system("python emotional_search.py " + search_query)