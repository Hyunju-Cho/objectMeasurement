import tkinter
from tkinter import Tk, filedialog
import cv2
import numpy as np
import imutils
from PIL import Image
from PIL import ImageTk
import time
import pandas as pd

class videoGUI:
    def __init__(self,window,window_title):
        self.window=window
        self.window.title(window_title)
        self.window.geometry("1000x800")
        self.window.resizable(False,False)

        # ------------영상 재생&시간 공간, 버튼------------
        self.lblVideo=tkinter.Label(self.window)
        self.lblVideo.place(x=250,y=60)

        self.openbtn=tkinter.Button(self.window,text="Open",width=20,command=lambda:self.openFile())
        self.openbtn.place(x=150,y=10)

        self.stopbtn=tkinter.Button(self.window,text="Stop",width=20,command=lambda:self.stopFile())
        self.stopbtn.place(x=450,y=10)

        self.savebtn=tkinter.Button(self.window,text="Save",width=20,command=lambda:self.saveFile())
        self.savebtn.place(x=750, y=10)

        # ------------하단 좌측 값 표시------------
        self.lblTime=tkinter.Label(self.window, text="시각")
        self.lblTime.place(x=20,y=400)
        self.lblTimeVal=tkinter.Label(self.window)
        self.lblTimeVal.place(x=70,y=400)

        self.lblArea=tkinter.Label(self.window, text="넓이")
        self.lblArea.place(x=20,y=450)
        self.lblAreaVal=tkinter.Label(self.window)
        self.lblAreaVal.place(x=70,y=450)

        self.lblHeight=tkinter.Label(self.window, text="높이")
        self.lblHeight.place(x=20,y=500)
        self.lblHeightVal=tkinter.Label(self.window)
        self.lblHeightVal.place(x=70,y=500)

        self.lblWidth=tkinter.Label(self.window, text="폭")
        self.lblWidth.place(x=20,y=550)
        self.lblWidthVal=tkinter.Label(self.window)
        self.lblWidthVal.place(x=70,y=550)

        self.lblCenter=tkinter.Label(self.window, text="중심점")
        self.lblCenter.place(x=20,y=600)
        self.lblCenterVal=tkinter.Label(self.window)
        self.lblCenterVal.place(x=70,y=600)

        # ------------Color H(스케일바)------------
        self.label_lh=tkinter.Label(window, text="L-H")
        self.label_lh.place(x=550,y=400)
        self.slider1 = tkinter.Scale(window, from_ = 0, to = 179, length=300,orient=tkinter.HORIZONTAL)
        self.slider1.place(x = 600, y = 380)

        self.label_uh=tkinter.Label(window, text="U-H")
        self.label_uh.place(x=550,y=450)
        self.slider11 = tkinter.Scale(window, from_ = 0, to = 179, length=300,orient=tkinter.HORIZONTAL)
        self.slider11.set(179)
        self.slider11.place(x = 600, y = 430)

        # ------------Color S(스케일바)------------
        self.label_ls=tkinter.Label(window, text="L-S")
        self.label_ls.place(x=550,y=500)
        self.slider2 = tkinter.Scale(window, from_ = 0, to = 255, length=300,orient=tkinter.HORIZONTAL)
        self.slider2.place(x = 600, y = 480)

        self.label_us=tkinter.Label(window, text="U-S")
        self.label_us.place(x=550,y=550)
        self.slider22 = tkinter.Scale(window, from_ = 0, to = 255, length=300,orient=tkinter.HORIZONTAL)
        self.slider22.set(255)
        self.slider22.place(x = 600, y = 530)

        # ------------Color V(스케일바)------------
        self.label_lv=tkinter.Label(window, text="L-V")
        self.label_lv.place(x=550,y=600)
        self.slider3 = tkinter.Scale(window, from_ = 0, to = 255, length=300,orient=tkinter.HORIZONTAL)
        self.slider3.place(x = 600, y = 580)

        self.label_uv=tkinter.Label(window, text="U-V")
        self.label_uv.place(x=550,y=650)
        self.slider33 = tkinter.Scale(window, from_ = 0, to = 255, length=300,orient=tkinter.HORIZONTAL)
        self.slider33.set(101)
        self.slider33.place(x = 600, y = 630)

        #self.vidStart=False 
        self.start_flag=False
        self.count=0
        self.start_time=0
        self.after_id=0
        self.elapsed_time_str=0

        self.index=0

        self.window.mainloop()

    def openFile(self):
        try:
            file=filedialog.askopenfile(mode="r",filetypes=[('Video Files',['*.mp4',"*.mov","*.wmv","*.avi","*.mkv","*.mpg","*.mpeg"])])
            print(file.name)
            
            if file is not None:
                self.filename=file.name
                self.cap=cv2.VideoCapture(self.filename)
                
                self.fps=0
                self.fps=self.cap.get(cv2.CAP_PROP_FPS)
                self.delay=round(1000.0/self.fps)
                #self.update()

                #self.vidStart=True
                self.index=0
                if self.start_flag:
                    self.window.after_cancel(self.after_id)
                    self.start_flag=False
                    self.elapsed_time_str=0

                self.time_list=[]
                self.area_list=[]
                self.height_list=[]
                self.width_list=[]

                self.measure()
        except AttributeError:
            pass

    def measure(self):
        try:
            _,frame=self.cap.read()
            frame=imutils.resize(frame,height=350,width=500)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            #H값 추출
            slival1=self.slider1.get()
            slival11=self.slider11.get()
            #S값 추출
            slival2=self.slider2.get()
            slival22=self.slider22.get()
            #V값 추출
            slival3=self.slider3.get()
            slival33=self.slider33.get()

            lower_color = np.array([slival1, slival2, slival3]) #하한 값 
            upper_color = np.array([slival11, slival22, slival33]) #상한 값

            mask = cv2.inRange(hsv, lower_color, upper_color)
            result = cv2.bitwise_and(frame, frame, mask=mask)
            cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                area = cv2.contourArea(c)
                if area > 500:

                    cv2.drawContours(frame, [c], -1, (0, 255, 200), 3)
                    
                    peri=cv2.arcLength(c,True)
                    approx=cv2.approxPolyDP(c,0.02*peri,True)
                    x,y,w,h=cv2.boundingRect(approx)
                    #print("높이:{}".format(h),"가로:{}".format(w))

                    M = cv2.moments(c)
                    self.cx = int(M["m10"] / M["m00"])
                    self.cy = int(M["m01"] / M["m00"])

                    cv2.circle(frame, (self.cx, self.cy), 7, (255, 255, 255), -1)
                    cv2.putText(frame, "Center", (self.cx-20, self.cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 1)

                    # print("area is ...", area)
                    # print("centroid is at..", self.cx, self.cy)

                    self.area_list.append(area)
                    self.height_list.append(h)
                    self.width_list.append(w)
                    self.time_list.append(self.elapsed_time_str)

                    self.value()

            im=Image.fromarray(frame)
            img=ImageTk.PhotoImage(image=im)

            self.lblVideo.configure(image=img)
            self.lblVideo.image=img
            self.timeFile()
            self.lblVideo.after(self.delay,self.measure)
        
        except cv2.error :
            self.stopFile() 
        except AttributeError:
            self.stopFile()

    def value(self):
        self.lblAreaVal.config(text=self.area_list[self.index])
        self.lblHeightVal.config(text=self.height_list[self.index])
        self.lblWidthVal.config(text=self.width_list[self.index])
        self.lblCenterVal.config(text="{}, {}".format(self.cx,self.cy))

        self.index+=1
    
    def stopFile(self):
        if self.start_flag:
            self.window.after_cancel(self.after_id)
            self.start_flag=False
            self.elapsed_time_str=0

        #self.vidStart=False
        self.cap.release()
        cv2.destroyAllWindows()

    def timeFile(self):
        if not self.start_flag:
            self.start_flag=True
            self.start_time=time.time()
            self.count=0
            self.after_id=self.window.after(10,self.update_time)

    def update_time(self):
        self.after_id=self.window.after(10,self.update_time)
        now_time=time.time()
        elapsed_time=now_time-self.start_time
        self.elapsed_time_str='{:.2f}'.format(elapsed_time)
        self.lblTimeVal.config(text=self.elapsed_time_str)
    
    def saveFile(self):
        outfilename=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[('CSV files','*.csv')])
        if outfilename:
            df=pd.DataFrame({'area':pd.Series(self.area_list), 'height':pd.Series(self.height_list),'width':pd.Series(self.width_list),'time':pd.Series(self.time_list)})
            df.to_csv(outfilename,index=False)

if __name__=="__main__":
    videoGUI(Tk(),"objectMeasurement")
    pass