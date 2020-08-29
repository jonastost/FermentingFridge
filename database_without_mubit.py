import time as timer
from datetime import datetime
import mysql.connector as sql

hostn = "localhost"
databasen = "ferment_data"
usernamen = "jonastost"
passwordn = "rachelrand"

mysql = sql.connect(
    host= hostn,
    user=usernamen,
    password=passwordn,
    database=databasen
)
cursor = mysql.cursor()

current_str = ""

while True:
    delaystart = timer.time()
    cursor1 = mysql.cursor()
    cursor1.execute("SELECT brew_name_time, mode FROM All_Records WHERE done=false")
    currents = cursor1.fetchall()
    print(currents)
    for cur in currents:
        cursor3 = mysql.cursor()
        cursor4 = mysql.cursor()
        print(cur[0])
        try:
            cursor3.execute("SELECT time FROM "+cur[0]+"_data LIMIT 1")
            three = cursor3.fetchall()
            print(three)
            cursor4.execute("SELECT row FROM "+cur[0]+"_data ORDER BY row DESC LIMIT 1")
            #cursor4.execute("SELECT row FROM "+cur[0]+"_data")
            four = cursor4.fetchall()
        except (Exception):
            four = ()
            print("There was an exception")
        print(four)

        if (len(four)>0):
            for x in four:
                latest = x[0]
                row = latest+1
                row = str(row)
                print(row)
            for x in three:
                time = timer.time()-float(x[0])
        else:
            time = timer.time()
            row = str(1)
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        print(row)
        if (cur[1] == "fridge" or cur[1] == "time"):
            current_temp = str(1000)
            average_temp = str(1000)
            
            time = str(time)
            timestamp = str(timestamp)
            print(cur[0])
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, current_temp, average_temp, row) VALUES ('"+time+"', '"+timestamp+"', "+current_temp+", "+average_temp+", "+row+")")
            mysql.commit()
        else:
            time = str(time)
            timestamp = str(timestamp)
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, row) VALUES ('"+time+"', '"+timestamp+"', "+row+")")
            mysql.commit()
        
        if (float(time) > 1209600 and int(row) != 1):
            cursor3.execute("UPDATE "+cur[0]+" SET done = true WHERE done = false")
            mysql.commit()
            cursor3.execute("UPDATE All_Records SET done=true WHERE brew_name_time = '"+cur[0]+"'")
            mysql.commit()
    delayend = timer.time()
    delay = delayend - delaystart
    if (delay > 60):
        delay = 60
    timer.sleep(120-delay)
    delay = 0