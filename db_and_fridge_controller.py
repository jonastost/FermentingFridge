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
cursor = mysql.cursor()
signal.signal(signal.SIGALRM, handler)
os.system('sudo /var/www/html/rfoutlet/codesend 4199731')
time.sleep(5)

current = True
reconnect = False
off = False
temp = 20
reconnections = 0
delay = 0

ubit.connect()
print("connected and trying to receive sensor information")
total_time = 0

while total_time < 1209600:
    start_total = time.time()
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
    end = time.time()
    delay = delay + (end-start)
    if delay > 60:
        delay = 60
    time.sleep(sleepingtime-delay)
    delay = 0
    end_total = time.time()
    total_time = total_time + (end_total - start_total)
print("Two weeks have now passed! Time to bottle or brew a new batch!")
print("There have been ", reconnections, " reconnections during this brew.")

ubit.disconnect()
