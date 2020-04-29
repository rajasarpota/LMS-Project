from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import sqlite3
import ctypes

dbfile = sqlite3.connect("student.db")
dbcursor = dbfile.cursor()


class User():

    user_id = ""
    user_pass = ""

    def admin_set_id(self,u_id):
        User.user_id = u_id

    def admin_set_pass(self,u_pass):
        User.user_pass = u_pass

    def admin_get_id(self):
        return User.user_id

    def admin_user_pass(self):
        return User.user_pass

    def admin_assignments(self,s_id,c_id):
        dbcursor.execute("SELECT * FROM grades WHERE student_id= ? AND course_id = ?",(s_id,c_id))
        dbfile.commit()
        results = dbcursor.fetchall()
        assignments=[]
        print(results)
        for i in range(len(results)):
            assignments.append(results[i][3])
        return assignments

    def admin_grades(self,s_id,c_id):
        dbcursor.execute("SELECT * FROM grades WHERE student_id= ? AND course_id = ?",(s_id,c_id))
        dbfile.commit()
        results = dbcursor.fetchall()
        course_grades=[]
        print(results)
        for i in range(len(results)):
            course_grades.append(results[i][2])
        return course_grades

    def admin_course_list(self,s_id):
        dbcursor.execute("SELECT * FROM enrollment WHERE student_id= ?",(s_id,))
        dbfile.commit()
        results = dbcursor.fetchall()
        course_list=[]
        print(results)
        for i in range(len(results)):
            course_list.append(results[i][1])
        return course_list

    def admin_select_grades(self,s_id,c_id):
        dbcursor.execute("SELECT * FROM grades WHERE student_id= ? AND course_id = ?",(s_id,c_id))
        dbfile.commit()
        results = dbcursor.fetchall()
        return results

    def admin_show_courses(self,s_id):
        dbcursor.execute("SELECT * FROM enrollment WHERE student_id= ?",(s_id,))
        dbfile.commit()
        results = dbcursor.fetchall()
        return results

    def offered_courses(self):
        dbcursor.execute("SELECT * FROM courses")
        dbfile.commit()
        results = dbcursor.fetchall()
        return results

    def select_student(self):
        dbcursor.execute("SELECT * FROM students")
        dbfile.commit()
        result = dbcursor.fetchall()
        return results



