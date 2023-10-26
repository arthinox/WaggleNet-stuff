#"module" is not the final name for this interface
#every data generating device (camera, microphone, thermometer) 
#should have its own module class which implements setup and
#poll functions

import random
import time

#dummy class representing a generic sensor, not required
class exampleSensor():
    def read_data(self):
        data = [random.randint(0, 9999) for i in range(0, 10)]
        return data

class exampleModule():
    module_name = "example" #put the name of your sensor/project here
    sensor = None
    polling_interval = .5 #time between polls in seconds
    last_poll = time.monotonic()

    def __init__(self):
        print(f"instance of {self.module_name} created")

    def setup(self):
        SCK = digitalio.DigitalInOut(board.GP6)
        SCK.direction = digitalio.Direction.OUTPUT

        LED = digitalio.DigitalInOut(board.GP13)
        LED.direction = digitalio.Direction.OUTPUT
        LED.value = 0

        DT = digitalio.DigitalInOut(board.GP5)
    
    def readCount():
        i = 0
        Count = 0
        
        # DT = Pin(5, Pin.OUT)
        
        DT.direction = digitalio.Direction.OUTPUT
        DT.value = 1
        DT.value = 0
        # DT = Pin(5, Pin.IN)
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


#don't need to modify this
    def wrap_poll(self):
        if ((time.monotonic() - self.last_poll) > self.polling_interval):
            self.last_poll = time.monotonic()
            return self.poll()
        return None


    def poll(self):
        a = -4.482101*10**(-5)
        b = 381.3089

        switch = digitalio.DigitalInOut(board.GP18)

        switch.switch_to_input(pull=digitalio.Pull.DOWN)

        state = 1

        print("Flip switch to start.")

        while (state == 1):
            if switch.value == True:
                print("Remove any objects on the scale.")
                while (switch.value == True):
                    LED.value = 1
                    time.sleep(0.15)
                    LED.value = 0
                    time.sleep(0.15)
                state = 0
                break
            time.sleep(0.15)

        while (state == 0):
            LED.value = 0
            if switch.value == True:
                # Read zero weight data here
                print("Place weight on scale.")
                while (switch.value == True):
                    LED.value = 1
                    time.sleep(0.15)
                    LED.value = 0
                    time.sleep(0.15)
                state = 1
                break
            time.sleep(0.15)

        while (state == 1):
            LED.value = 1
            if switch.value == True:
                # Read calibration weight and calculate factor
                print("Flip switch to continue.")
                while (switch.value == True):
                    LED.value = 1
                    time.sleep(0.15)
                    LED.value = 0
                    time.sleep(0.15)
                state = 0
                break
            time.sleep(0.15)

        sampling_interval = 5
        weights = []

        LED.value = 0
        with open("test.txt", "w") as data_file:
            data_file.write("Date, Time, Weight\n")

            while (1):
                weight = readCount()
                weight = a * weight + b
                result = round(weight, 3)
                weights.append(result)
                print("weight:", weight)
                if len(weights) == sampling_interval:
                    weights.sort()
                    weight = weights[sampling_interval // 2]
                    timestring = time.localtime()
                    month = timestring[1]
                    day  = timestring[2]
                    hour  = timestring[3]
                    minute  = timestring[4]
                    sec  = timestring[5]
                    timestring1 = str(month) + "/" + str(day) + "," + str(hour) + ":" + str(minute) + ":" + str(sec)
                    data_file.write(timestring1 + "," + str(weight) + "\n")        
                    data_file.flush()
                    weights = []
                time.sleep(1)

