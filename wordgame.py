# SIMPLE WORD GAME
import time, os
import keyboard
from random import randint
import threading
class game:
    def __init__(self, words):
        self.words = words
        self.wordlist = words.split(' ')
        self.userword = "test"
        self.gamestrings = []
        self.maxlen = 0
        self.game = self.createGame()
        self.losed = 0
        self.points = 0
        self.route = 0
        self.lock = threading.Lock()
        self.keystatus = False
        keyboard.hook(self.press)
        #threading.Thread(target=self.graphics, args=()).start()
        threading.Thread(target=self.testing).start()
        keyboard.wait("esc")
        keyboard.unhook(self.press)

    def press(self, event):
        if self.keystatus == False:
            self.keystatus = True
        else:
            self.keystatus = False


        if event.name == "space":
#            for string in self.gamestrings:
 #               if string.find(self.userword,len(string)-150-i,len(string)-i) != -1:
  #                  self.points += 1
   #                 self.wordlist.remove(self.userword)
    #                self.gamestrings[counter].replace(word,len(word) * " ")
            self.userword = ""
        elif self.keystatus == True:
            self.userword += event.name
        #if len(event.name) == 2:
        #if event.name[0] == event.name[1]:
        
    def createGame(self):
        words = self.wordlist
        if len(words) < 20:
            print("Minimum Words ist 20")
            quit()
        if len(words) % 2 == 1:
            words.pop(len(words) -1)
        game = []
        columlen = int(0.05 * len(words))
        for i in range(1,21,1): # Spiel Linien
            columend = i * columlen
            columstart = columend - columlen
            print("Building line {} with {} Words, wordstart: {}, wordend: {}".format(i, columend-columstart , columstart, columend))
            time.sleep(0.1)
            build = []
            gamestrings = []
            for colum in range(columstart, columend, 1):
                randnum = randint(40,90) # Zufälliger Abstand zwischen den wörtern 
                build.append(words[colum])
                build.append(randnum)
            
            randnum = randint(40,70) # Zufälliger Abstand zwischen den wörtern 
            build.append(randnum)
            game.append(build)
        for colum in game:
            columstring = ""
            for item in colum:
                if isinstance(item, int):
                    columstring += item * " "
                else:
                    columstring += str(item)
            print("Appending string with {} chars.".format(len(columstring)))
            time.sleep(0.1)
            gamestrings.append(columstring)

        maxlen = 0
        print('Search for max length..')
        time.sleep(0.1)
        for strings in gamestrings:
            if len(strings) > maxlen:
                maxlen = len(strings)
        self.maxlen = maxlen
        print('max length:', self.maxlen)
        time.sleep(0.1)
        print('Checking Strings')
        time.sleep(0.1)
        for strings in gamestrings:
            if len(strings) < maxlen:
                missing = maxlen - len(strings)
                print("{} Missing, Pumping: {}-->{}".format(missing, len(strings), len(strings) + missing))
                time.sleep(0.1)
                self.gamestrings.append(missing * " " + strings)
            else:
                print('Length is good', len(strings))
                time.sleep(0.1)
                self.gamestrings.append(strings)
        return game 

    def graphics(self):
        print("Graphics started", self.maxlen)
        time.sleep(1)
        for i in range(self.maxlen):
            if keyboard.is_pressed("esc"):
                break
            time.sleep(0.2)
            self.route = i
            os.system("clear")
            for string in self.gamestrings:
                i = self.route
                print(string[len(string)-150-i:len(string)-i]) #In dem beeich bei eingabe nach dem wort suchen, nach dem ende des bereiches nach Wörter suchen aus liste, punkt abzug.
                for word in self.wordlist:
                    if string.find(word,len(string)-i+len(word),len(string)) != -1:
                        self.losed += 1
                        self.wordlist.remove(word)
            print("Missed Words: {}  Points: {}  Typing: {} Route: {}/{}".format(self.losed, self.points, self.userword,self.route, self.maxlen))

    def testing(self):
        print('Thread started')
        time.sleep(0.1)
        while not keyboard.is_pressed("esc"):
            time.sleep(1)
            os.system("clear")
            print(self.userword)
f = open('text.txt', "r+")
txt = f.read()
f.close()
game(txt)
