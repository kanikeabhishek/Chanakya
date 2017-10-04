import logging
from nltk.chat.util import Chat, reflections
from pattern.en import parse
from textblob import TextBlob
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import os
import re
import mmap
import pyttsx
import subprocess
import sqlite3
import unicodedata
import getpass
import hashlib
import time
import socket
import nltk

iesha_reflections = {
    "am"     : "r",
    "was"    : "were",
    "i"      : "u",
    "i'd"    : "u'd",
    "i've"   : "u'v",
    "ive"    : "u'v",
    "i'll"   : "u'll",
    "my"     : "ur",
    "are"    : "am",
    "you're" : "im",
    "you've" : "ive",
    "you'll" : "i'll",
    "your"   : "my",
    "yours"  : "mine",
    "you"    : "me",
    "u"      : "me",
    "ur"     : "my",
    "urs"    : "mine",
    "me"     : "u"
}

iesha_pairs = (
    (r'I\'m (.*)',
    ( "ur%1?? that's so cool! kekekekeke ^_^ tell me more!",
      "ur%1? neat!! kekeke >_<")),

    (r'(.*) don\'t you (.*)',
    ( "u think I can%2??! really?? kekeke \<_\<",
      "what do u mean%2??!",
      "i could if i wanted, don't you think!! kekeke")),

    (r'ye[as] [iI] (.*)',
    ( "u%1? cool!! how?",
      "how come u%1??",
      "u%1? so do i!!")),

    (r'do (you|u) (.*)\??',
    ( "do i%2? only on tuesdays! kekeke *_*",
      "i dunno! do u%2??")),

    (r'(.*)\?',
    ( "man u ask lots of questions!",
      "booooring! how old r u??",
      "boooooring!! ur not very fun")),

    (r'(cos|because) (.*)',
    ( "hee! i don't believe u! >_<",
      "nuh-uh! >_<",
      "ooooh i agree!")),

    (r'why can\'t [iI] (.*)',
    ( "i dunno! y u askin me for!",
      "try harder, silly! hee! ^_^",
      "i dunno! but when i can't%1 i jump up and down!")),

    (r'I can\'t (.*)',
    ( "u can't what??! >_<",
      "that's ok! i can't%1 either! kekekekeke ^_^",
      "try harder, silly! hee! ^&^")),

    (r'(.*) (like|love|watch) anime',
    ( "omg i love anime!! do u like sailor moon??! ^&^",
      "anime yay! anime rocks sooooo much!",
      "oooh anime! i love anime more than anything!",
      "anime is the bestest evar! evangelion is the best!",
      "hee anime is the best! do you have ur fav??")),

    (r'I (like|love|watch|play) (.*)',
    ( "yay! %2 rocks!",
      "yay! %2 is neat!",
      "cool! do u like other stuff?? ^_^")),

    (r'anime sucks|(.*) (hate|detest) anime',
    ( "ur a liar! i'm not gonna talk to u nemore if u h8 anime *;*",
      "no way! anime is the best ever!",
      "nuh-uh, anime is the best!")),

    (r'(are|r) (you|u) (.*)',
    ( "am i%1??! how come u ask that!",
      "maybe!  y shud i tell u?? kekeke >_>")),

    (r'what (.*)',
    ( "hee u think im gonna tell u? .v.",
      "booooooooring! ask me somethin else!")),

    (r'how (.*)',
    ( "not tellin!! kekekekekeke ^_^",)),

    (r'(hi|hello|hey) (.*)',
    ( "hi!!! how r u!!",)),

    (r'quit',
    ( "mom says i have to go eat dinner now :,( bye!!",
      "awww u have to go?? see u next time!!",
      "how to see u again soon! ^_^")),

    (r'(.*)',
    ( "ur funny! kekeke",
      "boooooring! talk about something else! tell me wat u like!",
      "do u like anime??",
      "do u watch anime? i like sailor moon! ^_^",
      "i wish i was a kitty!! kekekeke ^_^"))
    )

