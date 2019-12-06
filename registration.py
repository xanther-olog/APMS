from time import sleep
import serial
import pymysql as sql
import tkinter
from tkinter import *
from tkinter import messagebox as msgb
def initAlertGui():
    root=Tk()
    root.title("Notice")
    windowWidth=root.winfo_reqwidth()
    windowHeight=root.winfo_reqheight()
    positionRight=int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown=int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    root.withdraw()
    msgb.showinfo("Alert!","You have already registered!")
    root.destroy()
def initFormGui(x):
    root=Tk()
    root.title("Registration Form")
    windowWidth=root.winfo_reqwidth()
    windowHeight=root.winfo_reqheight()
    positionRight=int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown=int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    def ex():
        root.destroy()
    def submit(id):
        name=E1.get()
        regno=E2.get()
        addToDatabase(id,name,regno)
        root.withdraw()
        msgb.showinfo("Notice",name+" has been authorised to use the parking.")
        root.destroy()
    picc=x
    L1=Label(root,text="Enter your name: ")
    L2=Label(root,text="Enter your Registration Number: ")
    E1=Entry(root,font=("Arial", 20))
    E2=Entry(root,font=("Arial", 20))
    L1.grid(row=0,column=0)
    L2.grid(row=1,column=0)
    E1.grid(row=0,column=1)
    E2.grid(row=1,column=1)
    B1=Button(root,text="Submit",command=lambda: submit(picc))
    B2=Button(root,text="Exit",command=ex)
    B1.grid(row=2,column=0)
    B2.grid(row=2,column=1)
    L1.config(font=("Arial", 20))
    L2.config(font=("Arial", 20))
    root.mainloop()
def addToDatabase(buffer,name,regno):
    #add first time users to database
    conn=sql.connect(host="localhost" , user="root" , password="" , database="minor_project")
    if(conn):
        cursor=conn.cursor()
        insertQuery="INSERT INTO registration_parking(name,rno,picc_id) VALUES(%s,%s,%s);"
        x=(name , regno , buffer)
        cursor.execute(insertQuery,x)
        conn.commit()
        print("User Data Saved! Please continue.")
        cursor.close()
    else:
        print("Connection Unsuccessful! User Entry Failed!")
def checkExistence(buffer):
    #check if user already exists in database
    conn=sql.connect(host="localhost" , user="root" , password="" , database="minor_project")
    if(conn):
        cursor=conn.cursor()
        query="SELECT * FROM registration_parking WHERE picc_id=%s;"
        cursor.execute(query,buffer)
        conn.commit()
        row_count=cursor.rowcount
        cursor.close()
        if(row_count==0):
            return False
        else:
            return True
    else:
        print("Connection Unsuccessful! Existence Check Failed!")
try:
    port = "/dev/ttyACM0"   #define port
    ard = serial.Serial(port,9600,timeout=5)
    while(1):
        #begin infinite loop
        buffer=ard.readline()
        #string formatting
        buffer=buffer[0:len(buffer)-2].decode("utf-8")
        if(len(buffer)!=0): #prevent null values in system
            bakwaas=buffer.split(";")
            rfid=bakwaas[0]
            picc=bakwaas[1]
            exists=checkExistence(picc)
            if(exists):
                print("You've already registered!")
                initAlertGui()
            else:
                initFormGui(picc)
        else:
            continue
except(serial.SerialException):
    print("Device not detected! Could not open port.")
except(KeyboardInterrupt):
    print("\nProgram Stopped! Keyboard Interrupt Detected!")
finally:
    print("Shutting Down!")
