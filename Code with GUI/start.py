LARGE_FONT= ("Verdana", 12)

import tkinter as tk
from tkinter import filedialog,messagebox
import ResumeParser

import MySQLdb as mdb
global conn, cur
conn=mdb.connect('localhost','user','password','Career')
cur=conn.cursor()
curr=conn.cursor()

#resumes = []
#jd = []
class Control(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LogIn, SignUp, CompanyView, NewJD, ResultCandidate, CandidateView, NewCV, ResultCompany):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        parser()
        self.show_frame(LogIn)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Log In ", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        usernameLabel = tk.Label(self ,text = "Username")
        usernameLabel.pack()
        username = tk.Entry(self)
        username.pack()
        
        passwordLabel = tk.Label(self ,text = "Password")
        passwordLabel.pack()
        
        password = tk.Entry(self)
        password.pack()
        
        login_b = tk.Button(self, text="Log In",
                            command=lambda: self.login(username.get(),password.get(),controller))
        login_b.pack()

        button = tk.Button(self, text="Sign Up",
                            command=lambda: controller.show_frame(SignUp))
        button.pack()


    def login(self,username,password,controller):
        cur.execute("SELECT type from user where username='%s' and password='%s'" % (username,password))
        result=cur.fetchone()
        if(result[0]=='C'):
            controller.show_frame(CompanyView)
        elif(result[0]=='U'):
            controller.show_frame(CandidateView)

       

class SignUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sign Up", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        nameLabel = tk.Label(self ,text = "Username")
        nameLabel.pack()
        username = tk.Entry(self)
        username.pack()

        passwordLabel = tk.Label(self ,text = "Password")
        passwordLabel.pack()
        password = tk.Entry(self)
        password.pack()
        
        type_v = tk.StringVar() 
        
        r1 = tk.Radiobutton(self, text='Company', variable=type_v, value="C") 
        r2 = tk.Radiobutton(self, text='Candidate', variable=type_v, value="U")
        r1.pack()
        r2.pack()
        
        signup_b = tk.Button(self, text="Sign Up",
                            command=lambda: self.signUp(username.get(),password.get(),type_v.get()))
        signup_b.pack()

        back_login = tk.Button(self, text="Back to Log In",
                            command=lambda: controller.show_frame(LogIn))
        back_login.pack()

    def signUp(self,username,password,type_v):
        #print(username)
        #print(password)
        #print(type_v)
        cur.execute("INSERT into user(username,password,type) VALUES('%s','%s','%s')"%(username,password,type_v))
        conn.commit()
        messagebox.showinfo("Registration","You have been successfully registered")
        

class CompanyView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Company Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Stop', width=25, command=self.destroy) 
        button.pack()        
        
        jd_b = tk.Button(self, text='Add New Job', width=25, command = lambda : self.openNewJD(controller)) 
        jd_b.pack()

        view = tk.Button(self, text='View Candidates', width=25, command = lambda : self.openResultCandidate(controller)) 
        view.pack()

        button1 = tk.Button(self, text="Logout", command=lambda: controller.show_frame(LogIn))
        button1.pack()

    def openNewJD(self,controller):
        controller.show_frame(NewJD)

    def openResultCandidate(self,controller):
        controller.show_frame(ResultCandidate)

        
class NewJD(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add New JD ", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        companyNameLabel = tk.Label(self ,text = "Company Name")
        companyNameLabel.pack()
        companyName = tk.Entry(self)
        companyName.pack()
        
        jobNameLabel = tk.Label(self ,text = "Job Name")
        jobNameLabel.pack()
        
        jobName = tk.Entry(self)
        jobName.pack()

        jd_b = tk.Button(self, text='Upload New JD', width=25, command = lambda : self.upload(companyName.get(),jobName.get(),controller)) 
        jd_b.pack()

        back_login = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(CompanyView))
        back_login.pack()
               
    def upload(self,company,job_name,controller):
        filety= [("text files", "*.txt")]
        filea = filedialog.askopenfilename(parent=self,title='Choose JD',filetypes=filety)
        jd=filea.split("/")
        cur.execute("INSERT into jobs(job_name,company,jd) VALUES('%s','%s','%s')"%(job_name,company,jd[-1]))
        conn.commit()
        parser()
        if messagebox.askyesno("Upload JD","Thank you for uploading a new jd. Would you like to go back to Home Page?"):
            controller.show_frame(CompanyView)


