#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:58:47 2020

@author: fairshare
"""

import tkinter as tk
from tkinter import filedialog
import ResumeParser

resumes = []
jd = []
def open_file():
    filety= [("text files", "*.txt")]
    filez = filedialog.askopenfilenames(parent=m,title='Choose resume',filetypes=filety)
    for i in filez:
        resumes.append(str(i))
    print (m.tk.splitlist(filez))

def open_jd():
    filety= [("text files", "*.txt")]
    filea = filedialog.askopenfilename(parent=m,title='Choose JD',filetypes=filety)
    jd.append(filea)
    
def call_parser():
    j = str(jd[0])
    for i in resumes:
        r = str(i)
        ResumeParser.main(j,r)
m = tk.Tk()

m.geometry("500x300+900+300")

m.title('Resume Picker') 
button = tk.Button(m, text='Stop', width=25, command=m.destroy) 
button.pack()

res_b = tk.Button(m, text='Upload Resumes', width=25, command = open_file) 
res_b.pack()
 
jd_b = tk.Button(m, text='Upload JD', width=25, command = open_jd) 
jd_b.pack()

call = tk.Button(m, text='Parse', width=25, command = call_parser) 
call.pack()


m.mainloop()