import os
import tkinter
from tkinter import font
from typing import Text

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pickle
import shutil
import threading
# GUI
from tkinter import (END, HORIZONTAL, Button, Entry, Label, Menu, StringVar,
                     Text, Tk, filedialog, messagebox, ttk)
from tkinter.font import Font

import cv2
import face_recognition
import PIL
import PIL.Image
import pymysql as mydb
from imutils import paths
from numpy.core.shape_base import block
from path import *
from PIL import Image, ImageTk
from pymysql.err import Error
from tensorflow import *

from Web_Camera import Video


class Login:
    def __init__(self) :
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x500+250+100")
        self.root.config(bg = "#021e2f")
        
          #background_image=tk.PhotoImage("shutter.png")
        self.img = ImageTk.PhotoImage(Image.open("shutter.jpg"))
        #=============Frames=============================
        login_frame = Label(self.root,bg="white",image=self.img)
        login_frame.place(x=0,y=0,width=800,height=500)

        title = Label(login_frame,text="LOGIN HERE", font=("Tahoma",15,"bold"),bg="white",fg="lightgray")
        
        self.email = Label(login_frame,text="Email Address",font=("Tahoma",15),bg="white",fg="black")
        self.email.place(x=80,y=115,width=350,height=35)
        self.txt_email=Entry(login_frame,font=("Tahoma ",10),bg="lightgray")
        self.txt_email.place(x=80,y=150,width=350,height=35)

        self.pass_=Label(login_frame,text="Password",font=("Tahoma ",15),bg="white",fg="black",)
        self.pass_.place(x=80,y=215,width=350,height=35)
        self.txt_pass = Entry(login_frame,show="*",font=("Tahoma ",10),bg="lightgray")
        self.txt_pass.place(x=80,y=250,width=350,height=35)
        
        self.btn_login=Button(login_frame,text="Login",font=("Tahoma ",15,"bold"),fg="pink",bg="green",command=self.login) 
        self.btn_login.place(x=80,y=305,width=350,height=35)

        self.btn_reg=Button(login_frame,cursor="hand2",text="Register Here",font=("Tahoma ",15,"bold"),fg="pink",bg="black",command=Register)
        self.btn_reg.place(x=80,y=350,width=350,height=35)
    
    def login(self):
        #get the data and store it into tuple (data)
        con = mydb.connect(host="localhost",user="root",passwd="",database="camera")
        data = (self.txt_email.get(),self.txt_pass.get())


        # validations
        if self.txt_email.get() == "":
            messagebox.showinfo("Alert!","Enter Email First")
        elif self.txt_pass.get() == "":
            messagebox.showinfo("Alert!", "Enter Password first")
        else:
            
                    #get the data and store it into tuple (data)
            con = mydb.connect(host="localhost",user="root",passwd="",database="camera")      
            cur = con.cursor()
            cur.execute("SELECT * FROM `users` WHERE `email`=%s AND `password`=%s",data)
            res = cur.fetchone()
            if res:
                messagebox.showinfo("Message", "Login Successfully")
                
                command =Main()
                
            else:
                        messagebox.showinfo("Alert!", "Wrong username/password")