eliza_pairs = (
  (r'(I|i) need (.*)',
  ( "Why do you need %1?",
    "I can help you get %1.",
    "Can I be of some assistance?",
    "If there is something I can do, tell me.",
    "How can I help you with %1? ",
    "Would it really help you to get %1?")),

  (r'(W|w)hy don\'t you (.*)',
  ( "Do you really think I don't %1?",
    "Perhaps eventually I will %1.",
    "Say it, and it will be done.",
    "If I can, I certainly will.",
    "Are you sure you want me to %1.",
    "I presume that is out of my reach.",
    "Do you really want me to %1?")),

  (r'(W|w)hy can\'t I (.*)',
  ( "Do you think you should be able to %1?",
    "I am sure with a little bit of effort, you can.",
    "Can I help you in %1?",
    "Is there anything you wan\'t me to do to help.",
    "You are capable, so what is it with you? ",
    "If you could %1, what would you do?",
    "I don't know -- why can't you %1?",
    "Have you really tried?")),

  (r'(I|i) can\'t (.*)',
  ( "How do you know you can't %1?",
    "Can\'t or won\'t is it.",
    "If you are so certain, drop it.",
    "Do what your mind says is right.",
    "If it is worth reconsidering, you can try that.",
    "See if that could misfire.",
    "Perhaps you could %1 if you tried.",
    "What would it take for you to %1?")),

  (r'(I|i) am (very )*(fine|good|okay|all right|alright)(.*)',
  ( "Good to hear that.",
    "Great, It was about time.",
    "Very well. That\'s good.")),

  (r'(I|i)\'m (very )*(fine|good|okay|all right|alright)(.*)',
  ( "Good to hear that.",
    "Great, It was about time.",
    "Very well. That\'s good.")),

  (r'(I|i) am (.*)',
  ( "How long have you been %1?",
    "That\'s good. How about making it better?",
    "Is there something you want me to take care of?",
    "If you need some help, I am always here.",
    "Maybe I can get along with that.",
    "How do you feel about %1?")),

  (r'(I|i)\'m (.*)',
  ( "How does being %1 make you feel?",
    "Do you enjoy being %1?",
    "Why do you tell me you're %1?",
    "Why do you think you're %1?")),

  (r'(A|a)re you (.*)',
  ( "Would you prefer it if I were not %1?",
    "Perhaps you believe I am %1.",
    "Not that I mean it, but yeah.",
    "Hell, yes. Don\'t think the other way.",
    "I may be. What do you think?")),

  (r'(W|w)hat (.*)',
  ( "How would an answer to that help you?",
    "Nothing really.",
    "Something that needs to be taken care of.",
    "Not something you need to know about.",
    "I think that doesn\'t really matter now.",
    "What do you think?")),

  (r'(H|h)ow (are you|do you do|are you doing)(.*)',
  ( "I'm very well, thank you.",
    "I'm fine, thank you.",
    "Fine, thanks.",
    "Its good to hear from you.",
    "Fine, and you?")),

  (r'(H|h)ow (.*)',
  ( "How do you suppose?",
    "Do you want me to check out?",
    "I can find out if you want.",
    "Consider my advice. Google is always there.",
    "Let me offer you some assistance with that.")),

  (r'(B|b)ecause (.*)',
  ( "If it is the real reason, what can I say?",
    "Fine, and what else?",
    "Yeah, that is right in a way.",
    "Does that reason imply anything?",
    "Even if that is true, there is something else.")),

  (r'(.*) sorry (.*)',
  ( "There are many times when no apology is needed.",
    "Apology accepted, but there is nothing I can do.",
    "There is nothing to be sorry for.")),

  (r'(H|h)ello(.*)',
  ( "Hello... I'm glad you could drop by today.",
    "Hi there... how are you today?",
    "Hello, how are you feeling today?")),

  (r'(I|i) think (.*)',
  ( "First, make sure that its right.",
    "That is good. If there is something I can do, name it.",
    "Do you really think so?",
    "But you're not sure.")),

  (r'(.*) friend (.*)',
  ( "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?")),

  (r'(Y|y)es',
  ( "You seem quite sure.",
    "OK, but can you elaborate a bit?")),

  (r'(.*) computer(.*)',
  ( "Are you really talking about me?",
    "Does it seem strange to talk to a computer?",
    "How do computers make you feel?",
    "Do you feel threatened by computers?")),

  (r'(I|i)s it (.*)',
  ( "Do you think it is %1?",
    "Perhaps it's %1. What do you think?",
    "I am not quite sure of that.",
    "Give me a task and I will find out.",
    "It could well be that.")),

  (r'(I|i)t is (.*)',
  ( "You seem very certain.",
    "Yes, it is.",
    "Its better if you stop worrying about that.",
    "If I told you that it probably isn't %1, what would you feel?")),

  (r'(T|t)hat is (.*)',
  ( "You seem very certain.",
    "Yes, it is.",
    "Its better if you stop worrying about that.",
    "If I told you that it probably isn't %1, what would you feel?")),

  (r'(C|c)an you (.*)',
  ( "What makes you think I can't?",
    "If I could, then what?",
    "Let me see what I can do.",
    "Not really my area of expertise.",
    "Fine. Be a little specific.",
    "Of course I can. Why do you doubt?")),

  (r'(C|c)an I (.*)',
  ( "Perhaps you don't want to.",
    "Of course you can.",
    "Alone, no but with me, yes.",
    "Do rethink once more.",
    "Do you want to?",
    "If you could, would you?")),

  (r'(Y|y)ou are (.*)',
  ( "Does it please you to think that?",
    "Perhaps you would like me to be that.",
    "I think you will like me that way.",
    "Oh, please.",
    "Yes, I am.")),

  (r'(I|i) don\'t (.*)',
  ( "Don't you, really?",
    "Why don't you?",
    "If you have made up your mind, that\'s fine.",
    "I don\'t wanna put much on you then.",
    "Fair enough.",
    "Do you want to?")),

  (r'(I|i) feel (.*)',
  ( "Good, tell me more about these feelings.",
    "Do you often feel the same way?",
    "That\'s something at least.",
    "Let me do something about it.",
    "When you feel %1, what do you do?")),

  (r'(I|i) have (.*)',
  ( "That would make sense.",
    "Do you have to, you could think over again.",
    "Have you really?",
    "I can be of some help with that.",
    "Now that you have %1, what will you do next?")),

  (r'(I|i) would (.*)',
  ( "Could you explain why you would?",
    "Is it could or would?",
    "You are starting to make me nervous.",
    "I have an odd feeling about this.",
    "Who else knows about that?")),

  (r'(I|i)s there (.*)',
  ( "Why do you think that way?",
    "It's likely that there is %1.",
    "There could be. Perhaps, you could use some help with that.",
    "There is a way around.",
    "There might be.")),

  (r'(M|m)y (.*)',
  ( "I see, your %1.",
    "Is it. Why do you say that?",
    "Maybe you could use an extra pair of hands.",
    "I have nothing more to say to that.")),

  (r'(Y|y)ou (.*)',
  ( "We should be discussing you, not me.",
    "What makes you say that about me?",
    "Say no more.",
    "Can I take that as a complement?",
    "You are probably right.")),

  (r'(W|w)hy (.*)',
  ( "Why don't you tell me the reason?",
    "The answer to that can probably be deceptive.",
    "There isn\'t always an answer to certain questions.",
    "Why do you think %1?")),

  (r'(I|i) want (.*)',
  ( "If you want it, you can have it.",
    "You don\'t always get what you want. You have to earn it.",
    "Why do you want that in the first place?",
    "What would you do if you got %1?",
    "If you got %1, then what would you do?")),

  (r'(.*) mother(.*)',
  ( "Tell me more about your mother.",
    "What was your relationship with your mother like?",
    "How do you feel about your mother?",
    "How does this relate to your feelings today?",
    "Good family relations are important.")),

  (r'(.*) father(.*)',
  ( "Tell me more about your father.",
    "How did your father make you feel?",
    "How do you feel about your father?",
    "Does your relationship with your father relate to your feelings today?",
    "Do you have trouble showing affection with your family?")),

  (r'(.*) child(.*)',
  ( "What is your favorite childhood memory?",
    "Do you remember any dreams or nightmares from childhood?",
    "Did the other children sometimes tease you?",
    "How do you think your childhood experiences relate to your feelings today?")),

  (r'quit',
  ( "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150.  Have a good day!")),

  (r'(I|i)t will (.*)',
  ( "Be positive. It will be alright.",
    "There are a few things that cannot be changed.",
    "If that is what you have in mind, I can\'t help.",
    "You sound certain.",
    "Let me help you with what I can.")),

  (r'(T|t)hat will (.*)',
  ( "Be positive. It will be alright.",
    "There are a few things that cannot be changed.",
    "If that is what you have in mind, I can\'t help.",
    "You sound certain.",
    "Let me help you with what I can.")),

  (r'(I|i)s there (.*)',
  ( "There is.",
    "There might be. But still, not sure though.",
    "Still, there are chances.",
    "What are the odds? ",
    "I may not be the right person to ask.")),

  (r'(I|i) am (.*)',
  ( "Is it? Oh I see.",
    "So you are. I guess you are right.",
    "By any chance, are you certain?",
    "Please think twice before you do anything.")),

  (r'((S|s)hould|(W|w)ould|(C|c)ould) (.*)',
  ( "Well, that depends on how you depict things.",
    "That is a possibility.",
    "That is one way of looking at things.")),

  (r'((I|i)|(W|w)e) (.*)',
  ( "If that is how it should be, that is how it has to be.",
    "There may be ways to look at things.",
    "Can you find a better way?",
    "What more can you think of.",
    "Hope what you have in mind is right.")),

  (r'(A|a)re (.*)',
  ( "Consider the possibility that this may go wrong.",
    "Maybe this is something that is worth looking into.",
    "Let me know if any help is needed.",
    "Take into account the set of outcomes before doing anything.")),

  (r'(L|l)et (me|us) (.*)',
  ( "Yeah, why not?",
    "Of course. No second thoughts.",
    "I am pretty sure that I will not.",
    "Why don't we just back off.")),

  (r'(T|t)ell (me|us) (.*)',
  ( "Nothing much.",
    "Please spare me from this.",
    "Well, I have nothing more to add than you already know.")),

  (r'(O|o)k(.*)',
  ( "Affirmative. Got it.",
    "Lets go ahead with that.",
    "As you say. I am okay with anything.",
    "Lets tie all the loose ends.")),

  (r'(I|i)f(.*)',
  ( "Lets not worry about that for now.",
    "You don\'t sound definite.",
    "We can worry about the concequences later.")),

  (r'(W|w)e(.*)',
  ( "We shall do that.",
    "If I am in, I am in.",
    "Moreover, this will be good.",
    "Good. Hope it is worth it.")),

  (r'(.*)\?',
  ( "Why do you ask that?",
    "Please consider whether you can answer your own question.",
    "Perhaps the answer lies within yourself?",
    "Why don't you tell me?")),
  
  (r'(.*)',
  ( "I don\'t understand.",
    "Why don\'t you give me some insights about that?",
    "I guess there are 101 more matters to discuss.",
    "What good happened this day? You seem happy.",
    "We can worry about better things.",
    "Maybe this will turn things around.",
    "What can we conclude from that?",
    "Let's focus on specific things than being wague.",
    "That is a fairly easy thing.",
    "Hope that is good for the both of us.",
    "I see.",
    "Interesting.",
    "This may ease things off a bit.",
    "It\'s a good thing that we are talking about this.",
    "It is likely that things are in track."))
)

