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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        

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

        for F in (LogIn, SignUp, CompanyView,GraphView):

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
        label.grid(row=1,column=3)
        
        n = tk.Label(self ,text = "First Name")
        n.grid(row=3,column =2 )
        name = tk.Entry(self)
        name.grid(row=3,column=3)
        pswrd = tk.Label(self ,text = "Password")
        pswrd.grid(row=5,column=2)
        
        password = tk.Entry(self)
        password.grid(row=5,column=3)
        
        login_b = tk.Button(self, text="Log In",
                            command=lambda: self.login(name.get(),password.get(),controller))
        login_b.grid(row=10,column=2)
        button = tk.Button(self, text="Sign Up",
                            command=lambda: controller.show_frame(SignUp))
        button.grid(row=10,column=4)
    def login(self,name,password,controller):
        print(name,password) 
        if (name == "indira" and password == "test123"):
            controller.show_frame(CompanyView)
        else:
            print("OK")

       

class SignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sign Up", font=LARGE_FONT)
        label.grid(row=1,column=3)

        n = tk.Label(self ,text = "First Name")
        n.grid(row=2,column=1)
        name = tk.Entry(self)
        name.grid(row=2,column=3)
        pswrd = tk.Label(self ,text = "Password")
        pswrd.grid(row=4,column=1)
        password = tk.Entry(self)
        password.grid(row=4,column=3)
        
        signup_b = tk.Button(self, text="Sign Up",
                            command=lambda: self.signup(name.get(),password.get()))
        signup_b.grid(row=8,column=2)
        button1 = tk.Button(self, text="Back to Log In",
                            command=lambda: controller.show_frame(LogIn))
        button1.grid(row=9,column=2)

        #button2 = tk.Button(self, text="Page Two",
                           # command=lambda: controller.show_frame(PageTwo))
        #button2.pack()
    def signup(self,name,password):
        print(name,password)


class CompanyView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="CV Analysis", font=LARGE_FONT)
        label.grid(row=0,column=2)

        #self.geometry("500x300+900+300")
        
        button = tk.Button(self, text='Stop', width=25, command=self.destroy) 
        button.grid(row=1,column=2)
        
        res_b = tk.Button(self, text='Upload Resumes', width=25, command = self.open_file) 
        res_b.grid(row=3,column=2)
         
        jd_b = tk.Button(self, text='Upload JD', width=25, command = self.open_jd) 
        jd_b.grid(row=4,column=2)
        
        call = tk.Button(self, text='Parse', width=25, command = self.call_parser) 
        call.grid(row=5,column=2)
        
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(LogIn))
        button1.grid(row=6,column=2)

        button2 = tk.Button(self, text="Show Graph",
                            command=lambda: controller.show_frame(GraphView))
        button2.grid(row=7,column=2)
        
    
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
        resumes.clear()

class GraphView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph of Resume Similarities", font=LARGE_FONT)
        label.grid(row=1, column = 2)
        button1 = tk.Button(self, text="Back", command=lambda: controller.show_frame(CompanyView))
        button1.grid(row=10,column = 2)
        button1 = tk.Button(self, text="Plot", command=self.plot_gr)
        button1.grid(row=9,column = 2)
        
        
    def plot_gr(self):
        data = pd.read_csv("similarities.csv")
        df1 = pd.DataFrame(data)
        short = []
        sum_ = []
        long = list(data.filename)
        for i in long:
            i = i.split("/")
            short.append(i[-1])
        leng = len(data)
        df1.insert(1,"short_file",short)
        for k in range(leng):
            sum_.append((df1.hardskill[k] + df1.softskill[k] + df1.general[k])/3)
        df1.insert(2,"Average", sum_) 
        figure1 = plt.Figure(figsize=(7,7), dpi=100)
        ax1 = figure1.add_subplot(221)
        ax2 = figure1.add_subplot(222)
        ax3 = figure1.add_subplot(223)
        ax4 = figure1.add_subplot(224)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().grid(row = 4, column = 3)
        df1.plot(x='short_file', y='hardskill', kind='bar',legend=True,ax=ax1)
        df1.plot(x='short_file', y='softskill', kind='bar',legend=True,ax=ax2)
        df1.plot(x='short_file', y='general', kind='bar',legend=True,ax=ax3)
        df1.plot(x='short_file', y='Average', kind='bar',legend=True,ax=ax4)
        ax1.set_title('Resumes')
	

app = Control()
app.title('Resume Picker') 
#app.geometry("300x120+900+300")
app.mainloop()
