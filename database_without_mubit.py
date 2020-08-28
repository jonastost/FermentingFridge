import time
from datetime import datetime
import mysql.connector as sql

hostn = "localhost"
databasen = "ferment_data"
usernamen = "jonastost"
passwordn = "rachelrand"

def handler(signum, frame):
    print("The connecting statement timed out.")
    raise Exception("Timeout")

mysql = sql.connect(
    host= hostn,
    user=usernamen,
    password=passwordn,
    database=databasen
)
cursor = mysql.cursor()

current_str = ""

while True:
    delaystart = time.time()
    cursor1 = mysql.cursor()
    cursor1.execute("SELECT brew_name_time, mode FROM All_Records WHERE done=false")
    currents = cursor1.fetchall()
    print(currents)
    for cur in currents:
        cursor2 = mysql.cursor()
        cursor3 = mysql.cursor()
        cursor4 = mysql.cursor()
        print(cur[0])
        try:
            cursor3.execute("SELECT time FROM "+cur[0]+"_data ORDER BY row DESC LIMIT 1")
            three = cursor3.fetchall()
            print(three)
            #cursor4.execute("SELECT time, row FROM "+cur+" ORDER BY row DESC LIMIT 1")
            cursor4.execute("SELECT row FROM "+cur[0]+"_data")
            four = cursor4.fetchall()
        except (Exception):
            four = None

        if (four is not None):
            for x in four:
                latest = x[0]
                row = latest+1
                row = str(row)
                print(row)
            for x in three:
                time = time.time()-x[0]
        else:
            time = time.time()
            row = str(1)
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        if (cur[1] != "fridge" or cur[1] != "time"):
            current_temp = str(1000)
            average_temp = str(1000)
            
            time = str(time)
            timestamp = str(timestamp)
            
            cursor3.fetchall()
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, current_temp, average_temp, row) VALUES ('"+time+"', '"+timestamp+"', "+current_temp+", "+average_temp+", "+row+")")
            mysql.commit()
        else:
            time = str(time)
            timestamp = str(timestamp)
            cursor3.fetchall()
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, row) VALUES ('"+time+"', '"+timestamp+"', "+row+")")
            mysql.commit()
        
        if (float(time) > 1209600):
            cursor3.fetchall()
            cursor3.execute("UPDATE "+cur[0]+"_data SET done = true WHERE done = false")
            mysql.commit()
            cursor3.fetchall()
            cursor3.execute("UPDATE All_Records SET done = true WHERE brew_name_time = "+cur[0])
            mysql.commit()
    delayend = time.time()
    delay = delayend - delaystart
    if (delay > 60):
        delay = 60
    time.sleep(120-delay)
    delay = 0