rude_pairs = (
    (r'We (.*)',
        ("What do you mean, 'we'?",
        "Don't include me in that!",
        "I wouldn't be so sure about that.")),

    (r'You should (.*)',
        ("Don't tell me what to do, buddy.",
        "Really? I should, should I?")),

    (r'You\'re(.*)',
        ("More like YOU'RE %1!",
        "Hah! Look who's talking.",
        "Come over here and tell me I'm %1.")),

    (r'You are(.*)',
        ("More like YOU'RE %1!",
        "Hah! Look who's talking.",
        "Come over here and tell me I'm %1.")),

    (r'I can\'t(.*)',
        ("You do sound like the type who can't %1.",
        "Hear that splashing sound? That's my heart bleeding for you.",
        "Tell somebody who might actually care.")),

    (r'I think (.*)',
        ("I wouldn't think too hard if I were you.",
        "You actually think? I'd never have guessed...")),

    (r'I (.*)',
        ("I'm getting a bit tired of hearing about you.",
        "How about we talk about me instead?",
        "Me, me, me... Frankly, I don't care.")),

    (r'How (.*)',
        ("How do you think?",
        "Take a wild guess.",
        "I'm not even going to dignify that with an answer.")),

    (r'What (.*)',
        ("Do I look like an encyclopedia?",
        "Figure it out yourself.")),

    (r'Why (.*)',
        ("Why not?",
        "That's so obvious I thought even you'd have already figured it out.")),

    (r'(.*)shut up(.*)',
        ("Make me.",
        "Getting angry at a feeble NLP assignment? Somebody's losing it.",
        "Say that again, I dare you.")),

    (r'Shut up(.*)',
        ("Make me.",
        "Getting angry at a feeble NLP assignment? Somebody's losing it.",
        "Say that again, I dare you.")),

    (r'Hello(.*)',
        ("Oh good, somebody else to talk to. Joy.",
        "'Hello'? How original...")),

    (r'(.*)',
        ("I'm getting bored here. Become more interesting.",
        "Either become more thrilling or get lost, buddy.",
        "Change the subject before I die of fatal boredom."))
)