class Register:
    
    def __init__(self) :
        self.root = root
        self.root.title("Register")
        self.root.geometry("800x500+250+100")
        self.root.config(bg = "#021e2f")
        self.img = ImageTk.PhotoImage(Image.open("shutter.jpg"))

        #=========Register Frame======
        frame1 = Label(self.root,bg="white",image=self.img)
        frame1.place(x=0,y=0,width=800,height=500)
        
        
        self.title=Label(frame1,text="REGISTER HERE",font=("Tahoma"),bg="white",fg="gray")
        self.title.place(x=250,y=50,width=350)
        #=====Row1  Email=====
        
        self.email=Label(frame1,text="Email Address",font=("Tahoma"),bg="white",fg="gray")
        self.email.place(x=250, y=115,width=350,height=35)
        self.txt_email=Entry(frame1,font=("Tahoma",15),bg="lightgray",fg="gray")
        self.txt_email.place(x=250,y=150,width=350,height=35)

         #=====Row2   First Name=====
        self.f_name=Label(frame1,text="First Name",font=("Tahoma"),bg="white",fg="gray")
        self.f_name.place(x=70,y=200,width=350,height=35)
        self.txt_fname=Entry(frame1,font=("Tahoma",15),bg="lightgray",fg="gray")
        self.txt_fname.place(x=70,y=235,width=350,height=35)
        
         #=====Row2   Last Name=====
        self.l_name=Label(frame1,text="Last Name",font=("Tahoma"),bg="white",fg="gray")
        self.l_name.place(x=440,y=200,width=350,height=35)
        self.txt_lname=Entry(frame1,font=("Tahoma",15),bg="lightgray",fg="gray")
        self.txt_lname.place(x=440,y=235,width=350,height=35)
       

       #self.txt_pass = Entry(login_frame,show="*",font=("Tahoma ",10),bg="lightgray")
        #=====Row3 password=====
        self.password=Label(frame1,text="Password",font=("Tahoma"),bg="white",fg="gray")
        self.password.place(x=70, y=280,width=350,height=35)
        self.txt_password=Entry(frame1,show="*",font=("Tahoma",15),bg="lightgray",fg="gray")
        self.txt_password.place(x=70,y=315,width=350,height=35)

        #=====Row3 confirm password=====
        self.cpassword=Label(frame1,text="Confirm Password",font=("Tahoma"),bg="white",fg="gray")
        self.cpassword.place(x=440, y=280,width=350,height=35)
        self.txt_cpassword=Entry(frame1,show="*",font=("Tahoma",15),bg="lightgray",fg="gray")
        self.txt_cpassword.place(x=440,y=315,width=350,height=35)

        self.btn_register=Button(frame1,text="Sign in", font=("Tahoma",15,"bold"),fg="pink",bg="green",bd=0,cursor="hand2",command=self.register_data)
        self.btn_register.place(x=250,y=400,width=350)
        
        
        
        #back to priveus page
        self.btn_back=Button(frame1,text="Back", font=("Tahoma",15,"bold"),fg="pink",bg="black",bd=0,cursor="hand2",command=Login)
        self.btn_back.place(x=70,y=400,width=100)
           
    def register_data(self):
        if self.txt_email.get()=="":
            messagebox.showerror("Error!", "Insert Email ",parent=self.root)
        elif self.txt_fname.get()=="":
            messagebox.showerror("Error!", "Insert First Name",parent=self.root)
        elif self.txt_lname.get()=="" :
            messagebox.showerror("Error!", "Insert Last Name",parent=self.root)
        elif self.txt_password.get()=="" :
            messagebox.showerror("Error!", "Insert Password",parent=self.root)
        elif self.txt_cpassword.get()=="":
            messagebox.showerror("Error!", "Insert Cofirm Password",parent=self.root)                
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error!", "Passwords Don't Match", parent=self.root)
        else:
            try:
                con=mydb.connect(host="localhost",user="root",passwd="",database="camera")
                cur=con.cursor()
                #check if email allready exist
                cur.execute("select * from users where email=%s",self.txt_email.get())
                row=cur.fetchone()
                if(row!=None):
                    messagebox.showerror("Error!", "Email Allready Exist")
                cur.execute("insert into users (f_name,l_name,email,password) values (%s,%s,%s,%s)",
                                (self.txt_fname.get(),
                                self.txt_lname.get(),
                                self.txt_email.get(),
                                self.txt_password.get()
                                ))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Register Success", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Error due to :{str(es)}",parent=self.root)   
            
            #clear all register fields 
            self.clear_fields()    
                            
        # clear all fields
    def clear_fields(self):
        self.txt_fname.delete(0,END)
        self.txt_lname.delete(0,END)
        self.txt_email.delete(0,END)
        self.txt_password.delete(0,END)
        self.txt_cpassword.delete(0,END)

##################################################

