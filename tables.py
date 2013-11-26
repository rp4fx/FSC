__author__ = 'roran_000'



import pymysql
import random
from Tkinter import *


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

def enroll(cursor):
    cursor.execute("SELECT SID from student")
    studentList = cursor.fetchall()
    cursor.execute("SELECT CID from course")
    courseList = cursor.fetchall()
    courseList = list(courseList)
    courseList = [i[0] for i in courseList]
    studentList = [i[0] for i in studentList]
    print courseList
    print studentList
    for s in studentList:
        random.shuffle(courseList)

        for x in range(4):
            entry = (str(s),str(courseList[x]))
            cursor.execute("INSERT INTO takes (SID,CID) VALUES (?,?)",entry)





def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

    db = pymysql.connect(host='128.143.71.84',
                     user='cs4750rp4fx',
                     passwd='yju6328.',
                     db='cs4750rp4fx',)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS student  (name VARCHAR (50), SID INT UNIQUE)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS course  (courseID VARCHAR(10), section INT, semester VARCHAR(6), title VARCHAR(50), year INT, CID INT unique)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS professor  (name VARCHAR(50), PID INT UNIQUE, notification_number INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS question  (content VARCHAR(250), date TIMESTAMP, SID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS device  (ipAddress VARCHAR(50), type VARCHAR(50))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS s_uses  (ipAddress VARCHAR(50), SID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS takes  (SID INT, courseID VARCHAR(10))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teaches  (PID INT, CID INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS answers  (PID INT, content VARCHAR(250))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS asks  (SID INT, content VARCHAR(250))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS p_uses (PID INT, ipAddress VARCHAR(50))""")
    #enroll(cursor)



if __name__ == "__main__":
    main()