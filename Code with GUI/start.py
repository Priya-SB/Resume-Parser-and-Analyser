#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:09:54 2020

@author: fairshare
"""


LARGE_FONT= ("Verdana", 12)

import tkinter as tk
from tkinter import filedialog
import ResumeParser

resumes = []
jd = []
class Control(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LogIn, SignUp, CompanyView):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogIn)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Log In ", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        n = tk.Label(self ,text = "First Name")
        n.pack()
        name = tk.Entry(self)
        name.pack()
        pswrd = tk.Label(self ,text = "Password")
        pswrd.pack()
        
        password = tk.Entry(self)
        password.pack()
        
        v = tk.StringVar() 
        
        r1 = tk.Radiobutton(self, text='Company', variable=v, value="company") 
        r2 = tk.Radiobutton(self, text='Candidate', variable=v, value="candidate")
        r1.pack()
        r2.pack()
        login_b = tk.Button(self, text="Log In",
                            command=lambda: self.login(name.get(),password.get(),v.get(),controller))
        login_b.pack()
        button = tk.Button(self, text="Sign Up",
                            command=lambda: controller.show_frame(SignUp))
        button.pack()
    def login(self,name,password,v,controller):
        
        if (name == "indira" and password == "test123"):
            controller.show_frame(CompanyView)
        else:
            print("OK")

       

class SignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sign Up", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        n = tk.Label(self ,text = "First Name")
        n.pack()
        name = tk.Entry(self)
        name.pack()
        pswrd = tk.Label(self ,text = "Password")
        pswrd.pack()
        password = tk.Entry(self)
        password.pack()
        
        v = tk.StringVar() 
        
        r1 = tk.Radiobutton(self, text='Company', variable=v, value="company") 
        r2 = tk.Radiobutton(self, text='Candidate', variable=v, value="candidate")
        r1.pack()
        r2.pack()
        
        signup_b = tk.Button(self, text="Sign Up",
                            command=lambda: self.signup(name.get(),password.get(),v.get()))
        signup_b.pack()
        button1 = tk.Button(self, text="Back to Log In",
                            command=lambda: controller.show_frame(LogIn))
        button1.pack()

        #button2 = tk.Button(self, text="Page Two",
                           # command=lambda: controller.show_frame(PageTwo))
        #button2.pack()
    def signup(self,name,password,type_v):
        print(name,password,type_v)


class CompanyView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="CV Analysis", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #self.geometry("500x300+900+300")
        
        button = tk.Button(self, text='Stop', width=25, command=self.destroy) 
        button.pack()        
        
        res_b = tk.Button(self, text='Upload Resumes', width=25, command = self.open_file) 
        res_b.pack()
         
        jd_b = tk.Button(self, text='Upload JD', width=25, command = self.open_jd) 
        jd_b.pack()
        
        call = tk.Button(self, text='Parse', width=25, command = self.call_parser) 
        call.pack()
        
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(LogIn))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(SignUp))
        button2.pack()
        
    
    def open_file(self):
        filety= [("text files", "*.txt")]
        filez = filedialog.askopenfilenames(parent=self,title='Choose resume',filetypes=filety)
        for i in filez:
            resumes.append(str(i))
        print (self.tk.splitlist(filez))
    
    def open_jd(self):
        filety= [("text files", "*.txt")]
        filea = filedialog.askopenfilename(parent=self,title='Choose JD',filetypes=filety)
        jd.append(filea)
        
    def call_parser(self):
        j = str(jd[0])
        for i in resumes:
            r = str(i)
            ResumeParser.main(j,r)
        

app = Control()
app.title('Resume Picker') 
app.geometry("500x300+900+300")
app.mainloop()
