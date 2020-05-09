from tkinter import *
import clipboard
from model import ytdata


class gui:
    url=None

    def download_video(self,stream):
        stream.download()

    def pasteBtnClicked(self):
        copytext = clipboard.paste()
        self.tb.delete(0,END)
        self.tb.insert(0,copytext)
    def dlBtnClicked(self):
        self.url = self.tb.get()
        ytdataobj = ytdata(self.url)
        ytdataobj.load_data()

        self.view(self.root,ytdataobj)


    def single_widget(self,root,stream):
        single_widget_frame = Frame(root,)
        single_widget_frame.pack(fill=X)
        size=stream.filesize
        size=round(size/1048576,2)
        Label(single_widget_frame,text=f"Type: {stream.mime_type}  Resolution: {stream.resolution} File Size: {size}MB").pack(fill=Y,side=LEFT)
        Button(single_widget_frame,text="Download",command=lambda : self.download_video(stream)).pack(padx=10,fill=Y,side=RIGHT)

    def view(self,root,ytData):
        viewFrame = Frame(root, borderwidth=20, relief="flat")
        viewFrame.place(x=50,y=200)
        Label(viewFrame,text=ytData.video_title,  borderwidth=2, relief="groove" ,font="bell 10 ",).pack(fill=X,pady=10,padx=12)
        for i in ytData.streamsList:
            self.single_widget(root=viewFrame,stream=i)

    def run(self):
        self.root = Tk()
        self.root.geometry("600x600")
        self.root.configure(background='#d7f0f5',)
        self.tb = Entry(self.root,text="paste Your link here",font="bell 14 italic")
        
        self.tb.place(x=100,y=50,height=40,width=400)
        pastebtn = Button(self.root,text="Paste Link",command=self.pasteBtnClicked , font="bell 10 italic")
        pastebtn.place(x=270,y=110)
        dlbtn = Button(self.root,text="Download",command =self.dlBtnClicked, font="bell 10 bold")
        dlbtn.place(x=270,y=145)
        
        

        self.root.mainloop()


if __name__ == "__main__":
    obj = gui()
    obj.run()