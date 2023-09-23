import RPi.GPIO as gpio

import time

import csv

from datetime import datetime

from datetime import date


# GPIO on Pi
DT = 5
SCK= 6

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(SCK, gpio.OUT)

# output of count without connecting the load cell, can use it to tare

def readCount():

  i=0
  Count=0

 # print Count
 # time.sleep(0.001)

  gpio.setup(DT, gpio.OUT)
  gpio.output(DT,1)
  gpio.output(SCK,0)
  gpio.setup(DT, gpio.IN)

  while gpio.input(DT) == 1:

      i=0

  for i in range(24):

        gpio.output(SCK,1)        


        Count = Count<<1


        gpio.output(SCK,0)

        #time.sleep(0.001)

        if gpio.input(DT) == 0: 

            Count=Count+1

            #print Count

        

  gpio.output(SCK,1)

  Count=Count^0x800000 # xor = ^

  #time.sleep(0.001)

  gpio.output(SCK,0)

  return Count



#### Write to csv ####\


print("Please remove anything on the weight scale: (press enter to continue)")
c = input("")
x1 = readCount()
y1 = 0
print("Please put some weight on the weight scale (kg):")
y2 = float(input(""))
x2 = readCount()

a = (y2-y1)/(x2-x1)
b = y1 - a*x1


with open('raw_data.csv', 'w') as csvfile:
    
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Date', 'Time', 'Weight'])
    
    while 1:

        curr_date = date.today()
        
        time_now = datetime.now()
        
        curr_time = time_now.strftime("%H:%M:%S")
        
        count = readCount()

        w = count * a + b
        
        result = round(w, 3)

        print("Weight: ", result, "kg")
        
        filewriter.writerow([curr_date, curr_time, result])
        
        csvfile.flush()

        time.sleep(0.5)
        

