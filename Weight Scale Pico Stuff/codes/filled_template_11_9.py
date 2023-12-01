#"module" is not the final name for this interface
#every data generating device (camera, microphone, thermometer) 
#should have its own module class which implements setup and
#poll functions

import random
import time
import digitalio
import board

#dummy class representing a generic sensor, not required
class HX711():
    def read_data(self, DT, SCK):       
        i = 0
        Count = 0
        DT.direction = digitalio.Direction.OUTPUT
        DT.value = 1
        DT.value = 0
        DT.direction = digitalio.Direction.INPUT

        while DT.value == 1:
            i = 0
        
        for i in range(24):
            SCK.value = 1
            Count = Count << 1
            SCK.value = 0
            
            if DT.value == 1:
                Count += 1
        
        SCK.value = 1
        Count = Count ^ 0x800000
        SCK.value = 0
        return Count

class weighScale():
    module_name = "Weight Scale" #put the name of your sensor/project here
    
    polling_interval = .5 #time between polls in seconds
    last_poll = time.monotonic()
    
    

    def __init__(self):
        print(f"instance of {self.module_name} created")
        self.DT = digitalio.DigitalInOut(board.GP18)
        self.SCK = digitalio.DigitalInOut(board.GP19)
        self.LED = digitalio.DigitalInOut(board.GP20)
        self.switch = digitalio.DigitalInOut(board.GP21)
        self.a = 0
        self.b = 0
        self.sensor = HX711()

    def setup(self):
        
        
        self.SCK.direction = digitalio.Direction.OUTPUT

        
        self.LED.direction = digitalio.Direction.OUTPUT
        self.LED.value = 0

        
        self.a = -4.482101*10**(-5)
        self.b = 381.3089

        

        self.switch.switch_to_input(pull=digitalio.Pull.DOWN)

        state = 1
        x1, y1, x2, y2 = 0, 0, 0, 0

        print("Flip switch to start.")

        while (state == 1):
            if self.switch.value == True:
                print("Remove any objects on the scale.")
                while (self.switch.value == True):
                    self.LED.value = 1
                    time.sleep(0.15)
                    self.LED.value = 0
                    time.sleep(0.15)
                    x1 = self.sensor.read_data(self.DT, self.SCK)
                    
                state = 0
                break
            time.sleep(0.15)

        while (state == 0):
            self.LED.value = 0
            if self.switch.value == True:
                # Read zero weight data here
                print("Put weight on scale.")
                y2 = 2.518
                while (self.switch.value == True):
                    self.LED.value = 1
                    time.sleep(0.15)
                    self.LED.value = 0
                    time.sleep(0.15)
                    x2 = self.sensor.read_data(self.DT, self.SCK)
                    
                state = 1
                break
            time.sleep(0.15)

        while (state == 1):
            self.LED.value = 1
            if self.switch.value == True:
                # Read calibration weight and calculate factor
                print("Flip switch to continue.")
                while (self.switch.value == True):
                    self.LED.value = 1
                    time.sleep(0.15)
                    self.LED.value = 0
                    time.sleep(0.15)
                state = 0
                break
            time.sleep(0.15)

        

        self.LED.value = 0
        
        self.a = (y2-y1)/(x2-x1)
        self.b = y1 - self.a*x1
        
        # with open("test.txt", "w") as data_file:
        #     data_file.write("Date, Time, Weight\n")
        

#don't need to modify this
    def wrap_poll(self):
        if ((time.monotonic() - self.last_poll) > self.polling_interval):
            self.last_poll = time.monotonic()
            return self.poll()
        return None


    def poll(self):
        
        #with open("test.txt", "w") as data_file:
        sampling_interval = 5
        weights = []
        for i in range(sampling_interval):
            weight = self.sensor.read_data(self.DT, self.SCK)
            weight = self.a * weight + self.b
            result = round(weight, 3)
            weights.append(result)
        
        if len(weights) == sampling_interval:
            weights.sort()
            weight = weights[sampling_interval // 2]
            print("weight:", weight)
            timestring = time.localtime()
            month = timestring[1]
            day  = timestring[2]
            hour  = timestring[3]
            minute  = timestring[4]
            sec  = timestring[5]
            timestring1 = str(month) + "/" + str(day) + "," + str(hour) + ":" + str(minute) + ":" + str(sec) + "," + str(weight) + "\n"
            # data_file.write(timestring1 + "," + str(weight) + "\n")        
            # data_file.flush()
            weights = []
            return timestring1


