import RPi.GPIO as gpio

import time

import csv

import datetime



DT = 5

SCK= 6


HIGH=1

LOW=0


sample=0

val=0


gpio.setwarnings(False)

gpio.setmode(gpio.BCM)


gpio.setup(SCK, gpio.OUT)



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

  Count=Count^0x800000

  #time.sleep(0.001)

  gpio.output(SCK,0)

  return Count  

with open('raw_data.csv', 'wb') as csvfile:
    
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['DateTime', 'Weight'])
    
    while 1:

        current_utc = datetime.utcnow()
        
        count = readCount()

        w = 0

        w = (count-sample)/106        # Accurate weight proportion

        print(w,"g")
        
        filewriter.writerow([current_utc, w])

        time.sleep(0.5)