class Main:
    #constructor
    def __init__(self):
        self.root = root
        self.root.title("Face Recogntion")
        self.root.geometry("800x500+250+100")
        self.root.config(bg = "#021e2f")
        self.img = ImageTk.PhotoImage(Image.open("shutter.jpg"))
        self.label = Label(self.root,image=self.img)
        self.label.place(x=0,y=0,width=800,height=500)         
    
        self.creat_combox()
        self.Creat_Menu()
        self.label_frame = ttk.LabelFrame(self.root, text = "Add New Images")
        self.label_frame.grid(column=0, row=1, padx=20, pady=20)
        self.add_img_buton()
       
    def Click_Me(self):
        self.label.configure(text = "Selected :" + self.languages.get())
        if self.languages.get().__eq__("Mask Detctor"):
            #call to other Web_Camera class
            command=Video(vid_typ="Mask Detctor")
        elif self.languages.get().__eq__("Normal Camera"):
            #call to other Web_Camera class
            command=Video(vid_typ="Normal Camera")
        elif self.languages.get().__eq__("Face Recogntion"):
            #call to other Web_Camera class
            command=Video(vid_typ="Mask Detctor",face_recog=True)
        elif self.languages.get().__eq__("Train"):
            self.my_progress_bar=ttk.Progressbar(self.root, orient=HORIZONTAL,length=250,mode='determinate')
            self.my_progress_bar.grid(column=2,row=1)
            #this is using tkinter in a thread, but some tkinter methods are ok to use in threads
            t1 = threading.Thread(target = self.train_facerecogntion)
            t1.start()
            self.my_progress_bar.start()
             
    # creat combox
    def creat_combox(self):
        
        self.languages = StringVar()
        self.combobox = ttk.Combobox(self.root, width = 20, textvariable = self.languages)

        self.label = ttk.Label(self.root, text ="Select Camera Status")  
        self.label.grid(column = 1, row = 0)

        self.combobox['values'] = ("Normal Camera", "Mask Detctor", "Face Recogntion", "Train")
        self.combobox.grid(column = 2, row = 0)  

        self.button = ttk.Button(self.root, text = "Run", command = self.Click_Me)
        self.button.grid(column = 3, row = 0)

        #add new image to the dataset
    def add_img_buton(self):
        button = ttk.Button(self.label_frame, text = "Browse A File", command= self.file_dialog)
        #self.label.configure(text = "Selected :" + self.languages.get())
        button.grid(column=1,row=1) 
    def file_dialog(self):
        root = Tk()
        root.withdraw() #use to hide tkinter window
        # current dir path
        currdir = os.getcwd()
        # file name to copy to current directory
        file_name = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        label = ttk.Label(self.label_frame, text = "")
        label.grid(column=1, row=2)
        label.configure(text=file_name)    

        original = file_name
        target = os.getcwd() + '\DataSet'
        self.copytree(src=original,dst=target)    

        #train face reecognation
    def train_facerecogntion(self):   
        #get paths of each file in folder named Images
        #Images here contains my data(folders of various persons)
        imagePaths = list(paths.list_images(r"DataSet"))
        knownEncodings = []
        knownNames = []
            # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            name = imagePath.split(os.path.sep)[-2]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
    
            image = cv2.imread(imagePath)

            try:    
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except :
                print(imagePath,"not correct")    
                self.my_progress_bar.stop()
            #Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb,model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
            #save emcodings along with their names in dictionary data
        data = {"encodings": knownEncodings, "names": knownNames}
            #use pickle to save data into a file for later use
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()   
        self.my_progress_bar.stop()
        self.my_progress_bar.destroy()
        print("progress finished")

    def creat_directory(self,name:str, parent_dir:str):

        # Directory
        dir_name =  name
        # Parent Directory path or current dir path
        # Path
        path = os.path.join(parent_dir, dir_name)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)    

    # copy new directory to dist directory   
    def copytree(self, src, dst, symlinks=False, ignore=None):
        #creat new directory name the last part of path
        
        self.creat_directory(name=os.path.basename(os.path.normpath(src)),parent_dir=dst)

        # distnation is now the new directory
        dst = dst + "/" + os.path.basename(os.path.normpath(src))
        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(self, s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

        # creat menu bar
    def Creat_Menu(self):
            Menu_Bar = Menu(self.root)
            self.root.config(menu = Menu_Bar)
            
            file_menu = Menu(Menu_Bar, tearoff = 0)
            Menu_Bar.add_cascade(label = "File", menu = file_menu)
            #file_menu.add_command(label = "New")
            #exit
            file_menu.add_command(label = "Exit", command = self.window_close)
            file_menu.add_command(label = "Logout", command=Login)
            
            file_menu.add_separator()
            file_menu.add_command(label = "About",command=About)
    
        #close windows
    def window_close(self):
        self.root.destroy()
        exit()
    def App_Info(self):
        filename = "readme.txt"
        os.startfile(filename)
class About:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("About")
        self.root.geometry("800x500+250+100")
        # self.root.config(bg = "white")
        self.text_button = Text(self.root,height=800,width=500,bg="white",fg="black")
        self.label = Label(self.root,text="About")
        self.label.config(font=("Tahoma",20))
        fileObject = open('readme.txt', 'r')
        data = fileObject.read()
        self.back = Button(self.root,text="Exit",command=self.root.destroy)
        self.text_button.insert(END,data)
        self.back.pack()
        self.label.pack()
        self.text_button.pack()
        
        self.root.mainloop()
root = Tk()
obj = Login()
root.mainloop()
