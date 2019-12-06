import pymysql as sql
#script to check which slots are empty and provide a tentative slot to the user
def getslot():
    conn=sql.connect(host="localhost" ,\
     user="root" , password="" , database="minor_project")
    if(conn):
        cursor=conn.cursor()
        query="SELECT slot_id FROM slot_monitor WHERE\
         state ='Empty' ORDER BY Sno ASC;"
        cursor.execute(query)
        conn.commit()
        result=cursor.fetchall()
        cursor.close()
        if(len(result)>0):
            return result[0][0]
        else:
            return "Full"
    else:
        print("Connection Declined! Slot updation Failed")
