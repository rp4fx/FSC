__author__ = 'roran_000'



import pymysql
#import cymysql
import random
from Tkinter import *
import base64

def sql_string(str): #formats string so it doesn't cause errors
    return '"'+str+'"'
class student():
    def __init__(self,name,SID):#constructor
        self.name = sql_string(name)
        self.SID = SID
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
        self.date = date
        self.QID = QID
    def __str__(self):#toString
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


def insert_student(cursor,s, db):
    cursor.execute("INSERT INTO student (name,SID) VALUES (%s,%d)"  %(s.name,s.SID))
    db.commit()




def create_course(cursor,course,db):
    cursor.execute("INSERT INTO course (courseID,section,semester,title,year,CID) VALUES (%s,%d,%s,%s,%d,%d)" %(course.courseID,course.section,course.semester,course.title,course.year,course.CID)
    )
    db.commit()

def insert_professor(cursor,p,db):
    cursor.execute("INSERT INTO professor (name,PID,notification_number) VALUES (%s,%d,%d)" % (p.name,p.PID,p.notification_number))
    db.commit

def ask_question(cursor,q,s,p,db):
    cursor.execute("INSERT INTO question (content,date,QID) VALUES (%s,%s,%d)") % (q.content,q.date,q.QID)
    db.commit()
    cursor.execute("INSERT INTO answers (PID,QID) VALUES (%d,%d)" % (p.PID,q.QID))
    db.commit()
    cursor.execute("INSERT INTO asks (SID,QID) VALUES (%d,%d)" %(s.SID,q.QID))
    db.commit()
    cursor.execute("SELECT notification_number from professor where PID = %d)" % (p.PID))
    r = cursor.fetchone()
    r = r+1
    cursor.execute("UPDATE professor SET notification_number = %d" % (r))



def main():
    #root = Tk()
    #app = Application(master=root)
    #app.mainloop()
    #root.destroy()

    db = pymysql.connect(host='128.143.71.84',
                     user='cs4750rp4fx',
                     passwd='yju6328.',
                     db='cs4750rp4fx',)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS student  (name VARCHAR (50), SID INT UNIQUE)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS course  (courseID VARCHAR(10), section INT, semester VARCHAR(6), title VARCHAR(50), year INT, CID INT unique)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS professor  (name VARCHAR(50), PID INT UNIQUE, notification_number INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS question  (content VARCHAR(250), date TIMESTAMP, QID INT)""")#changed
    cursor.execute("""CREATE TABLE IF NOT EXISTS device  (ipAddress VARCHAR(50), type VARCHAR(50))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS s_uses  (ipAddress VARCHAR(50), SID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS takes  (SID INT, courseID VARCHAR(10))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teaches  (PID INT, CID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS answers  (PID INT, QID INT)""")#changed
    cursor.execute("""CREATE TABLE IF NOT EXISTS asks  (SID INT, QID INT)""")#changed
    cursor.execute("""CREATE TABLE IF NOT EXISTS p_uses (PID INT, ipAddress VARCHAR(50))""")
    #enroll(cursor)
    #make question table strong entity
    #insert_student(cursor,'john doe',36,db)
   # c = course("cs4200",1,"fall","What is sleep",2013,12)
    #create_course(cursor,c,db)
if __name__ == "__main__":
    main()