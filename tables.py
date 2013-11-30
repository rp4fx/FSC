__author__ = 'roran_000'



import pymysql
#test
import random
from Tkinter import *
import base64
import os

def sql_string(str): #formats string so it doesn't cause errors
    return '"'+str+'"'

def encode(str):
    return base64.b64encode(str)

def decode(str):
    return base64.b64decode(str)

class user():
    def __init__(self,username,password,userType):
        self.username = username
        self.password = encode(password)
        self.userType = userType
    def __str__(self):
        return "Name: "+self.name + " self.username: " +self.username+" userType: "+self.userType
    def get_password(self):
        return decode(self.password)



class student():
    def __init__(self,name,SID,notification_number):#constructor
        self.name = sql_string(name)
        self.SID = SID
        self.notification_number=notification_number
    def __str__(self):#toString
        return self.name

class course():
    def __init__(self,courseID,section,semester,title,year,CID): #constructor
        self.courseID = sql_string(courseID)
        self.section = section
        self.semester = sql_string(semester)
        self.title = sql_string(title)
        self.year = year
        self.CID = CID
    def __str__(self):#toString
        return self.title

class professor():
    def __init__(self,name,PID,notification_number):#constructor
        self.name = sql_string(name)
        self.PID = PID
        self.notification_number = notification_number
    def __str__(self):#toString
        return self.name

class question():
    def __init__(self,content,date,QID):#constructor
        self.content = sql_string(content)
        self.date = sql_string(date)
        self.QID = QID
    def __str__(self):#toString
        return self.content

class response():
    def __init__(self,content,date,RID):
        self.content = sql_string(content)
        self.date = sql_string(date)
        self.RID = RID
    def __str__(self):
        return self.content

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def sql_injection_prevent(string):#works
       if ('\'' in string or '\"'):
            print 'Don\'t hack me'
            sys.exit()



def insert_student(cursor,s, db):
    cursor.execute("INSERT INTO student (name,SID,notification_number) VALUES (%s,%d,%d)"  %(s.name,s.SID,s.notification_number))
    db.commit()

def get_student(cursor,SID):
    cursor.execute("SELECT name,SID,notification_number FROM student WHERE SID =%d" % (SID))
    r = cursor.fetchone()
    return student(r[0],r[1],r[2])



def create_course(cursor,course,db):
    cursor.execute("INSERT INTO course (courseID,section,semester,title,year,CID) VALUES (%s,%d,%s,%s,%d,%d)" %(course.courseID,course.section,course.semester,course.title,course.year,course.CID)
    )
    db.commit()

def insert_professor(cursor,p,db):
    cursor.execute("INSERT INTO professor (name,PID,notification_number) VALUES (%s,%d,%d)" % (p.name,p.PID,p.notification_number))
    db.commit

def get_professor(cursor,PID):
    cursor.execute("SELECT name,PID,notification_number FROM professor WHERE PID =%d" % (PID))
    r = cursor.fetchone()
    return professor(r[0],r[1],r[2])

def get_classes(cursor,CID):
    cursor.execute("SELECT courseID, section,semester, title, year,CID FROM course WHERE CID =%d" % (CID))
    r = cursor.fetchone()
    return course(r[0],r[1],r[2],r[3],r[4],r[5])

def get_prof_class(cursor,c):
    cursor.execute("SELECT name FROM professor NATURAL JOIN course NATURAL JOIN teaches WHERE courseID = %s" %(c.courseID))
    for r in cursor:
        print r

def get_question(cursor,QID):
    cursor.execute("SELECT content,date,QID FROM question WHERE QID = %d" % (QID))
    r = cursor.fetchone()
    return question(r[0],r[1],r[2])

def get_response(cursor,QID):
    cursor.execute("SELECT content,date,QID FROM question WHERE QID = %d" % (QID))
    r = cursor.fetchone()
    return question(r[0],r[1],r[2])

def get_prof_notenum(cursor,p,):
    cursor.execute("SELECT notification_number from professor where PID = %d" % (p.PID))
    r = cursor.fetchone()
    return r[0]

def get_stud_notenum(cursor,s):
    cursor.execute("SELECT notification_number from student where SID = %d" % (s.SID))
    r = cursor.fetchone()
    return r[0]

def increment_prof(cursor,p,db):
    r = get_prof_notenum(cursor,p)
    r = r+1
    cursor.execute("UPDATE professor SET notification_number = %d WHERE PID = %d" % (r,p.PID))
    db.commit()

def increment_stud(cursor,s,db):
    r = get_stud_notenum(cursor,s)
    r=r+1
    cursor.execute("UPDATE student SET notification_number =%d WHERE SID = %d" %(r,s.SID))

