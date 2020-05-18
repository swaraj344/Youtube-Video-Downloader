from tkinter import Tk , Button , Entry , Frame ,Canvas ,END ,X,Y,W,LEFT,RIGHT,Label,BOTH,PhotoImage
from model import ytdata
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO



class gui:
    root = Tk()
    
    url="https://www.youtube.com/watch?v=Y9VgmhxtJFk"

    def download_video(self,stream):
        stream.download()

    def pasteBtnClicked(self):
        copytext = self.root.clipboard_get()
        self.tb.delete(0,END)
        self.tb.insert(0,copytext)
        self.url = self.tb.get()
    def dlBtnClicked(self):
        # self.url = self.tb.get()
        ytdataobj = ytdata(self.url)
        ytdataobj.load_data()

        self.view(self.root,ytdataobj)


    def single_widget(self,root,stream):
        single_widget_frame = Frame(root,borderwidth=2, relief="groove")
        single_widget_frame.pack(fill=X)
        size=stream.filesize
        size=round(size/1048576,2)
        Label(single_widget_frame,text=f"Type: {stream.mime_type}  Resolution: {stream.resolution}          File Size: {size}MB").pack(fill=Y,side=LEFT)
        Button(single_widget_frame,text="Download",command=lambda : self.download_video(stream)).pack(padx=10,pady=5,side=RIGHT)

    def view(self,root,ytData):
        URL = ytData.thumbnail_url
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        im = im.resize((440,250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)

        viewFrame = Frame(root, borderwidth=2, relief="groove")
        viewFrame.place(x=95,y=150)
        label = Label(viewFrame,image=photo)
        label.image = photo
        label.pack()
        video_title = ytData.video_title

        Label(viewFrame,text=video_title[slice(65)]+"...",anchor = W,  borderwidth=2, font="bell 10 bold ").pack(fill=BOTH,pady=5,padx=2)
        for i in ytData.streamsList:
            self.single_widget(root=viewFrame,stream=i)

    def run(self):
        self.root.title("Youtube Video Downloader")
        
        self.root.iconbitmap("./icon/icon.ico")

        self.root.geometry("620x600")
        self.root.configure(background='#d7f0f5',)
        self.tb = Entry(self.root,text="paste Your link here",font="bell 14 italic")
        
        self.tb.place(x=100,y=50,height=40,width=450)
        pastebtn = Button(self.root,text="Paste Link",command=self.pasteBtnClicked , font="bell 10 italic")
        pastebtn.place(x=370,y=100)
        dlbtn = Button(self.root,text="Download",command =self.dlBtnClicked, font="bell 10 bold")
        dlbtn.place(x=450,y=100)
        
        

        self.root.mainloop()


if __name__ == "__main__":
    obj = gui()
    obj.run()