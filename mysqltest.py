from datetime import *
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

import pymysql as mydb
from path import *
from PIL import Image, ImageDraw, ImageTk


class Login_Window:
    def __init__(self,root) :
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x500+250+100")
        self.root.config(bg = "#021e2f")
        
          #background_image=tk.PhotoImage("shutter.png")
        self.img = ImageTk.PhotoImage(Image.open("shutter.png"))
        # self.label = Label(self.root,image=self.img)
        # self.label.place(x=0, y=0)
        
        #============Background Color==================
        #bg = PhotoImage(file = "facial-recognition-.png")
        
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
                self.win.destroy()
            else:
                        messagebox.showinfo("ALert!", "Wrong username/password")

class Register:
    
    def __init__(self) :
        self.root = root
        self.root.title("Register")
        self.root.geometry("800x500+250+100")
        self.root.config(bg = "#021e2f")
        self.img = ImageTk.PhotoImage(Image.open("shutter.png"))

        #=========Register Frame======
        frame1 = Label(self.root,bg="white",image=self.img)
        frame1.place(x=0,y=0,width=800,height=500)
        
        title=Label(frame1,text="REGISTER HERE",font=("Tahoma",20,"bold"),bg="white",fg="pink")

        #=====Row1=====
        
        self.f_name=Label(frame1,text="First Name",font=("Tahoma",15),bg="white",fg="black")
        self.f_name.place(x=80,y=115,width=350,height=35)
        self.txt_fname=Entry(frame1,font=("Tahoma",15),bg="white",fg="black")
        self.txt_fname.place(x=80,y=150,width=350,height=35)
        
        self.l_name=Label(frame1,text="Last Name",font=("Tahoma",15,"bold"),bg="white",fg="black")
        self.f_name.place(x=80,y=115,width=375,height=35)
        self.txt_lname=Entry(frame1,font=("Tahoma",15),bg="white")
        self.txt_lname.place(x=80,y=150,width=425,height=35)
        #=====Row2=====
        self.email=Label(frame1,text="Email Address",font=("Tahoma",15,"bold"),bg="white",fg="pink")
        self.txt_email=Entry(frame1,font=("Tahoma",15),bg="white")
        self.txt_email.place(x=80,y=185,width=350,height=35)
        #=====Row3=====
        self.password=Label(frame1,text="Password",font=("Tahoma",15,"bold"),bg="white",fg="pink")
        self.txt_password=Entry(frame1,font=("Tahoma",15),bg="pink")

        self.cpassword==Label(frame1,text="Confirm Password",font=("Tahoma",15,"bold"),bg="white",fg="pink")
        self.txt_cpassword=Entry(frame1,font=("Tahoma",15),bg="pink")

        self.btn_register=Button(frame1,text="Sign in", font=("Tahoma",20),bd=0,cursor="hand2",command=self.register_data).place(x=50,y=420)

    def register_data(self):
        print(self.var_fname.get()
        ,self.txt_lname.get()
        ,self.txt_email.get()
        ,self.txt_password.get()
        ,self.txt_cpassword.get())







root = Tk()
obj = Login_Window(root)
root.mainloop()
