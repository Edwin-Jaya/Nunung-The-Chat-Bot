import random
from pytube import YouTube
from faulthandler import disable
from datetime import datetime
from tkinter import *
import tkinter as tk
import json
from PIL import ImageTk, Image
from io import BytesIO
from urllib.request import urlopen
from itertools import count, cycle
 
class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1024x640")
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
        chatFrame=Frame(self, background="Black", width=512, height=640)
        chatFrame.grid(row= 0,column=0)
        chatFrame.pack_propagate(False)
        global ytFrame
        ytFrame=Frame(self, background="Black", width=512, height=640)
        ytFrame.grid(row= 0,column=1)
        ytFrame.pack_propagate(False)
        self.resizable(False, False)
        self.title("Nunung The Chat Bot By Edwin Liona Jaya")
        headerPanel = Frame(chatFrame, bg="black")
        img = ImageTk.PhotoImage(Image.open("./Images/headerPanel.jpg").resize((512, 80), Image.ANTIALIAS))
        lbl = tk.Label(headerPanel, image=img)
        lbl.img = img  
        lbl.place(relx=0.5, rely=0.5, anchor='center') 
        headerPanel.pack(fill=BOTH)
        #photo = ImageTk.PhotoImage(Image.open('./Images/nunung.jpg'))
        #labelpic=tk.Label(headerPanel,image=photo, borderwidth=0)
        #labelpic.photo = photo
        #labelpic.pack(padx=8, pady=10, side=LEFT)
        photo = ImageLabel(headerPanel,borderwidth=0)
        photo.pack(padx=8, pady=10, side=LEFT)
        photo.load('./Images/nunung-profile.gif')  
        label = tk.Label(headerPanel, foreground="White", background="Black",text="Nunung", font=("Verdana", 14))
        label.pack(padx=2, pady=10, side=LEFT)
        labelVersion = tk.Label(headerPanel, foreground="White", background="Black",text="version 1.0", font=("arial", 10))
        labelVersion.pack(padx=10, pady=10, side=RIGHT)
        #ytFrame
        imgRain = ImageTk.PhotoImage(Image.open("./Images/nunungRoom.jpg").resize((512, 640), Image.ANTIALIAS))
        lbl = tk.Label(ytFrame, image=imgRain)
        lbl.imgRain = imgRain  
        lbl.place(relx=0.5, rely=0.5, anchor='center')
        #chat Panel
        chatPanel = Frame(chatFrame)
        chatPanel.pack(fill=BOTH)
        global teks
        teks = tk.Text(chatPanel, wrap='word', bg="black", height=31)
        userInputPanel = Frame(chatFrame, bg="black")
        userInputPanel.pack(side=BOTTOM, fill=BOTH)
        scrollbar = Scrollbar(chatPanel, orient=VERTICAL, bg="White")
        scrollbar.pack(side=RIGHT,
                       fill=Y)
        #panelEntry
        global user_var
        user_var = tk.StringVar()
        userEntry = tk.Entry(userInputPanel, width=43, font=('arial', 12, 'normal'), textvariable=user_var,bd=1,\
            relief=FLAT,highlightbackground="white",highlightcolor="black", highlightthickness=2)
        userEntry.pack(side=LEFT, pady=15, padx=15)
        sendButton = tk.Button(userInputPanel, text=" > ",font=('fixedsys', 18, 'bold'), background="Black", foreground="Green", \
            command=self.send, borderwidth=0)
        sendButton.pack(side=LEFT)
        scrollbar.config(command=teks.yview)
        userEntry.bind('<Return>', self.sendEnter)
        teks.tag_configure('bot_text', foreground="green")
        teks.tag_configure('warning', foreground="red")
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
    
    def setYoutubeFrameUI(self):
        global contentPanel
        contentPanel=Frame(ytFrame, background="Black", width=512, height=640)
        contentPanel.grid(row= 0,column=0)
        contentPanel.pack_propagate(False)
        imgRain = ImageTk.PhotoImage(Image.open("./Images/youtubeNunung.jpg").resize((512, 640), Image.ANTIALIAS))
        lbl = tk.Label(ytFrame, image=imgRain)
        lbl.imgRain = imgRain  
        lbl.place(relx=0.5, rely=0.5, anchor='center')
        global searchEntry
        global ytlink
        ytlink = tk.StringVar()
        searchEntry = tk.Entry(ytFrame, width=50, textvariable=ytlink)
        searchEntry.grid(row=0,sticky="n", ipady=3,pady=15)
        searchEntry.insert(0,'Put your youtube link here')
        searchEntry.bind('<Button-1>', self.clearBox)
        searchEntry.bind('<Return>', self.getYoutubeVideosData)
        self.retrieve(self)

    def getYoutubeVideosData(self,event):
        tagChat='warning'
        youtubelink = ytlink.get()
        print(youtubelink)
        global yt
        yt = YouTube(youtubelink)
        vidauthor=yt.author
        vidlength=yt.length
        vidtitle=yt.title
        imgurl = yt.thumbnail_url
        u = urlopen(imgurl)
        img_raw_data = u.read()
        u.close()
        self.setYoutubeThumb(vidtitle,img_raw_data,vidauthor,vidlength)
        sendButton = tk.Button(ytFrame, text=" D O W N L O A D ",font=('fixedsys', 18, 'bold'), background="Black", foreground="Green", \
        command=self.downloadVideo, borderwidth=0)
        sendButton.place(relx=0.5, rely=0.8, anchor='center')
        br = botName + " : " + "Okay, okay, hold on a sec. Don't panic if you see me not responding ok,"+ \
                " that'd happen because i'd have to hack into satellite and stuff. It's hard you know, so just sit tight. Be a good boy and imma give you 720p. *wink*"
        self.insertText(br,tagChat)
    
    def convert(self,seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return "%d:%02d:%02d" % (hour, min, sec)
    
    def setYoutubeThumb(self,title,thumb,author,length):
        vidlength=self.convert(length)
        videostitle = tk.Label(ytFrame,text=title,font=("arial",16),wraplength=400)
        videostitle.place(relx=0.5, rely=0.2, anchor='center')
        img = Image.open(BytesIO(thumb)).resize((200, 150), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(ytFrame, image=photo)
        lbl.imgRain = photo  
        lbl.place(relx=0.5, rely=0.4, anchor='center')
        videosauthor = tk.Label(ytFrame,text="Author : "+author,font=("arial",12),wraplength=400)
        videosauthor.place(relx=0.3, rely=0.6, anchor='center')
        videoslength = tk.Label(ytFrame,text="Length : "+vidlength,font=("arial",12),wraplength=400)
        videoslength.place(relx=0.7, rely=0.6, anchor='center')
    
    def downloadVideo(self):
        tagChat='warning'
        mp4files = yt.streams.filter(progressive=True).get_highest_resolution()
        SAVE_PATH = "E:/"
        try:
            mp4files.download(SAVE_PATH) 
            br = botName + " : " + "Done. I put it in " + SAVE_PATH +". Your welcome."
            self.insertText(br,tagChat)
        except: 
            br = botName + " : " + "Something's wrong. Failed."
            self.insertText(br,tagChat)

    def clearBox(self,event):
        searchEntry.delete(0, END)
        return
    
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
            case ["yt", "nunung"]:
                words = botName + " : " + "You know you could just stream it... but ok, imma switch to my laptop."
                self.insertText(words,tagChat)
                self.setYoutubeFrameUI()
            case ["quit"]:
                exit()
            case _:
                self.confusedResp()

    def help(self):
        tagChat="warning"
        words="LIST COMMAND : \n" \
              "-----------------------------------------------\n" \
              "1. Greetings : 'hi nunung','hello nunung','sup nunung'\n" \
              "2. Tell Time : 'tell me time nunung'\n" \
              "3. Help      : 'help nunung' \n" \
              "4. Youtube Download      : 'yt nunung' \n" \
              "5. Quit      : 'quit'"
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

class ImageLabel(tk.Label):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
 
if __name__ == '__main__':
    app = app()
    app.mainloop()


