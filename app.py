import random
from faulthandler import disable
from datetime import datetime
from tkinter import *
import tkinter as tk
import json
from PIL import ImageTk, Image
from io import BytesIO
from urllib.request import urlopen

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
        botName = "Nunung"
        self.getWelcomeMessage()

    def initUI(self):
        #header Panel
        self.resizable(False, False)
        self.geometry("450x525")
        self.title("Nunung The Chat Bot By Edwin Liona Jaya")
        headerPanel = Frame(self, bg="black")
        img = ImageTk.PhotoImage(Image.open("./Images/headerPanel.jpg").resize((450, 80), Image.ANTIALIAS))
        lbl = tk.Label(headerPanel, image=img)
        lbl.img = img  
        lbl.place(relx=0.5, rely=0.5, anchor='center') 
        headerPanel.pack(fill=BOTH)
        photo = ImageTk.PhotoImage(Image.open('./Images/nunung.jpg'))  
        labelpic=tk.Label(headerPanel,image=photo, borderwidth=0)
        labelpic.photo = photo
        labelpic.pack(padx=8, pady=10, side=LEFT)
        label = tk.Label(headerPanel, foreground="White", background="Black",text="Nunung", font=("Verdana", 14))
        label.pack(padx=2, pady=10, side=LEFT)
        labelVersion = tk.Label(headerPanel, foreground="White", background="Black",text="version 1.0", font=("arial", 10))
        labelVersion.pack(padx=10, pady=10, side=RIGHT)
        #chat Panel
        chatPanel = Frame(self)
        chatPanel.pack(fill=BOTH)
        global teks
        teks = tk.Text(chatPanel, wrap='word', bg="black")
        userInputPanel = Frame(self, bg="black")
        userInputPanel.pack(side=BOTTOM, fill=BOTH)
        scrollbar = Scrollbar(chatPanel, orient=VERTICAL, bg="White")
        scrollbar.pack(side=RIGHT,
                       fill=Y)
        global user_var
        user_var = tk.StringVar()
        userEntry = tk.Entry(userInputPanel, width=40, font=('arial', 12, 'normal'), textvariable=user_var,bd=1,\
            relief=FLAT,highlightbackground="white",highlightcolor="black", highlightthickness=2)
        userEntry.pack(side=LEFT, pady=15, padx=15)
        sendButton = tk.Button(userInputPanel, text=" > ",font=('fixedsys', 18, 'bold'), background="Black", foreground="Green", \
            command=self.send, borderwidth=0)
        sendButton.pack(side=LEFT)
        scrollbar.config(command=teks.yview)
        userEntry.bind('<Return>', self.sendEnter)
        teks.tag_configure('bot_text', foreground="green")
        teks.tag_configure('user_text', foreground="white")

    def send(self):
        tagChat='user_text'
        global user_var
        if (user_var != ""):
            userEntry = user_var.get()
            concat = "user : " + userEntry
            self.insertText(concat,tagChat)
            self.botRespond(userEntry)
            user_var.set("")
    
    def sendEnter(self,event):
        tagChat='user_text'
        global user_var
        if (user_var != ""):
            userEntry = user_var.get()
            concat = "user : " + userEntry
            self.insertText(concat, tagChat)
            self.botRespond(userEntry)
            user_var.set("")

    def insertText(self, text, tagChat):
        global teks
        teks.configure(state=NORMAL)
        teks.insert(END, text + "\n", tagChat)
        teks.configure(state=DISABLED)
        teks.see(END)
        teks.pack()
        return teks

    def getWelcomeMessage(self):
        tagChat='bot_text'
        introwordsstr="Hi! Welcome human! My name is Nunung, i'm a rule based bot by Edwin Liona Jaya." \
                      " If you wanna command me to do something just say it and end it with 'nunung'." \
                      " For Example if you wanna know the time, you could say 'tell me time nunung'." \
                      " For the details of my commmand you could type 'help nunung'. \n" \
                      "Thank you!!!"
        br = botName + " : " + introwordsstr
        self.insertText(br,tagChat)

    def botRespond(self,word):
        global botName
        tagChat='bot_text'
        bedTime = "21:00:00"
        lunchTime = "12:00:00"
        dumbMasterTime = "17:00:00"
        match word.split():
            case ["hi", "nunung" ]| ["hello", "nunung"]| ["sup", "nunung"]:
                a = random.choice(botrespond['greetings'])
                br = botName + " : " + a
                self.insertText(br,tagChat)
            case ["tell","me", "time", "nunung"]:
                br = botName + " : " + "It's " + currenttime + " in your area."
                self.insertText(br,tagChat)
                if(currenttime>=bedTime):
                    words="You should get some sleep! You need a healthy body, mind, and soul to be success :)"
                    self.insertText(words,tagChat)
                elif (currenttime >= lunchTime and currenttime <= "13:00:00"):
                    words = "Have you ate some lunch? Don't forget to have some lunch!"
                    self.insertText(words,tagChat)
                elif (currenttime >= dumbMasterTime and currenttime <= "18:00:00"):
                    words = "Lmao, it made me remember something. My maker was searching how to insert a text in tkinter at this hour." \
                            " Well, he's not bad and not good either. But sometimes when he didn't have coffee for breakfast, he'd be dumb asf." \
                            " Btw it's a perfect time to take a shower to keep your body, mind, and soul cleannn."
                    self.insertText(words,tagChat)
            case ["help","nunung"]:
                self.help()
            case ["quit"]:
                exit()
            case _:
                self.confusedResp()

    def help(self):
        tagChat="bot_text"
        words="LIST COMMAND : \n" \
              "1. Greetings : 'hi nunung','hello nunung','sup nunung'\n" \
              "2. Tell Time : 'tell me time nunung'\n" \
              "4. Help      : 'help nunung' \n" \
              "3. Quit      : 'quit'"
        self.insertText(words,tagChat)

    def confusedResp(self):
        tagChat="bot_text"
        confused = botName + " : " + "Hmm... I'm sorry, i don't understand what you said :( " \
            +"Please check your typing or type 'help nunung' to see my command list."
        self.insertText(confused,tagChat)
        return confused

    def getDictToStr(self, word):
        convert = str(word).replace("}", "").replace("{", "").replace("[", "").replace("]", "").replace("'","").replace(",", " ").replace('"', " ")
        return convert


if __name__ == '__main__':
    app = app()
    app.mainloop()


