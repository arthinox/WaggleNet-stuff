from machine import Pin
import utime

SCK = Pin(6, Pin.OUT)
switch = Pin(18, Pin.IN)
LED = Pin(13, Pin.OUT)

def readCount():
    
    i = 0
    Count = 0
    
    DT = Pin(5, Pin.OUT)
    DT.high()
    DT.low()
    DT = Pin(5, Pin.IN)

    while DT.value() == 1:
        i = 0
    
    for i in range(24):
        SCK.high()
        Count = Count << 1
        SCK.low()
        
        if DT.value() == 1:
            Count += 1
    
    SCK.high()
    Count = Count ^ 0x800000
    SCK.low()
    return Count

'''
print("Please remove anything on the weight scale: (press enter to continue)")
c = input("")
x1 = readCount()
y1 = 0
print("Please put some weight on the weight scale (kg):")
y2 = float(input(""))
x2 = readCount()

a = (y2-y1)/(x2-x1)
b = y1 - a*x1
'''

a = -4.482101*10**(-5)
b = 381.3089

rtc = machine.RTC()

with open("test.txt", "w") as data_file:
    data_file.write("Date, Time, Weight\n")

    while (1):
        timestamp = rtc.datetime()
        fake_time = 0
        weight = readCount()
        weight = a * weight + b
        result = round(weight, 3)
        print("weight:", weight)        
        timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
        data_file.write(timestring + "," + str(weight) + "\n")        
        data_file.flush()
        utime.sleep(1)
