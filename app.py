import random
from faulthandler import disable
import nltk
from nltk.chat.util import Chat, reflections
from datetime import datetime
from tkinter import *
import tkinter as tk
import json


class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initUI()
        timenow = datetime.now()
        global currenttime
        currenttime = timenow.strftime("%H:%M:%S")
        b=open("botrespond.json","r")
        global botrespond
        botrespond=json.load(b)
        global botName
        botName = "nunung"
        self.getWelcomeMessage()

    def initUI(self):
        #header Panel
        self.geometry("450x500")
        self.title("Nunung The Chat Bot By Edwin Liona Jaya")
        photo = PhotoImage(file="girl.png")
        headerPanel = Frame(self, bg="black")
        headerPanel.pack(fill=BOTH)
        labelpic=tk.Label(headerPanel,image=photo)
        labelpic.pack(padx=10, pady=10, side=LEFT)
        label = tk.Label(headerPanel, foreground="White",background="Black", text="Nunung", font=("arial", 12))
        label.pack(padx=10, pady=10, side=LEFT)
        labelVersion = tk.Label(headerPanel, foreground="White",background="Black" ,text="version 1.0", font=("arial", 10))
        labelVersion.pack(padx=10, pady=10, side=RIGHT)
        #chat Panel
        chatPanel = Frame(self, bg="white")
        chatPanel.pack(fill=BOTH)
        userInputPanel = Frame(self, bg="black")
        userInputPanel.pack(side=BOTTOM, fill=BOTH)
        scrollbar = Scrollbar(chatPanel, orient=VERTICAL, jump=1)
        scrollbar.pack(side=RIGHT,
                       fill=Y)
        global user_var
        user_var = tk.StringVar()
        userEntry = tk.Entry(userInputPanel, width=40, font=('Arial', 12, 'normal'), textvariable=user_var)
        userEntry.pack(side=LEFT, pady=15, padx=15)
        sendButton = tk.Button(userInputPanel, text="SEND", command=self.send)
        sendButton.pack(side=LEFT)
        global teks
        teks = tk.Text(chatPanel, wrap='word')
        scrollbar.config(command=teks.yview)

    def send(self):
        global user_var
        if (user_var != ""):
            userEntry = user_var.get()
            concat = "user : " + userEntry
            self.insertText(concat)
            self.botRespond(userEntry)
            user_var.set("")


    def insertText(self, text):
        global teks
        teks.configure(state=NORMAL)
        teks.insert(END, text + "\n")
        teks.configure(state=DISABLED)
        teks.pack()
        return teks

    def getWelcomeMessage(self):
        introwordsstr="Hi! Welcome human! My name is Nunung, i'm a rule based bot by Edwin Liona Jaya." \
                      " If you wanna command me to do something just say it and end it with 'nunung'." \
                      " For Example if you wanna know the time, you could say 'tell me time nunung'." \
                      " For the details of my commmand you could type 'help nunung'. \n" \
                      "Thank you!!!"
        br = botName + " : " + introwordsstr
        self.insertText(br)

    def botRespond(self,word):
        bedTime = "21:00:00"
        lunchTime = "12:00:00"
        dumbMasterTime = "17:00:00"
        match word.split():
            case ["hi", botName ]| ["hello", botName]| ["sup", botName]:
                a = random.choice(botrespond['greetings'])
                br = botName + " : " + a
                self.insertText(br)
            case ["what","time", "is","it", botName,"?"] | ["tell","me", "time", botName]:
                br = botName + " : " + "It's " + currenttime + " in your area."
                self.insertText(br)
                if(currenttime>=bedTime):
                    words="You should get some sleep! You need a healthy body, mind, and soul to be success :)"
                    self.insertText(words)
                elif (currenttime >= lunchTime and currenttime <= "13:00:00"):
                    words = "Have you ate some lunch? Don't forget to have some lunch!"
                    self.insertText(words)
                elif (currenttime >= dumbMasterTime and currenttime <= "18:00:00"):
                    words = "Lmao, it made me remember something. My maker was searching how to insert a text in tkinter at this hour." \
                            " Well, he's not bad and not good either. But sometimes when he didn't have coffee for breakfast, he'd be dumb asf." \
                            " Btw it's a perfect time to take a shower to keep your body, mind, and soul cleannn."
                    self.insertText(words)
            case ["help",botName]:
                self.help()
            case ["quit"]:
                exit()
            case _:
                self.confusedResp()

    def help(self):
        words="LIST COMMAND : \n" \
              "1. Greetings : 'hi nunung','hello nunung','sup nunung'\n" \
              "2. Tell Time : 'what time is it nunung ?', 'tell me time nunung'\n" \
              "4. Help      : 'help nunung' \n" \
              "3. Quit      : 'quit'"
        self.insertText(words)

    def confusedResp(self):
        confused = botName + " : " + "Hmm... I'm sorry, i don't understand what you said :( Please check your typing or type help to see my command list."
        self.insertText(confused)
        return confused

    def getDictToStr(self, word):
        convert = str(word).replace("}", "").replace("{", "").replace("[", "").replace("]", "").replace("'","").replace(",", " ").replace('"', " ")
        return convert


if __name__ == '__main__':
    app = app()
    app.mainloop()


