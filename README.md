# FermentingFridge
Software for a Raspberry Pi utilizing a MicroBit to control the temperature of a fridge, and sort data from a variety of fermentation projects

#Set-Up
1. Clone the repository. If running Raspbian and MuBit, make sure that serial connections are permitted.
2. If no Mubit is required, no hardware action is required. Skip to step 9 
3. If you have a microbit, there are two options (bluetooth and wired).
4. Avoid using bluetooth if possible, as this is unreliable. Google how to set up bluetooth betweem pi and microbit
5. If using wried, make sure pyserial is installed. Using Make Code, simply add the serial write number (with get temperature value) to the forever loop.
6. In a terminal type "ls /dev/ttyA*"
7. Plug microbit into pi and repeat step 6. The new file that pops up will be the one to remember
8. Copy this name into the serial Python script on line (57?) It should be obvious where
9. Install mysql (I used MariaDB) on your pi
10. Install Python mysql-connector
11. Move to the FermentingDatabase Repo and follow continued instructions.
