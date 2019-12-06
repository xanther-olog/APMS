from time import sleep
import serial
import pymysql as sql
import time     #calculate timestamps
import cv2
import slot     #defined as slot.py
import imageProcess as imgP
import alpr
def clickEntryImage():
    camera=cv2.VideoCapture(0);
    ret, frame = camera.read()
    img_name = "opencv_frame_entry.png"
    cv2.imwrite(img_name, frame)
    camera.release()
def clickExitImage():
    camera=cv2.VideoCapture(0);
    ret, frame = camera.read()
    img_name = "opencv_frame_exit.png"
    cv2.imwrite(img_name, frame)
    camera.release()
def checkRegistration(buffer):
    #check if user is registered to use the Parking
    #deny parking if user doesn't exist
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
def addToDatabase(buffer):
    #register entry of car in parking lot
    picc=buffer
    imageLocation="/home/arkadeep/Documents/Mini_experiment/opencv_frame_entry.png"
    #imageLocation="/home/arkadeep/Documents/Mini_experiment/tmkc.jpg"
    enlplate=alpr.getresult(imageLocation)
    #lplate="GJ 16 AP 3152"
    flag=checkRegistration(picc)
    if(flag==True and enlplate != -1):
        val=slot.getslot()
        if "Full" in val:
            print("Parking full! Try Again Later")
        else:
            conn=sql.connect(host="localhost" , user="root" , password="" , database="minor_project")
            if(conn):
                cursor=conn.cursor()
                curr_time=time.ctime(time.time())
                insertQuery="INSERT INTO entry_table(picc_id,timestamps,number_plate) VALUES(%s,%s,%s);"
                x=(buffer , curr_time , enlplate)
                cursor.execute(insertQuery,x)
                conn.commit()
                withdraw_query="SELECT name,rno FROM registration_parking WHERE picc_id=%s;"
                cursor.execute(withdraw_query,picc)
                result=cursor.fetchall()
                user_name=result[0][0]
                reg_no=result[0][1]
                #register user entry to log file
                entryLogQuery="INSERT INTO log_table_in(rno , name , in_time, img , number_plate) VALUES (%s,%s,%s,%s,%s);"
                image=imgP.convertToString(imageLocation)
                x=(reg_no , user_name , curr_time , image , enlplate)
                cursor.execute(entryLogQuery,x)
                conn.commit()
                print("User Punching In!")
                print("User ID: "+user_name+" at "+curr_time)
                print("Number Plate: "+enlplate)
                print("Recommended Parking Slot: ",val)
                cursor.close()
            else:
                print("Connection Unsuccessful! User Entry Failed!")
    else:
        print("Parking Denied!")
def deleteFromDatabase(buffer):
    #remove user details from parking management table if user leaves the parking
    picc=buffer
    imageLocation="/home/arkadeep/Documents/Mini_experiment/opencv_frame_exit.png"
    #imageLocation="/home/arkadeep/Documents/Mini_experiment/tmkc.jpg"
    exlplate=alpr.getresult(imageLocation)
    #lplate="GJ 16 AP 3152"
    conn=sql.connect(host="localhost" , user="root" , password="" , database="minor_project")
    if(conn and exlplate != -1):
        cursor=conn.cursor()
        exitQuery="SELECT number_plate FROM entry_table where picc_id=%s"
        cursor.execute(exitQuery,buffer)
        conn.commit()
        exitResult=cursor.fetchall()
        leaving_number_plate=exitResult[0][0]
        if(leaving_number_plate==exlplate):
            query="DELETE FROM entry_table where picc_id=%s"
            cursor.execute(query,buffer)
            curr_time=time.ctime(time.time())
            conn.commit()
            withdraw_query="SELECT name,rno FROM registration_parking WHERE picc_id=%s;"
            cursor.execute(withdraw_query,picc)
            result=cursor.fetchall()
            user_name=result[0][0]
            reg_no=result[0][1]
            #update time at which user leaves the parking lot in log file
            exitLogQuery="INSERT INTO log_table_out(rno , name , out_time, img, number_plate) VALUES (%s,%s,%s,%s,%s);"
            image=imgP.convertToString(imageLocation)
            x=(reg_no , user_name , curr_time , image , exlplate)
            cursor.execute(exitLogQuery,x)
            conn.commit()
            print("User Punching Out!")
            print("User ID: "+user_name+" at "+curr_time)
            cursor.close()
        else:
            print("Number plate Verification failed")
            print("Number plate detected at entry gate was",leaving_number_plate)
            print("Number plate detected at exit gate was",exlplate)
            print("Please contact Administrator")
    else:
        print("Connection Unsuccessful! Number Plate Verification Failed!")
def checkExistence(buffer):
    #check if user already exists in database
    #deny parking if user not registered
    conn=sql.connect(host="localhost" , user="root" , password="" , database="minor_project")
    if(conn):
        cursor=conn.cursor()
        query="SELECT * FROM entry_table WHERE picc_id=%s;"
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
port = "/dev/ttyACM0"
ard = serial.Serial(port,9600,timeout=5)
while(1):
    buffer=ard.readline()
    buffer=buffer[0:len(buffer)-2].decode("utf-8")
    if(len(buffer)!=0):
        bakwaas=buffer.split(";")
        rfid=int(bakwaas[0])
        picc=bakwaas[1]
        exists=checkExistence(picc)
        if(exists and rfid==2):
            clickExitImage()
            deleteFromDatabase(picc)
        elif(exists and rfid==1):
            print("You have already entered the parking lot!")
        elif(not exists and rfid==2):
            print("Proceed to Entry Gate.")
        else:
            #capture image of the entering car when rfid sensor triggered
            clickEntryImage()
            addToDatabase(picc)
    else:
        continue
