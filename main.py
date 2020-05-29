from tkinter import Tk , Button , Entry , Frame ,Canvas ,END ,X,Y,W,LEFT,RIGHT,Label,BOTH,PhotoImage,Toplevel,HORIZONTAL,NONE 
from tkinter.ttk import Progressbar
from model import ytdata
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
from tkinter.filedialog import askdirectory
import socket, re,os
from webbrowser import open as open_url





class gui:

    # some color defined
    Theme1 = {
       "color1":"#f9f7f7",
       "color2":"#dbe2ef",
       "color3":"#3f72af",
       "color4":"#112d4e"
    }
    Theme2 = {
       "color1":"#5fdde5",
       "color2":"#f4ea8e",
       "color3":"#f37121",
       "color4":"#d92027"
    }

    # open file to read file path string
    default_path =f"C:\\Users\\{os.getenv('username')}\\Downloads\\Youtube-Video-downloader\\"
    filetxt = open("./file_path.txt","r").read() 
    if os.path.isdir(filetxt):
        filepath = filetxt
    else:
        filepath = default_path
    root = Tk()
    root.geometry("620x600")

    viewFrame = Frame()
    url=""

    def Isconnect(self):      #method to check internet 
        print("Checking Internet.....")
        try:
            socket.create_connection(("www.google.com", 80))
            
            return True
        except OSError:
            pass
        return False

    # Validation for url
    def Link_validation(self,link):
        x = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", link)

        if link == "" :
            return False
        elif x == None :
            return False
        else:
            return True
            

    # method to download video by creating another thread
    def download_video(self,stream):
        self.dlpopup()
        t2 = Thread(target=lambda :stream.download(output_path=self.filepath))
        t2.start()        

        # progress callback function
    def dlprogress(self,stream,chunk,bytes):
        total = stream.filesize - bytes
        percent =(total*100)/stream.filesize 
        self.progressbar["value"] = int(percent)
        self.progresslabel.config(text=f"Total file size : {round(stream.filesize/1048576,2)}                                                Downloaded Size :{round(total/1048576,2)} | {int(percent)}%")

        # method execute on paste button click
    def pasteBtnClicked(self):
        self.invalid_message.place_forget()
        self.viewFrame.place_forget()
        copytext = self.root.clipboard_get()
        self.tb.delete(0,END)
        self.tb.insert(0,copytext)
        self.url = self.tb.get()

        #download progress dialog popup window
    def dlpopup(self): 
        self.x = self.root.winfo_x()
        self.y = self.root.winfo_y()
        self.PopUpRoot = Toplevel(self.root)
        self.PopUpRoot.geometry("%dx%d+%d+%d" % (440,100,self.x + 100, self.y + 200))
        self.PopUpRoot.configure(background=self.Theme2["color2"],)
        self.PopUpRoot.iconbitmap("./icon/icon.ico")
        self.PopUpRoot.resizable(False,False)   
        self.progressbar = Progressbar(self.PopUpRoot,orient = HORIZONTAL, 
              length = 400, mode = 'determinate')
        self.progresslabel = Label(self.PopUpRoot,text=f"Downloading..................",bg=self.Theme2["color2"])
        self.progresslabel.place(x=17,y=10)
        self.progressbar.place(x=18,y=40)
        Button(self.PopUpRoot,text="Close",command=self.PopUpRoot.withdraw, font="bell 10 bold",borderwidth=0,bg=self.Theme2["color3"],foreground="white").place(x=180,y=70,width=100,height=26)    
        
        # on completed callback method
    def download_completed(self,stream,file_handle):
        self.PopUpRoot.withdraw()

        # method which load data by creating the object of ytdata
    def loaddata(self):
        ytdataobj = ytdata(self.url)
        ytdataobj.load_data()
        ytdataobj.yt.register_on_progress_callback(self.dlprogress)
        ytdataobj.yt.register_on_complete_callback(self.download_completed)
        self.msglabel.place_forget()
        self.view(self.root,ytdataobj)

        # method execute of download button click
    def dlBtnClicked(self):
        if self.Link_validation(self.url):
            if self.Isconnect():
                self.msglabel.place(x=200,y=160)                
                self.msglabel.config(text="Please Wait extracting data..",fg = "green")
                self.t1 = Thread(target=self.loaddata)
                self.t1.start()
            else:
                self.msglabel.place(x=200,y=160)
                self.msglabel.config(text="No Internet Check Connection",fg = "red")
                print("no internet")
        else:
            self.invalid_message.place(x=98,y=90)
        
        # method which ask for directory  to save the file
    def askSaveDirectory(self):
        self.filepath = askdirectory()
        self.pathLabel.delete(0,END)
        self.pathLabel.insert(0,self.filepath)
        update_path = open("./file_path.txt","w")
        update_path.write(self.filepath)

        # setting window 
    def SettingWindow(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        settingWinRoot = Toplevel(self.root)
        settingWinRoot.grab_set()
        settingWinRoot.resizable(False,False)
        settingWinRoot.geometry("%dx%d+%d+%d" % (500,200,x + 50,y + 50))
        settingWinRoot.title("Setting")
        settingWinRoot.iconbitmap("./icon/icon.ico")
        settingWinRoot.configure(background=self.Theme2["color3"],)
        f1 = Frame(settingWinRoot,width=450, height=500, background="bisque",borderwidth=3,relief = "raised")
        f1.pack(fill =NONE, pady=20,padx=10)
        Label(f1,text="File Path:",font="bell 12 italic",bg="bisque",fg="Black").place(x=10,y=20)
        self.pathLabel = Entry(f1,font="bell 10 bold")
        Button(f1,text="Select Path",command = self.askSaveDirectory,borderwidth=2,bg=self.Theme2["color3"],foreground="white").place(x=310,y=20)
        self.pathLabel.insert(0,self.filepath)
        self.pathLabel.place(x=100,y=20,height=25,width=200)


    def single_widget(self,root,stream):
        single_widget_frame = Frame(root,borderwidth=2, relief="groove",bg = "#4361ee",height=20)
        single_widget_frame.pack(fill=X,padx=5,pady=5)
        size=stream.filesize
        size=round(size/1048576,2)
        Label(single_widget_frame,bg = "#4361ee",fg="white",text=f"Type: {stream.mime_type}  Resolution: {stream.resolution}          File Size: {size}MB",).pack(fill=Y,side=LEFT)
        Button(single_widget_frame,text="Download",command=lambda : self.download_video(stream),bg=self.Theme1["color4"],foreground="white",relief="flat").pack(padx=10,pady=2,side=RIGHT)

        # method which show loaded data on download button click
    def view(self,root,ytData):
        URL = ytData.thumbnail_url
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        im = im.resize((440,250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)

        self.viewFrame = Frame(root, borderwidth=2, relief="groove",bg=self.Theme1["color4"])
        self.viewFrame.place(x=95,y=150)
        label = Label(self.viewFrame,image=photo,bg=self.Theme1["color4"])
        label.image = photo
        label.pack(padx=5,pady=5)
        video_title = ytData.video_title

        Label(self.viewFrame,text=video_title[slice(65)]+"...",anchor = W,  borderwidth=2, font="bell 10 bold ",bg=self.Theme1["color4"],fg="white").pack(fill=BOTH,pady=5,padx=2)
        for i in ytData.streamsList:
            self.single_widget(root=self.viewFrame,stream=i)

        # method to load icon image
    def icon_widget(self,icon_path,icon_size):
        icon = Image.open(f"{icon_path}")
        icon = icon.resize((icon_size,icon_size),Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)
        return icon

        # main entry point to run the application
    def run(self):
        instagramlink = "https://www.instagram.com/prog.rammingislove/"
        githublink = "https://github.com/swaraj344"
        linkedin = "https://www.linkedin.com/in/swaraj-kumar-b63376171/"


        hearticon = self.icon_widget("./icon/heart.png",28)
        settingicon = self.icon_widget("./icon/settingicon.png",40)
        connectedicon =self.icon_widget("./icon/connected.png",30)
        notconnected = self.icon_widget("./icon/notconnected.png",30)
        instagramicon = self.icon_widget("./icon/instagram.png",24)
        githubicon = self.icon_widget("./icon/github.png",24)
        linkedinicon = self.icon_widget("./icon/linkedin.png",24)


        
        self.root.title("Youtube Video Downloader")
        self.root.iconbitmap("./icon/icon.ico")
        self.root.resizable(False,True)
        self.root.configure(background=self.Theme2["color2"],)
        self.tb = Entry(self.root,font="bell 12 italic",bg=self.Theme1["color1"])
        
        self.tb.place(x=100,y=50,height=40,width=450)
        pastebtn = Button(self.root,text="Paste Link",command=self.pasteBtnClicked , font="bell 10 bold",borderwidth=0,bg=self.Theme2["color3"],foreground="white")
        pastebtn.place(x=340,y=100,width = 100,height=30)
        dlbtn = Button(self.root,text="Download",command =self.dlBtnClicked, font="bell 10 bold",borderwidth=2,relief="flat",bg=self.Theme1["color3"],foreground="white")
        dlbtn.place(x=450,y=100,width = 100,height=30)
        self.msglabel = Label(self.root,font="bold 14",bg=self.Theme2["color2"],fg="green")
        Button(self.root,text="hded",image = settingicon,borderwidth=0,command=self.SettingWindow,bg=self.Theme2["color2"]).place(x=550,y=540)
        self.invalid_message = Label(self.root,text="Invalid Link Please Check Your Link",fg="red",bg=self.Theme2['color2'],font="bell 10 bold")
        Label(self.root,text ="Made With           By Swaraj Kumar",justify="center",bg=self.Theme2["color2"],font ="bell 9 bold").place(x=198,y=560  )
        Label(self.root,image = hearticon ,bg=self.Theme2["color2"]).place(x=260 ,y=556)
        internettext = Label(self.root,bg = self.Theme2['color2'])
        internettext.place(x=520,y=14) 
        interneticon = Label(self.root ,bg=self.Theme2["color2"])
        interneticon.place(x=480,y=7)
        Button(self.root,image=instagramicon,bg =self.Theme2['color2'],borderwidth = 0,command=lambda :  open_url(instagramlink)).place(x=5,y=562)
        Button(self.root,image=githubicon,bg =self.Theme2['color2'],borderwidth = 0,command=lambda :  open_url(githublink)).place(x=35,y=562)
        Button(self.root,image=linkedinicon,bg =self.Theme2['color2'],borderwidth = 0,command=lambda :  open_url(linkedin)).place(x=65,y=562)

        if self.Isconnect():
            interneticon.config(image=connectedicon)
            internettext.config(text = "Connected",fg = 'green')
        else:
            interneticon.config(image = notconnected)
            internettext.config(text = "Not Connected",fg = 'Red') 

        self.root.mainloop()


if __name__ == "__main__":
    obj = gui()
    obj.run()