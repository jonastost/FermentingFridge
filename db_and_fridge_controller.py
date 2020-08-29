from bluezero import microbit
import dbus
import time
from datetime import datetime
import mysql.connector as sql
import signal
import os

tempup = 18
tempdown = 16
sleepingtime = 60

hostn = "localhost"
databasen = "ferment_data"
usernamen = "jonastost"
passwordn = "rachelrand"

def handler(signum, frame):
    print("The connecting statement timed out.")
    raise Exception("Timeout")

#Remember that if a new microbit program used, repair the devices first
ubit = microbit.Microbit(
    adapter_addr='B8:27:EB:E5:57:0A',
    device_addr='C9:9F:35:CF:03:1D',
    accelerometer_service=False,
    button_service=False,
    led_service=False,
    magnetometer_service=False,
    pin_service=False,
    temperature_service=True)

mysql = sql.connect(
    host= hostn,
    user=usernamen,
    password=passwordn,
    database=databasen
)
signal.signal(signal.SIGALRM, handler)
os.system('sudo /var/www/html/rfoutlet/codesend 4199731')
time.sleep(5)

current = True
reconnect = False
off = False
temp = 20
reconnections = 0
delay = 0

print("connected and trying to receive sensor information")
total_time = 0

while True:
    start_total = time.time()
    ubit.connect()
    disconnected = True
    while disconnected:
        start = time.time()
        try:
            if reconnect:
                ubit = microbit.Microbit(
                    adapter_addr='B8:27:EB:E5:57:0A',
                    device_addr='C9:9F:35:CF:03:1D',
                    accelerometer_service=False,
                    button_service=False,
                    led_service=False,
                    magnetometer_service=False,
                    pin_service=True,
                    temperature_service=True)
                signal.alarm(15)
                ubit.connect()
                signal.alarm(0)
                
            temp = ubit.temperature
            print("Temperature: ", temp)
            now = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            print(now)
            if temp >= tempup:
                off = False
            elif temp <= tempdown:
                off = True
            disconnected = False
            reconnect = False
        except dbus.exceptions.DBusException:
            print("Connection lost, reestablishing...")
            reconnections = reconnections + 1
            reconnect = True
        except Exception as ex:
            print("An Exception was thrown.")
            print(str(ex))
            reconnect = True
        end = time.time()
        delay = delay + (end-start)
    ubit.disconnect()
    # Can we get this part to run in the background such that we continue with rigid timing?
    start = time.time()
    if off and current:
        print("Turning off the fridge...")
        os.system('sudo /var/www/html/rfoutlet/codesend 4199740')
        time.sleep(2)
        os.system('sudo /var/www/html/rfoutlet/codesend 4199740')
        current = False
        print("Done.")
    elif not off and not current:
        print("Turning on the fridge...")
        os.system('sudo /var/www/html/rfoutlet/codesend 4199731')
        time.sleep(2)
        os.system('sudo /var/www/html/rfoutlet/codesend 4199731')
        current = True
        print("Done.")
    print("There have been ", reconnections, " reconnection attempts.")
    print("\n")
    
    #Here is the code that controls the MySQL database.
    mysql.disconnect()
    mysql = sql.connect(
    host= hostn,
    user=usernamen,
    password=passwordn,
    database=databasen
    )
    
    cursor1 = mysql.cursor()
    cursor1.execute("SELECT brew_name_time, mode FROM All_Records WHERE done=false")
    currents = cursor1.fetchall()
    for cur in currents:
        three = ()
        four = ()
        cursor3 = mysql.cursor()
        cursor4 = mysql.cursor()
        try:
            cursor3.execute("SELECT time FROM "+cur[0]+"_data LIMIT 1")
            three = cursor3.fetchall()
            cursor4.execute("SELECT row, average_temp FROM "+cur[0]+"_data ORDER BY row DESC LIMIT 1")
            four = cursor4.fetchall()
        except (Exception):
            four = ()
            print("There was an exception")
        if (len(four)>0):
            for x in four:
                latest = x[0]
                average_temp = float(x[1])
                row = latest+1
                row = str(row)
            for x in three:
                times = time.time()-float(x[0])
        else:
            times = time.time()
            row = str(1)
            average_temp = float(1000)
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        if (cur[1] == "fridge" or cur[1] == "time"):
            current_temp = str(temp)
            if (average_temp == float(1000)):
                average_temp = current_temp
            else:
                average_temp = (average_temp + temp)/2
                average_temp = str(average_temp)
            times = str(times)
            timestamp = str(timestamp)
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, current_temp, average_temp, row) VALUES ('"+times+"', '"+timestamp+"', "+current_temp+", "+average_temp+", "+row+")")
            mysql.commit()
        else:
            times = str(times)
            timestamp = str(timestamp)
            cursor3.execute("INSERT INTO "+cur[0]+"_data (time, timestamp, row) VALUES ('"+times+"', '"+timestamp+"', "+row+")")
            mysql.commit()
        
        if (float(times) > 1209600 and int(row) != 1):
            cursor3.execute("UPDATE "+cur[0]+" SET done = true WHERE done = false")
            mysql.commit()
            cursor3.execute("UPDATE All_Records SET done=true WHERE brew_name_time = '"+cur[0]+"'")
            mysql.commit()
    
    
    end = time.time()
    delay = delay + (end-start)
    if delay > 60:
        delay = 60
    time.sleep(sleepingtime-delay)
    delay = 0
    end_total = time.time()
    total_time = total_time + (end_total - start_total)