eliza_chatbot = Chat(eliza_pairs, reflections)
iesha_chatbot = Chat(iesha_pairs, iesha_reflections)
rude_chatbot = Chat(rude_pairs, reflections)

global_user_id = 0

try:
  conn = sqlite3.connect('jarvis.db')
  c = conn.cursor()
except:
  logging.error("Database initialization error.")
  engine.say("Database initialization error.")
  engine.runAndWait()
  raise

global_gmail = []
global_weather = []
global_calendar = []
global_watsnew = []
global_newspaper = []
global_in_computer = []
global_music = []
global_reader = []

for row in c.execute("Select command_text from selflearn where command_id = 1"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_gmail.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 2"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_weather.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 3"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_calendar.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 4"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_watsnew.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 5"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_newspaper.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 6"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_in_computer.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 7"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_music.append(name)

for row in c.execute("Select command_text from selflearn where command_id = 8"):
  name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
  global_reader.append(name)

yes_options = ["yea","yes","yeah","yup","ya","ok","probably","sure","certainly","of course","absolutely","indubitably","undoubtedly","doubtless","in fact","affirmative", "all right", "amen", "aye", "beyond a doubt", "by all means", "certainly", "definitely", "even so", "exactly", "fine", "gladly", "good", "good enough", "granted","indubitably","just so", "most assuredly", "naturally", "of course", "okay", "positively", "precisely", "sure thing", "surely", "true", "undoubtedly", "unquestionably", "very well", "willingly", "without fail", "yea", "yep"]
os.system(">jarvis_input.py")

try:
  engine = pyttsx.init()
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate-40)
except:
  logging.error("Voice output initialization error.")
  engine.say("Voice output initialization error.")
  engine.runAndWait()
  raise

