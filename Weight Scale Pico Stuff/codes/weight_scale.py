from machine import Pin
import utime

SCK = Pin(6, Pin.OUT)

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

a = 4.5573*10**(-5)
b = -376.44

with open("test.txt", "w") as data_file:
    data_file.write("Date, Time, Weight\n")

    while (1):
        fake_time = 0
        weight = readCount()
        weight = a * weight + b
        result = round(weight, 3)
        text = "1,"+str(fake_time)+", "+str(weight)+"\n"
        print("weight:", weight)
        fake_time += 1
        data_file.write(text)
        data_file.flush()
        utime.sleep(1)
    