class ResultCandidate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="View Candidates", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        companyNameLabel = tk.Label(self ,text = "Comapny Name")
        companyNameLabel.pack()
        companyName = tk.Entry(self)
        companyName.pack()
        
        jobNameLabel = tk.Label(self ,text = "Job Name")
        jobNameLabel.pack()
        
        jobName = tk.Entry(self)
        jobName.pack()

        displayLabel = tk.Label(self ,text = "")
        displayLabel.pack()

        view = tk.Button(self, text='View', width=25, command = lambda : self.view_candidate(companyName.get(),jobName.get())) 
        view.pack()

        back = tk.Button(self, text="Back to Home", command = lambda: controller.show_frame(CompanyView))
        back.pack()
               
    def view_candidate(self,company,job_name):
        print("\n\nJob Name : {0}\nCompany Name : {1}\n\n".format(job_name,company))
        cur.execute("SELECT job_id from jobs where job_name='%s' and company='%s'"%(job_name,company))
        job_id=cur.fetchone()
        conn.commit()
        #print(job_id[0])
        job=int(job_id[0])
        cur.execute("SELECT candidate from fit where job='%s' ORDER BY score desc " %(job))
        candidates=cur.fetchall()
        for candidate in candidates:
            cur.execute("SELECT name,email from candidate where username='%s'"%(candidate))
            result=cur.fetchall()
            for res in result:
                print("Candidate Name : {0}\nCandidate Email : {1}\n\n".format(res[0],res[1]))
                #displayLabel["text"]="Name : {0}\nEmail : {1}\n\n".format(res[0],res[1])

class CandidateView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Candidate Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Stop', width=25, command=self.destroy) 
        button.pack()        
        
        jd_b = tk.Button(self, text='Add New Resume', width=25, command = lambda : self.openNewCV(controller)) 
        jd_b.pack()

        view = tk.Button(self, text='View Companies', width=25, command = lambda : self.openResultCompany(controller)) 
        view.pack()

        button1 = tk.Button(self, text="Logout", command=lambda: controller.show_frame(LogIn))
        button1.pack()

    def openNewCV(self,controller):
        controller.show_frame(NewCV)

    def openResultCompany(self,controller):
        controller.show_frame(ResultCompany)

        
class NewCV(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add New CV", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        UsernameLabel = tk.Label(self ,text = "Username")
        UsernameLabel.pack()
        Username = tk.Entry(self)
        Username.pack()
        
        NameLabel = tk.Label(self ,text = "Name")
        NameLabel.pack()
        Name = tk.Entry(self)
        Name.pack()

        EmailLabel = tk.Label(self ,text = "Email")
        EmailLabel.pack()
        Email = tk.Entry(self)
        Email.pack()

        jd_b = tk.Button(self, text='Upload New CV', width=25, command = lambda : self.upload(Username.get(),Name.get(),Email.get(),controller)) 
        jd_b.pack()

        back = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(CompanyView))
        back.pack()
               
    def upload(self,username,name,email,controller):
        filety= [("text files", "*.txt")]
        filea = filedialog.askopenfilename(parent=self,title='Choose JD',filetypes=filety)
        cv=filea.split("/")
        cur.execute("INSERT into candidate(username,name,email,resume) VALUES('%s','%s','%s','%s')"%(username,name,email,cv[-1]))
        conn.commit()
        parser()
        if messagebox.askyesno("Upload CV","Thank you for uploading CV. Would you like to go back to Home Page?"):
            controller.show_frame(CandidateView)


class ResultCompany(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="View Companies", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        UsernameLabel = tk.Label(self ,text = "Username")
        UsernameLabel.pack()
        Username = tk.Entry(self)
        Username.pack()


        displayLabel = tk.Label(self ,text = "")
        displayLabel.pack()

        view = tk.Button(self, text='View', width=25, command = lambda : self.view_company(Username.get())) 
        view.pack()

        back = tk.Button(self, text="Back to Home", command = lambda: controller.show_frame(CompanyView))
        back.pack()
               
    def view_company(self,username):
        #print(username)
        print(" For Candidate : {0}".format(username))
        conn.commit()
        cur.execute("SELECT job from fit where candidate='%s' ORDER BY score desc" %(username))
        jobs=cur.fetchall()
        #print(jobs)
        for job in jobs:
            cur.execute("SELECT job_name,company from jobs where job_id='%s'"%(job))
            result=cur.fetchall()
            for res in result:
                print("Job Name : {0}\nCompany Name : {0}\n\n".format(res[0],res[1]))
                #displayLabel["text"]="Name : {0}\nEmail : {1}\n\n".format(res[0],res[1])

def parser():
    cur.execute("DELETE from fit")
    conn.commit()
    cur.execute("SELECT job_id,jd from jobs")
    jds=cur.fetchall()
    cur.execute("SELECT username,resume from candidate")
    resumes=cur.fetchall()
    for jd in jds:
        jd_name="Jds/"+str(jd[1])
        job_id=str(jd[0])
        for resume in resumes:
            resume_name = "Resumes/"+str(resume[1])
            resume_id=str(resume[0])
            ResumeParser.main(job_id,resume_id,jd_name,resume_name)


app = Control()
app.title('Resume Picker') 
app.geometry("500x300+900+300")
app.mainloop()