class AdminWindow(User):

    student_id = ""
    course_id = ""


    def __init__(self,master,a_id,a_pass):

        master.geometry("380x400")
        master.title("GatorsConnect-"+a_id+"(Admin)")
        master.configure(bg="DARKCYAN")
        frame = Frame(master,bg="DARKCYAN",width = 500,height = 100)  #

        frame.place(relx = 0.5, y=2, anchor = N)

        self.admin_set_id(a_id)
        self.admin_set_pass(a_pass)

        self.blank_label = Label(frame,bg='DARKCYAN').grid(row=0)



        self.searchEntry = Entry(frame)
        self.searchEntry.grid(row=5,column=1,sticky='w')
        self.searchStudentButton = Button(frame,text="Search ID",command=lambda:self.search_id(frame))
        self.searchStudentButton.grid(row=5,column=2,sticky='e')

        self.blank_label = Label(frame,bg='DARKCYAN').grid(row=8)

        self.addStudentButton = Button(frame, text="Add a student", command=lambda: self.add_student_window())
        self.addStudentButton.grid(row=10, column=1, sticky='e')

        self.blank_label = Label(frame, bg='DARKCYAN').grid(row=11)

        self.add_course_button = Button(frame, text="Add a course", command=lambda: self.add_course_window())
        self.add_course_button.grid(row=13, column=1, sticky='e')

        self.blank_label = Label(frame, bg='DARKCYAN').grid(row=14)

        self.remove_course_button = Button(frame, text="Remove a course", command=lambda: self.remove_course_window())

        self.logoutButton = Button(frame, text="Exit",width = 11,command=lambda: master.destroy())
        self.logoutButton.grid(row=20,column=1,sticky='e')

    def set_course_id(self,c_id):
        AdminWindow.course_id = c_id

    def get_course_id(self):
        return AdminWindow.course_id

    def set_student_id(self,s_id):
        AdminWindow.student_id = s_id

    def get_student_id(self):
        return AdminWindow.student_id

    def add_student_window(self):
        frame = Toplevel()
        self.first_name_label = Label(frame,text="First Name: ")
        self.last_name_label = Label(frame,text="Last Name: ")
        self.pass_label = Label(frame,text="Student Password: ")
        self.id_label = Label(frame,text="Student ID: ")
        self.first_name_entry = Entry(frame)
        self.last_name_entry = Entry(frame)
        self.pass_entry = Entry(frame)
        self.id_entry = Entry(frame)

        self.saveButton = Button(frame,text="Save",width=7,command=lambda: self.add_student(frame,
                self.first_name_entry.get(),self.last_name_entry.get(),
                self.id_entry.get(),self.pass_entry.get()))
        self.cancelButton = Button(frame, text = "Cancel",width=7,command=frame.destroy)

        self.first_name_label.grid(row=2,column=1)
        self.first_name_entry.grid(row=2,column=2)
        self.last_name_label.grid(row=3,column=1)
        self.last_name_entry.grid(row=3,column=2)
        self.pass_label.grid(row=4,column=1)
        self.pass_entry.grid(row=4,column=2)
        self.id_label.grid(row=5,column=1)
        self.id_entry.grid(row=5,column=2)
        self.saveButton.grid(row=6,column=2,sticky=W)
        self.cancelButton.grid(row=6,column=2,sticky=E)

    def add_student(self,frame,f_name,l_name,s_id,password):
        print("checking function call")
        print(f_name,l_name,s_id,password)
        if not f_name or not l_name or not s_id or not password:
            print("Please fill all entries")
            ctypes.windll.user32.MessageBoxW(0, "Please Fill all required entries", "Message", 0)
        else:
            with dbfile:
                dbcursor.execute("INSERT INTO students (student_id,first_name,last_name) values (?,?,?)",
                          (s_id,f_name,l_name))

                dbcursor.execute("INSERT INTO users (id,password,access) values (?,?,?)",
                          (s_id,password,"student"))

                dbfile.commit()
            frame.destroy()

    def remove_student_window(self):
        frame = Toplevel()
        confirm_label = Label(frame,text = "Are you sure?")
        confirm_button = Button(frame,text="Yes",command= lambda: [self.confirm(),frame.destroy()])
        cancel_button = Button(frame,text="Cancel",command = frame.destroy)

        confirm_label.grid(row=0,column=0)
        confirm_button.grid(row=1,column=0)
        cancel_button.grid(row=1,column=1)

    def remove_student(self):

        with dbfile:
            student_id = self.get_student_id()
            dbcursor.execute("DELETE FROM enrollment WHERE student_id = ?",
                      (student_id,))
            dbcursor.execute("DELETE FROM grades WHERE student_id = ?",
                      (student_id,))
            dbcursor.execute("DELETE FROM students WHERE student_id = ?",
                      (student_id,))
            dbcursor.execute("DELETE FROM users WHERE id = ?",
                      (student_id,))
            dbfile.commit()
        self.set_student_id("")


    def confirm(self):

        frame = Toplevel()
        enter_pass_label = Label(frame,text="Please enter your password")
        password_entry = Entry(frame,show="*")
        confirm_button = Button(frame,text="Confirm",command= lambda: self.verify_pass(frame,password_entry.get()))

        enter_pass_label.grid(row=0,column=0)
        password_entry.grid(row=0,column=1)
        confirm_button.grid(row=1,column=1)

    def verify_pass(self,frame,password):
        c_id = self.get_course_id()
        s_id = self.get_student_id()

        if(password==self.admin_user_pass()):
            if s_id:
                self.remove_student()
                ctypes.windll.user32.MessageBoxW(0, "Student has been deleted from records", "Message", 0)
                self.set_student_id("")
                frame.destroy()
            if c_id:
                self.remove_course()
                ctypes.windll.user32.MessageBoxW(0, "Course has been deleted from records", "Message", 0)
                self.set_course_id("")
                frame.destroy()

        else:
            ctypes.windll.user32.MessageBoxW(0, "Password entered does not match", "Message", 0)


    def add_course_window(self):
        frame = Toplevel()
        self.c_name_label = Label(frame,text="Course Name: ")
        self.c_id_label = Label(frame,text="Course ID: ")
        self.c_hr_label = Label(frame,text="Credit Hours: ")
        self.instructor_label = Label(frame,text="Instructor: ")
        self.c_name_entry = Entry(frame)
        self.c_id_entry = Entry(frame)
        self.c_hr_entry = Entry(frame)
        self.instructor_entry= Entry(frame)
        self.saveButton = Button(frame,text="Save",width=7,command=lambda: self.add_course(frame,
                                                                                           self.c_id_entry.get(),self.c_name_entry.get(),
                                                                                           self.c_hr_entry.get(),self.instructor_entry.get() ))
        self.cancelButton = Button(frame, text = "Cancel",width=7,command=frame.destroy)

        self.c_name_label.grid(row=2,column=1)
        self.c_name_entry.grid(row=2,column=2)
        self.c_id_label.grid(row=3,column=1)
        self.c_id_entry.grid(row=3,column=2)
        self.c_hr_label.grid(row=4,column=1)
        self.c_hr_entry.grid(row=4,column=2)
        self.instructor_label.grid(row=5,column=1)
        self.instructor_entry.grid(row=5,column=2)
        self.saveButton.grid(row=6,column=2,sticky=W)
        self.cancelButton.grid(row=6,column=2,sticky=E)

    def add_course(self,frame,c_id,c_name,c_hour,i_name):
        if not c_id or not c_name or not c_hour or not i_name:
            ctypes.windll.user32.MessageBoxW(0, "Please Fill all required entries", "Message", 0)
        else:
            with dbfile:
                dbcursor.execute("INSERT INTO courses (course_id,course_name,credit_hour,instructor_name) values (?,?,?,?)",
                          (c_id,c_name,c_hour,i_name))

                dbfile.commit()
            frame.destroy()

    def remove_course_window(self):
        frame = Toplevel()
        confirm_label = Label(frame,text = "Are you sure?")
        confirm_button = Button(frame,text="Yes",command= lambda: [self.confirm(),frame.destroy()])
        cancel_button = Button(frame,text="Cancel",command = frame.destroy)

        confirm_label.grid(row=0,column=0)
        confirm_button.grid(row=1,column=0)
        cancel_button.grid(row=1,column=1)

    def remove_course(self):

        with dbfile:
            c_id = self.get_course_id()
            dbcursor.execute("DELETE FROM courses WHERE course_id = ?",
                      (c_id,))
            dbcursor.execute("DELETE FROM enrollment WHERE course_id = ?",
                      (c_id,))
            dbfile.commit()
        self.set_course_id("")



    def search_id(self,frame):
        if self.searchEntry:#not in database
            self.listbox = Listbox(frame, width=30, height=10,)
            self.listbox.grid(row=6, column=1)
            self.listbox.config(state=NORMAL)
            self.listbox.delete('0',END)

            with dbfile:
                search_id=self.searchEntry.get()
                dbcursor.execute("SELECT * FROM students WHERE student_id= ?",(search_id,))

                dbfile.commit()
                student = dbcursor.fetchone()

                dbcursor.execute("SELECT * FROM courses WHERE course_id= ?",(search_id,))

                dbfile.commit()
                course = dbcursor.fetchone()


                if student:

                    dbcursor.execute("SELECT * FROM enrollment WHERE student_id= ?",(search_id,))

                    dbfile.commit()
                    courses = dbcursor.fetchall()

                    self.set_student_id(student[0])
                    self.set_course_id("")
                    student_id = student[0]

                    label = []
                    labels = ['Student ID: ','First Name: ','Last Name: ']
                    course_list = []


                    for i in range (len(student)):
                        self.listbox.insert('end',labels[i]+student[i])
                    self.listbox.insert('end',"Courses: ")

                    for i in range (len(courses)):
                        self.listbox.insert('end',courses[i][1] +" " +courses[i][2])


                    remove_student_button = Button(frame,text="Remove Student",command= lambda: self.remove_student_window())
                    remove_student_button.grid(row=6,column = 2,sticky=NE)

                    view_grades_button = Button(frame,text="View Grades",command=lambda: self.view_grades_window())
                    view_grades_button.grid(row = 6,column=2,sticky=SE)

                    view_courses_button = Button(frame,text="View Courses",command=lambda: self.view_courses_window())
                    view_courses_button.grid(row=6,column=2,sticky=E)

                elif course:

                    self.set_course_id(course[0])
                    self.set_student_id("")
                    student_id = ""
                    course_info = ["Course ID: ", "Course Name: ", " Credit Hours: ","Instructor: "]
                    for i in range(len(course)):
                        self.listbox.insert('end',course_info[i]+" "+str(course[i]))

                    remove_course_button = Button(frame,text = "Remove Course",command = lambda: self.remove_course_window())
                    remove_course_button.grid(row=6,column = 2,sticky=N)

                else:
                    self.set_course_id("")
                    self.set_student_id("")
                    print("try and hide this")


    def view_courses_window(self):
        student_id = self.get_student_id()
        if student_id:
            frame = Toplevel()
            coursesLabel = Label(frame,text="Courses")
            coursesLabel.grid(row=0,column=0,sticky=N)
            self.show_courses(frame,student_id)


            drop_course_button = Button(frame,text="Drop Course",command=lambda: [self.drop_course(student_id,self.listbox.index(ACTIVE)),self.show_courses(frame,student_id),self.listbox.select_set(0)])
            drop_course_button.grid(row=0,column=0)

            courses = []
            courses = self.offered_courses()
            courselist_label = Label(frame,text="Course list:")
            course_combobox= ttk.Combobox(frame,value = courses,width=40)
            enroll_button = Button(frame,text = "Enroll",command=lambda: [self.enroll(student_id,courses[course_combobox.current()]),self.show_courses(frame,student_id)])

            courselist_label.grid(row=0,column=2,sticky=N)
            course_combobox.grid(row=0,column=2)
            enroll_button.grid(row=0,column=2,sticky=S)

    def drop_course(self,student_id,i):
        courses = []
        courses = self.admin_show_courses(student_id)
        course_id = courses[i][1]
        with dbfile:
            dbcursor.execute("DELETE FROM enrollment WHERE student_id = ? and course_id = ?",
                    (student_id,course_id))
            dbfile.commit()

    def enroll(self,student_id,course):
        with dbfile:
            c_id = course[0]
            c_name = course[1]
            c_hour = course[2]
            c_instructor = course[3]

            dbcursor.execute("INSERT INTO enrollment (student_id,course_id,course_name,credit_hour,instructor) values (?,?,?,?,?)",
                    (student_id,c_id,c_name,c_hour,c_instructor))

            dbfile.commit()


    def show_courses(self,frame,student_id):
        self.listbox = Listbox(frame, width=50,height=10,)
        self.listbox.grid(row=0, column=1)
        self.listbox.config(state=NORMAL)
        self.listbox.delete('0',END)

        courses = []
        courses = self.admin_show_courses(student_id)

        for i in range (len(courses)):
                self.listbox.insert('end',courses[i][1] + "    "+(courses[i][2]) + "    "+str(courses[i][3]) +"    "+courses[i][4])
        self.listbox.select_set(0)
        return self.listbox




    def view_grades_window(self):
        student_id = self.get_student_id()
        if student_id:
            frame = Toplevel()
            course_list = []
            course_list = self.admin_course_list(student_id)
            self.course_label = Label(frame,text="Course ID: ")
            self.course_combobox = ttk.Combobox(frame,value=course_list)
            self.course_label.grid(row=0,column=0)
            self.course_combobox.grid(row=0,column=1)
            self.add_grade_button = Button(frame,text="Add/Remove Grades",command=lambda: self.add_grades_window(self.course_combobox.get(),student_id))
            self.add_grade_button.grid(row=1,column=1)

        #assignment entry
    def add_grades_window(self,course_id,student_id):
        frame = Toplevel()
        self.set_course_id(course_id)
        self.a_label = Label(frame,text="Assignment Name")
        self.a_entry = Entry(frame)
        self.g_label = Label(frame,text = "Grade: ")
        self.g_entry = Entry(frame)
        self.add_button = Button(frame,text="Add Grade",command=lambda: [self.add_grades(course_id,student_id,self.a_entry.get(),self.g_entry.get()),self.show_grades(frame,student_id,course_id)])

        self.a_label.grid(row=0,column=0)
        self.a_entry.grid(row=0,column=1)
        self.g_label.grid(row=1,column=0)
        self.g_entry.grid(row=1,column=1)
        self.add_button.grid(row=2,column=1)
        self.show_grades(frame,student_id,course_id)

        self.r_label = Label(frame,text="Remove Grades: ")
        self.admin_assignments(student_id,course_id)
        self.remove_button = Button(frame, text="Delete",command=lambda: [self.remove_grades(frame,student_id,course_id,self.L.index(ACTIVE))])
        self.r_label.grid(row=4,column=0,stick=N)
        self.remove_button.grid(row=4,column=0)



    def show_grades(self,frame,student_id,course_id):

        grades = []
        grades = self.admin_select_grades(student_id,course_id)

        self.s = Scrollbar(frame)
        self.L = Listbox(frame)

        self.s.grid(row=4,column=2,sticky=NS)
        self.L.grid(row=4,column=1,sticky=E)
        self.L.config(state=NORMAL)
        self.L.delete('0',END)


        self.s['command'] = self.L.yview
        self.L['yscrollcommand'] = self.s.set

        for i in range(len(grades)):
           self.L.insert(END, grades[i][3]+":    "+str(grades[i][2]) )
        print(grades)
        return self.L

    def add_grades(self,course_id,student_id,assignment,grade):

        with dbfile:
            s_id = student_id
            c_id = course_id
            g = grade
            a = assignment

            dbcursor.execute("INSERT INTO grades (student_id,course_id,grades,assignment) values (?,?,?,?)",
                    (s_id,c_id,g,a))

            dbfile.commit()


    def remove_grades(self,frame,student_id,course_id,i):

        grades = []
        grades = self.admin_select_grades(student_id,course_id)
        print("printing grades table")
        print(grades)
        assignment = grades[i][3]
        with dbfile:
            dbcursor.execute("DELETE FROM grades WHERE assignment = ? and student_id = ?",
                    (assignment,student_id))
            dbfile.commit()
        self.show_grades(frame,student_id,course_id)



