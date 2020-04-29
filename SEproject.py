from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import sqlite3
import ctypes

dbfile = sqlite3.connect("student.db")
dbcursor = dbfile.cursor()

from Admin_StudentWindows import *

class LoginWindow:

    def __init__(self, master):
        frame = Frame(master, bg="LIGHTCORAL",width=500, height=450)
        frame.pack()

        self.usernameLabel = Label(frame, text= "Username:",bg="LIGHTCORAL")
        self.usernameLabel.grid(row=0, sticky=E)
        self.usernameEntry= Entry(frame)
        self.usernameEntry.grid(row=0,column=1)
        self.usernameEntry.bind("<Return>",self.loginEnterKey)

        self.passwordLabel = Label(frame, text= "Password:",bg="LIGHTCORAL")
        self.passwordLabel.grid(row=1, sticky=E)
        self.passwordEntry = Entry(frame,show='*')
        self.passwordEntry.grid(row=1,column=1)
        self.passwordEntry.bind("<Return>",self.loginEnterKey)

        self.loginButton = Button(frame, text = "Login", command= self.loginButton)
        self.loginButton.grid(row=3,column=1)

    def loginButton(self):
        print("Logging in")
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        with sqlite3.connect("student.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE id= ? AND password = ?")      #from users table in student.db
        cursor.execute(findUser,[(username),(password)])
        results = cursor.fetchall()                                     #username: "s1", password:"p1", access:"student"

        if results:                                                     #username: "Chang", password:"password", access:"admin"
            for i in results:
                if i[2] == "student":
                    print("Student Login")
                    studentWindow = StudentWindow(Tk(),username,password)
                elif i[2] == "admin":
                    print("Admin Login")
                    adminWindow = AdminWindow(Tk(),username,password)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Invalid login please try again", "Message", 0)


    def loginEnterKey(self,event):
        print("Logging in")
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        with sqlite3.connect("student.db") as db:
            cursor = db.cursor()
        findUser = ("SELECT * FROM users WHERE id= ? AND password = ?")      #from users table in student.db
        cursor.execute(findUser,[(username),(password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                if i[2] == "student":
                    print("Student Login")
                    studentWindow = StudentWindow(Tk(),username,password)
                elif i[2] == "admin":
                    print("Admin Login")
                    adminWindow = AdminWindow(Tk(),username,password)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Invalid login please try again", "Message", 0)


def main():

    root = Tk()
    root.title("GatorsConnect")
    root.geometry("420x600")
    root.configure(bg="INDIANRED")
    Label(bg="INDIANRED").pack()
    Label(bg="INDIANRED").pack()
    Label(bg="INDIANRED").pack()


    Label(bg="INDIANRED").pack()
    Label(bg="INDIANRED").pack()
    Label(bg="INDIANRED").pack()
    Label(bg="INDIANRED").pack()
    login = LoginWindow(root)
    root.mainloop()



if __name__ == "__main__":
    main()