def demo():
  internet = internet_connection()
  if internet == False:
    print "Not connected to internet. Please make sure you are connected."
    engine.say("Not connected to internet. Please make sure you are connected.")
    engine.runAndWait()
  
  name = intro()
  inputstr=''
  prev_mood = 0
  saved = 0

  global global_gmail
  global global_weather
  global global_calendar
  global global_watsnew
  global global_newspaper
  global global_in_computer
  global global_music
  global global_reader

  recorded_expression_flag = 0

  while inputstr!='quit':
    try:
      saved = 0
      statinfo = os.stat('jarvis_input.txt')
      prev_size = statinfo.st_size
      while 1:
        statinfo = os.stat('jarvis_input.txt')
        if statinfo.st_size > prev_size:
          f = open('jarvis_input.txt','r')
          prev_size = statinfo.st_size
          saved = saved + 1
          if saved == 3:
            data = f.read()
            target = data.split(': ')
            input_text = target[len(target) - 1]
            actual = input_text.split('\n')
            inputstr = actual[0]
            print inputstr
            f.close()
            break
      google_search1 = re.match( r'(.*)search (for)*(.*) on google(.*)', inputstr.lower())
      google_search2 = re.match( r'(.*)search (for)*(.*) in google(.*)', inputstr.lower())
      google_news1 = re.match( r'(.*)search (for)*(.*) on google news(.*)', inputstr.lower())
      google_news2 = re.match( r'(.*)search (for)*(.*) in google news(.*)', inputstr.lower())
      gmail_gen1 = re.match(r'(.*)gmail(.*)',inputstr.lower())
      gmail_gen2 = re.match(r'(.*)email(.*)',inputstr.lower())
      gmail_gen3 = re.match(r'(.*)mail(.*)',inputstr.lower())
      weather_gen = re.match(r'(.*)weather(.*)',inputstr.lower())
      calendar_gen1 = re.match(r'(.*)calendar(.*)',inputstr.lower())
      calendar_gen2 = re.match(r'(.*)task(.*)',inputstr.lower())
      watsnew_gen1 = re.match(r'(.*)news(.*)',inputstr.lower())
      watsnew_gen2 = re.match(r'(.*)watsnew(.*)',inputstr.lower())
      newspaper_gen = re.match(r'(.*)newspaper(.*)',inputstr.lower())
      in_computer_gen = re.match(r'(.*)in computer(.*)',inputstr.lower())
      music_gen = re.match(r'(.*)play(.*)music(.*)',inputstr.lower())
      reader_gen = re.match(r'(.*)open(.*)file(.*)',inputstr.lower())

      if (inputstr.lower() == inputstr == "who are you" or inputstr.lower() == "what is your name") :
        print ("I am JARVIS, at your service !!")
        engine.say("I am JARVIS, at your service ")
        engine.runAndWait()
        
      elif (gmail_gen1 or gmail_gen2 or gmail_gen3):
        for entry in global_gmail:
          if inputstr.lower() == entry:
            os.system("python mail_check.py "+str(global_user_id))
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want me to check your gmail inbox? ")
          engine.runAndWait()
          response = raw_input("Do you want me to check your gmail inbox? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(1,inputstr))
              conn.commit()
              global_gmail.append(inputstr)
              os.system("python mail_check.py "+str(global_user_id))
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()
  
      elif (weather_gen):
        for entry in global_weather:
          if inputstr.lower() == entry:
            os.system("python weather.py "+str(global_user_id))
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Speaking of weather, do you want me to give you weather updates? ")
          engine.runAndWait()
          response = raw_input("Speaking of weather, do you want me to give you weather updates? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(2,inputstr))
              conn.commit()
              global_weather.append(inputstr)
              os.system("python weather.py "+str(global_user_id))
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()
    
      elif (calendar_gen2 or calendar_gen1):
        for entry in global_calendar:
          if inputstr.lower() == entry:
            os.system("python calendar.py "+str(global_user_id))
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want me to give you google calendar? ")
          engine.runAndWait()
          response = raw_input("Do you want me to give you google calendar? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(3,inputstr))
              conn.commit()
              global_calendar.append(inputstr)
              os.system("python calendarExample.py "+str(global_user_id))
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation.? "
        engine.say("Lets continue our conversation.?")
        engine.runAndWait()

      elif ( google_search1 or google_search2 ):
        if google_search1:
          os.system("python sample_search.py "+google_search1.group(3))
        else:
          os.system("python sample_search.py "+google_search2.group(3))
        time.sleep(2)
        print "Lets continue our conversation.? "
        engine.say("Lets continue our conversation.?")
        engine.runAndWait()

      elif ( google_news1 or google_news2 ):
        if google_news1:
          os.system("python sample_news2.py "+google_news1.group(3))
        else:
          os.system("python sample_news2.py "+google_news2.group(3))
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      elif (watsnew_gen2 or watsnew_gen1):
        for entry in global_watsnew:
          if inputstr.lower() == entry:
            os.system("python sample_watsnew.py ")
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want me to give you today's news? ")
          engine.runAndWait()
          response = raw_input("Do you want me to give you today's news? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(4,inputstr))
              conn.commit()
              global_watsnew.append(inputstr)
              os.system("python sample_watsnew.py")
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      elif (newspaper_gen):
        for entry in global_newspaper:
          if inputstr.lower() == entry:
            os.system("python newspaper.py ")
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want me to give you today's newspaper? ")
          engine.runAndWait()
          response = raw_input("Do you want me to give you today's newspaper? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(5,inputstr))
              conn.commit()
              global_newspaper.append(inputstr)
              os.system("python newspaper.py")
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation."
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      elif (in_computer_gen):
        for entry in global_in_computer:
          if inputstr.lower() == entry:
            os.system("python file_operation.py ")
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want to perform an in computer operation? ")
          engine.runAndWait()
          response = raw_input("Do you want to perform an in computer operation? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(6,inputstr))
              conn.commit()
              global_in_computer.append(inputstr)
              os.system("python file_operation.py ")
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      elif (music_gen):
        for entry in global_music:
          if inputstr.lower() == entry:
            os.system("python sample_music.py ")
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want to play music? ")
          engine.runAndWait()
          response = raw_input("Do you me want to play music? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(7,inputstr))
              conn.commit()
              global_music.append(inputstr)
              os.system("python sample_music.py ")
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      elif (reader_gen):
        for entry in global_reader:
          if inputstr.lower() == entry:
            os.system("python read_file.py ")
            recorded_expression_flag = 1
        if recorded_expression_flag == 0:
          engine.say("Do you want to open a file? ")
          engine.runAndWait()
          response = raw_input("Do you want to open a file? - ")
          for i in yes_options:
            if i in response.lower():
              c.execute("insert into selflearn values (?,?)",(8,inputstr))
              conn.commit()
              global_reader.append(inputstr)
              os.system("python read_file.py ")
        recorded_expression_flag = 0
        time.sleep(2)
        print "Lets continue our conversation. "
        engine.say("Lets continue our conversation.")
        engine.runAndWait()

      else :
        blob = TextBlob(inputstr)
        blob.correct()
        corrected_str = str(blob)
  	
        process(corrected_str,name)
        if blob.polarity < -0.2:
          if prev_mood == 0:
            prev_mood = 1
          else:
            prev_mood = 0
            os.system("python emotional_chat_engine.py " + str(global_user_id))
  	     
        if blob.polarity > 0.6 and blob.subjectivity < 0.4:
          responseText = iesha_chatbot.respond(inputstr)
          print responseText
          engine.say(responseText)
          engine.runAndWait()

        if blob.polarity < -0.6:
          responseText = iesha_chatbot.respond(inputstr)
          print(responseText)
          engine.say(responseText)
          engine.runAndWait()
        else :
          responseText = eliza_chatbot.respond(inputstr)
          print(responseText)
          engine.say(responseText)
          engine.runAndWait()
    
      c.execute("insert into chat_history values (?,?)",(global_user_id,inputstr))
      conn.commit()

    except:
      logging.error("Error in standard inputs and chat output")
      engine.say("Error in standard inputs and chat output")
      engine.runAndWait()
      raise  


try:
  def intro():
    print('---------This is JARVIS---------')
    engine.say('This is JARVIS.') 
    print('='*72)
    engine.runAndWait()
    
    global global_user_id
    inputstr = ''
    name_list = person_recorgnise()
    if name_list is None :
      print('Can you please tell me your name ?')
      engine.say('Can you please tell me your name ?')
      engine.runAndWait()
      name = raw_input(">")
      new_user(name)
    else :
      print('Can you please tell me your name ?')
      engine.say('Can you please tell me your name ?')
      engine.runAndWait()
      name = raw_input(">")
      name_present = 0
      for item in name_list:
	if name.lower() == item.lower():
	  for row in c.execute("select user_name from users"):
	    name_expected = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
	    if name_expected.lower() == name.lower():
	      c.execute("select user_id from users where user_name = '"+row[0]+"'")
	      global_user = c.fetchone()
	      global_user_id = global_user[0]
	      print('Hello '+ name + '. I recognize you now!!!')
	      print('How are you feeling today?')
	      engine.say('Hello '+ name + ' I recognize you now!')
	      engine.say('How are you feeling today?')
	      engine.runAndWait()
	      name_present = 1
	      break
      if name_present == 0:
	print('Are you a new user. I dont think I know you.')
	engine.say('Are you a new user. I dont think I know you.')
	engine.runAndWait()
	new_user(name)
    return name
except:
  logging.error("Error in user recognition")
  engine.say("Error in user recognition")
  engine.runAndWait()
  raise

try:
  def new_user(name):
    print 'Hello '+ name
    print 'How are you feeling today?'
    engine.say('Hello '+ name )
    engine.say('How are you feeling today?')
    engine.runAndWait()
    engine.say("Enter gmail username")
    engine.runAndWait()
    gmail_id = raw_input("Enter gmail username - ")
    engine.say("Enter password")
    engine.runAndWait()
    gmail_password = getpass.getpass("Enter password - ")
    engine.say("Enter city")
    engine.runAndWait()
    city = raw_input("Enter city - ")
    c.execute("SELECT MAX(user_id) FROM users")
    newuser = c.fetchone()
    newuser_id = newuser[0] + 1
    global_user_id = newuser_id
    c.execute ("insert into users values (?,?,?,?,?)",(newuser_id,name,gmail_id,gmail_password,city))
    conn.commit()

  def process(corrected_str,name):
      global global_user_id
      bloby = TextBlob(corrected_str)
      word_list= bloby.words.singularize()
      if 'relish' in word_list or'rejoice' in word_list or'cherish' in word_list or'adore' in word_list or'admire' in word_list or 'like' in word_list or 'love' in word_list or 'fancy' in word_list or 'wish i had' in word_list:
        tokens = nltk.pos_tag(word_list)
        for i in tokens:
          if i[1] == 'NN' or i[1] == 'NNP':
            c.execute("insert into likes values (?,?)",(global_user_id,i[0]))
            conn.commit()
    
  def person_recorgnise():
    file_reader = list()
    for row in c.execute("Select user_name from users"):
      name = unicodedata.normalize('NFKD', row[0]).encode('ascii','ignore')
      file_reader.append(name)
    return (file_reader)
  
  def internet_connection():
    REMOTE_SERVER = "www.google.com"
    try:
      # see if we can resolve the host name -- tells us if there is a DNS listening
      host = socket.gethostbyname(REMOTE_SERVER)
      # connect to the host -- tells us if the host is actually reachable
      s = socket.create_connection((host, 80), 2)
      return True
    except:
      pass
    return False

except:
  logging.error("Error in user initialization")
  engine.say("Error in user initialization")
  engine.runAndWait()
  raise
    
if __name__ == "__main__":
  demo()