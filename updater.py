from time import sleep
import serial
import pymysql as sql
def checkSlots(id , prox_status):
    #check which slots are empty regularly over a period of time
    flag=""
    val=int(prox_status)
    id=str(id)
    if(val>=700):
        flag="Empty"
    else:
        flag="Occupied"
    conn=sql.connect(host="localhost" ,\
     user="root" , password="" , database="minor_project")
    if(conn):
        cursor=conn.cursor()
        #update to table accordingly
        query="UPDATE slot_monitor SET state=%s WHERE SNo=%s;"
        x=(flag , id)
        cursor.execute(query,x)
        conn.commit()
        cursor.close()
    else:
        print("Connection Declined! Slot updation Failed")
port = "/dev/ttyACM1"
ard = serial.Serial(port,9600,timeout=3)
m=1
while(1):
    x=ard.readline()
    #print(x)
    x=x[0:len(x)-2].decode("utf-8").split()
    checkSlots(x[0],x[1])
    m=-1*m
    if m==1:
        sleep(3)    #refresh parking slots every 3 seconds