def decrement_prof(cursor,p,db):
    r = get_prof_notenum(cursor,p)
    if(r>0):
        r = r-1
    cursor.execute("UPDATE professor SET notification_number = %d WHERE PID = %d" % (r,p.PID))
    db.commit()

def decrement_student(cursor,s,db):
    r = get_stud_notenum(cursor,s)
    if(r>0):
        r = r-1
    cursor.execute("UPDATE student SET notification_number =%d WHERE SID = %d" %(r,s.SID))

def ask_question(cursor,q,s,p,db):
    cursor.execute("INSERT INTO question (content,date,QID) VALUES (%s,%s,%d)" % (q.content,q.date,q.QID))
    db.commit()
    cursor.execute("INSERT INTO answers (PID,QID) VALUES (%d,%d)" % (p.PID,q.QID))
    db.commit()
    cursor.execute("INSERT INTO asks (SID,QID) VALUES (%d,%d)" %(s.SID,q.QID))
    db.commit()
    #cursor.execute("SELECT notification_number from professor where PID = %d" % (p.PID))
    #r = cursor.fetchone()
    #r = r[0]
    increment_prof(cursor,p,db)

def answer_question(cursor,r,s,p,db):
    cursor.execute("INSERT INTO responses (content,date,RID) VALUES (%s,%s,%d)" % (r.content,r.date,r.RID))
    db.commit()
    cursor.execute("INSERT INTO answered (PID,RID) VALUES (%d,%d)" % (p.PID,r.RID))
    db.commit()
    cursor.execute("INSERT INTO ansReceived (SID,RID) VALUES (%d,%d)" %(s.SID,r.RID))
    db.commit()
    #cursor.execute("SELECT notification_number from professor where PID = %d" % (p.PID))
    #r = cursor.fetchone()
    #r = r[0]
    decrement_prof(cursor,p,db)
    increment_stud(cursor,s,db)


def login(username,password,userType,cursor):
    cursor.execute("SELECT password,userType from userCred WHERE username = (%s)" % (username,userType))
    r = cursor.fetchone()
    if(password == decode(r[0])):
        print "logged in"

def signup(username,password,userType,):
    print "s"


def main():
    #root = Tk()
    #app = Application(master=root)
    #app.mainloop()
    #root.destroy()


    #create admin user who can edit course related tables
    db = pymysql.connect(host='128.143.71.84',
                     user='cs4750rp4fx',
                     passwd='yju6328.',
                     db='cs4750rp4fx',)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS userCred (username VARCHAR(50) UNIQUE,password VARCHAR(50), userType VARCHAR(50)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS studentuser (username VARCHAR (50),SID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS profuser (userhame VARCHAR (50), PID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS student  (name VARCHAR (50), SID INT UNIQUE,notification_number INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS course  (courseID VARCHAR(10), section INT, semester VARCHAR(6), title VARCHAR(50), year INT, CID INT unique)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS professor  (name VARCHAR(50), PID INT UNIQUE, notification_number INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS question  (content VARCHAR(250), date VARCHAR(50), QID INT)""")#changed
    #cursor.execute("""CREATE TABLE IF NOT EXISTS device  (ipAddress VARCHAR(50), type VARCHAR(50))""")
    #cursor.execute("""CREATE TABLE IF NOT EXISTS s_uses  (ipAddress VARCHAR(50), SID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS takes  (SID INT, courseID VARCHAR(10))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teaches  (PID INT, CID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS answers  (PID INT, QID INT)""")#changed
    cursor.execute("""CREATE TABLE IF NOT EXISTS asks  (SID INT, QID INT)""")#changed
    cursor.execute("""CREATE TABLE IF NOT EXISTS qcourse (CID INT,QID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS rcourse (CID INT,RID INT)""")
    #cursor.execute("""CREATE TABLE IF NOT EXISTS p_uses (PID INT, ipAddress VARCHAR(50))""")
    #created table for professors to respond to students
    cursor.execute("""CREATE TABLE IF NOT EXISTS responses (content VARCHAR(250),date VARCHAR(50), RID INT UNIQUE)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS answered(PID INT,RID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ansReceived(SID INT,RID INT)""")
    q = question("hello",'2013-11-11',1)
    s = get_student(cursor,1)
    p = get_professor(cursor,12)
    r = response('hi','2013-11-27',1)
    #ask_question(cursor,q,s,p,db)
    #answer_question(cursor,r,s,p,db)
    c = get_classes(cursor,6)
    print c
    get_prof_class(cursor,c)
if __name__ == "__main__":
    main()