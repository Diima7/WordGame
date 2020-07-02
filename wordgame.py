# SIMPLE WORD GAME
import time, os
from pynput import keyboard
from random import randint
import threading
class game:
    def __init__(self, words):
        self.inspection = False 
        self.words = words
        replacelist = [".", ",", "\n", "/", "!", "?", "  ", "   "]
        for rep in replacelist:
            self.words = self.words.replace(str(rep), " ")
        self.wordlist = list(set(self.words.split(' ')))
        for word in reversed(self.wordlist):
            if word == "" or word == " " or word == "  ":
                self.wordlist.remove(word)
                
        self.userword = ""
        self.gamestrings = []
        self.maxlen = 0
        self.game = self.createGame()
        self.losed = 0
        self.points = 0
        self.route = 0
        if self.inspection == False:
            listener = keyboard.Listener(
            on_press=self.press,
            on_release=self.on_release)
            listener.start()
            threading.Thread(target=self.graphics, args=()).start()
            #threading.Thread(target=self.testing).start()
        else:
            print("INSPECTION MODE \n\nMAXLEN: {}\nTEXT:\n{}\nEND OF TEXT\n\nWORDLIST:\n{}\nEND OF WORDLIST\n\nGAMESTRINGS:\n{}\nEND OF GAMESTRINGS\n\nGAME:\n{}\n\nEND OF GAME".format(
                    self.maxlen, self.words, self.wordlist, self.gamestrings, self.game))

    def on_release(self, key):
        pass

    def press(self, key):
        try:
            self.userword += key.char
        except AttributeError:
            try:
                if key == keyboard.Key.space:
                    word = self.userword
                    self.userword = ""
                    counter = 0
                    for string in self.gamestrings:
                        counter += 1
                        i = self.route
                        if string.find(word,len(string)-150-i, len(string)-i+len(word)-1) != -1:
                            if word in self.wordlist:
                                self.points += 1
                                self.wordlist.remove(word)
                                self.gamestrings[counter-1] = string.replace(word, len(word) * " ")            
                elif key == keyboard.Key.backspace:
                    self.userword = self.userword[:len(self.userword) -1]
            except Exception as ex:
                print(ex)
                os._exit(1)
        except Exception as ex:
            print(ex)
            os._exit(1)

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
            build = []
            gamestrings = []
            for colum in range(columstart, columend, 1):
                randnum = randint(80,180) # Zufälliger Abstand zwischen den wörtern 
                build.append(words[colum])
                build.append(randnum)
            
            randnum = randint(20,40) # Zufälliger Abstand zwischen den wörtern 
            build.append(randnum)
            game.append(build)
        if self.inspection:
            print(game)
        for colum in game:
            columstring = ""
            for item in colum:
                if isinstance(item, int):
                    columstring += item * " "
                else:
                    columstring += str(item)
            print("Appending string with {} chars.".format(len(columstring)))
            gamestrings.append(columstring)
        
        if self.inspection:
            for string in gamestrings:
                print(string)
        maxlen = 0
        print('Search for max length..')
        for strings in gamestrings:
            if len(strings) > maxlen:
                maxlen = len(strings)
        self.maxlen = maxlen
        print('max length:', self.maxlen)
        print('Checking Strings')
        for strings in gamestrings:
            if len(strings) < maxlen:
                missing = maxlen - len(strings)
                print("{} Missing, Pumping: {}-->{}".format(missing, len(strings), len(strings) + missing))
                self.gamestrings.append((missing + 151) * " " + strings)
            else:
                print('Length is good', len(strings))
                self.gamestrings.append(strings)
        return game 

    def graphics(self):
        print("Graphics started", self.maxlen)
        for i in range(self.maxlen):
            self.route = i
            os.system("clear")
            for string in self.gamestrings:
                i = self.route
                print(string[len(string)-150-i:len(string)-i] + "|") #In dem beeich bei eingabe nach dem wort suchen, nach dem ende des bereiches nach Wörter suchen aus liste, punkt abzug.
                for word in self.wordlist:
                    if string.find(word,len(string)-i+len(word),len(string)) != -1:
                        self.losed += 1
                        self.wordlist.remove(word)
            print("Missed Words: {}  Points: {}  Typing: {} Route: {}/{}  Words Left: {}".format(self.losed, self.points, self.userword,self.route, self.maxlen, len(self.wordlist)))
            time.sleep(0.08)
        print("GAME END")

    
    def testing(self):
        print('Thread started')
        time.sleep(0.12)
        while True:
            time.sleep(3)
            os.system("clear")
            print(self.userword)
f = open('text.txt', "r+")
txt = f.read()
f.close()
game(txt)
