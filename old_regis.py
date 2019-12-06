from time import sleep
import serial   #to get data from serial port via arduino
import pymysql as sql   #connect mysql server
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
        else:
            name=input("Enter your name: ")
            regno=input("Enter your Registration Number: ")
            addToDatabase(picc,name,regno)
    else:
        continue