class StudentWindow(User):



    def __init__(self,master,s_id,s_pass):

        self.admin_set_id(s_id)
        self.admin_set_pass(s_pass)


        with dbfile:
                dbcursor.execute("SELECT * FROM students WHERE student_id= ?",(s_id,))

                dbfile.commit()
                student = dbcursor.fetchone()

                dbcursor.execute("SELECT * FROM enrollment WHERE student_id= ?",(s_id,))

                dbfile.commit()
                courses = dbcursor.fetchall()

        label = []
        labels = ['Student ID: ','First Name: ','Last Name: ']
        course_list = []


        master.geometry("640x400")
        master.title("GatorsConnect-"+s_id+"(Student)")
        master.configure(bg="MEDIUMPURPLE")
        frame = Frame(master,bg="MEDIUMPURPLE",width = 500,height = 100)
        frame2 = Frame(master,bg="MEDIUMPURPLE",width = 500,height = 100)
        frame3 = Frame(master,bg="#FF0000",width = 200)


        frame.place(relx = 0.30, rely = 0.5,anchor = "center")
        frame2.place(relx = 0.70, rely = 0.525,anchor = "center")
        frame3.place(relx = 0.5, y=2, anchor = N)

        title_label = Label(frame3,bg="THISTLE",text="Student Profile",font=("ms sans serif",24,"bold"),width = 400)
        title_label.pack(fill=X,expand=1)

        self.listbox = Listbox(frame, width=30, height=10)
        self.listbox.grid(row=6, column=0)
        self.listbox.config(state=NORMAL)
        self.listbox.delete('0',END)

        student_profile = Label(frame,text="Student Info: ",bg="THISTLE",relief="raised")
        student_profile.grid(row=0,column=0,sticky="w")
        label = Label(frame,bg="MEDIUMPURPLE")
        label.grid(row=1,column=1)

        self.listbox2 = Listbox(frame2, width=30, height=10)
        self.listbox2.grid(row=6, column=0)
        self.listbox2.config(state=NORMAL)
        self.listbox2.delete('0',END)


        for i in range (len(student)):
            self.listbox.insert('end',labels[i]+student[i])
        self.listbox.insert('end',"Courses: ")

        for i in range (len(courses)):
            self.listbox.insert('end',courses[i][1] +" " +courses[i][2])
            course_list.append(courses[i][1])
        print(course_list)



        self.course_label = Label(frame2,text="Course ID: ",bg="LIGHTSEAGREEN",relief="raised")
        self.course_combobox = ttk.Combobox(frame2,width = 16,value=course_list)
        self.view_course_button = Button(frame2,bg = "THISTLE",text = "View Course Details",command = lambda:self.view_course_details(self.course_combobox.get(),frame2))
        self.course_label.grid(row=0,column=0,sticky="w")
        self.course_combobox.grid(row=0,column=0,sticky="e")
        self.view_course_button.grid(row=1,column=0,sticky="e")

        self.view_grades_button = Button(frame2,text="View Grades",bg="THISTLE",command = lambda: self.view_grades(self.course_combobox.get()))
        self.view_grades_button.grid(row=7,sticky="e")

        #grade point function
        student_id= self.admin_get_id() #get_student_id()
        course_grade = []
        for x in range(len(courses)):
            course_grade.append(0)
        total_grade_point = 0
        total_credit_hours = 0

        for i in range(len(courses)):
            assignments = []
            total_credit_hours = total_credit_hours + courses[i][3]
            assignments = self.admin_grades(student_id,courses[i][1])
            for j in range(len(assignments)):
                course_grade[i]=course_grade[i] + assignments[j]

            if(len(assignments)>0):
                total_grade_point = total_grade_point + courses[i][3]*self.get_grade_point(course_grade[i]/len(assignments))
            else:
                total_credit_hours = total_credit_hours - courses[i][3]


        gpa = total_grade_point/total_credit_hours

        self.listbox.insert('end',"GPA: "+str(gpa))
        print(gpa)


    def get_grade_point(self,avg):
        if avg >= 60 and avg < 70:
            return 1
        elif avg >= 70 and avg < 80:
            return 2
        elif avg >= 80 and avg < 90:
            return 3
        elif avg >= 90:
            return 4
        else:
            return 0




    def view_grades(self,course_id):
        student_id = self.admin_get_id()
        frame = Toplevel(bg="MEDIUMPURPLE")

        grades = []
        grades = self.admin_select_grades(student_id,course_id)

        self.s = Scrollbar(frame)
        self.L = Listbox(frame)

        self.s.grid(row=4,column=2,sticky=NS)
        self.L.grid(row=4,column=1,sticky=E)
        self.L.config(state=NORMAL)
        self.L.config(width=30)
        self.L.delete('0',END)


        self.s['command'] = self.L.yview
        self.L['yscrollcommand'] = self.s.set

        total = 0

        Label(frame,bg="THISTLE",text="      Assignments / Grades :      ").grid(row=4,column=0,sticky="ne")
        for i in range(len(grades)):
           self.L.insert(END, grades[i][3]+":    "+str(grades[i][2]) )
           total = total + grades[i][2]
        course_avg = total/len(grades)
        self.L.insert(END,"Course Average: "+str(course_avg))
        print(grades)


    def view_course_details(self,c_id,frame):

        self.listbox = Listbox(frame, width=30, height=10)
        self.listbox.grid(row=6, column=0)
        self.listbox.config(state=NORMAL)
        self.listbox.delete('0',END)
        with dbfile:
            dbcursor.execute("SELECT * FROM courses WHERE course_id= ?",(c_id,))

            dbfile.commit()
            course = dbcursor.fetchone()

        course_info = ["Course ID: ", "Course Name: ", " Credit Hours: ","Instructor: "]
        for i in range(len(course)):
            self.listbox.insert('end',course_info[i]+" "+str(course[i]))