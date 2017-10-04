import sys
import pygst
pygst.require('0.10')
import gst

import time
import subprocess
import os
import pyttsx
import logging

try:

	def replace_special_chars(ip):
		invalid_list = [' ','(',')','[',']']
		for punct in invalid_list:
			ip.replace(punct,'\\'+punct)
		return ip

	flag_file_found = None
	class Player(object):

	    def __init__(self):
		pass

	    def __init__(self, channel):
	        self.pipeline = gst.Pipeline("RadioPipe")
	        self.player = gst.element_factory_make("playbin2", "player")
	        pulse = gst.element_factory_make("pulsesink", "pulse")
	        fakesink = gst.element_factory_make("fakesink", "fakesink")

	        self.player.set_property('uri', channel)
	        self.player.set_property("audio-sink", pulse)
	        self.player.set_property("video-sink", fakesink)
	        self.pipeline.add(self.player)

	    def play(self):
	        self.pipeline.set_state(gst.STATE_NULL)
	        self.pipeline.set_state(gst.STATE_PLAYING)

	    def stop(self):
	        self.pipeline.set_state(gst.STATE_PAUSED)

	def file_source(song):
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
		if not flag_file_found: 
			print "Song not found."
			engine.say("Song not found.")
			engine.runAndWait()
			return path

		else:
			if len(path) > 1:
				path = select_file(path)
			return 'file://' + str(path)


	def select_file(path, search_type = "directory"):
		print "There are multiple files - "
		print "Found in"
		engine.say("There are multiple files, found in")
		engine.runAndWait()
		for i, filepath in zip(xrange(len(path)), path):
			print i+1, ") ", filepath
			engine.say(str(i+1) + ") " + filepath)
			engine.runAndWait()
		engine.say("select the appropriate file ")
		engine.runAndWait()
		option = int(raw_input("select the appropriate file - "))
		if option < len(path):
			print "selected file ", path[option]
		return_opt = path[option-1]
		return return_opt[0:len(return_opt)]


	def action():
		path = file_source(sys.argv[1])
		player = Player(path)

		while 1:
		  engine.say("Give me a command, play, stop, new, exit ")
		  engine.runAndWait()
		  command = raw_input("Give me a command, play, stop, new, exit - ")
		  if command == "play":
		    player.play()
		  if command == "stop":
		    player.stop()
		  if command == "new":
		    player.stop()
		    action()
		    player = Player(path)
		  if command == "exit":
		    break
except:
	logging.error("Music player error.")
  	engine.say("Music player error.")
  	engine.runAndWait()

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-40)

if __name__ == '__main__':
	action()