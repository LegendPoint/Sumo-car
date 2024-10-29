import RPi.GPIO as GPIO
from time import sleep
import time
#1.Start
#2.Search
#3.Attack
#4.Back Off
LeftSensor = 19
CenterSensor = 21
RightSensor = 22
in1 = 16
in2 = 18
in3 = 40
in4 = 38
#send waves to object (output)
trig = 11
#recieve pulses from object (input)
echo = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(trig,GPIO.OUT)

GPIO.setup(LeftSensor,GPIO.IN)
GPIO.setup(CenterSensor,GPIO.IN)
GPIO.setup(RightSensor,GPIO.IN)
GPIO.setup(echo,GPIO.IN)


#initial
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(trig,GPIO.LOW)



p1=GPIO.PWM(in1,1000)
p2=GPIO.PWM(in2,1000)
p3=GPIO.PWM(in3,1000)
p4=GPIO.PWM(in4,1000)
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

def attack():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    
def backward():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    
def turnAround():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    
        
def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
def pin_check():
    while True:
        print(str(GPIO.input(echo)))
        sleep(1)
        

def measure_distance():
     GPIO.output(trig,GPIO.HIGH)
     sleep(0.00001)
     GPIO.output(trig,GPIO.LOW)
     start_time = time.time()
     end_time = time.time()
     print("here")
     while GPIO.input(echo) == 0:
         GPIO.output(trig,GPIO.HIGH)
         GPIO.output(trig,GPIO.LOW)
         start_time = time.time()
         #print("or this ome")
     while GPIO.input(echo) == 1:
         GPIO.output(trig,GPIO.HIGH)
         GPIO.output(trig,GPIO.LOW)
         end_time = time.time()
         #print("this one")
     #calculate duration
     duration = end_time-start_time
     distance = duration*(34300/2)
     print("Distance : ",distance," cm")
     return distance
#         
#     #calculate distance in cm
    
def Search(distance):  
    while True:
        if GPIO.input(echo)==0 :
            print("turn around")
            turnAround()
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(50)
            p3.ChangeDutyCycle(50)
            p4.ChangeDutyCycle(0)
            continue
        elif GPIO.input(echo)==1 :
            #safe distance
            if distance < 30 :
                stop()
                p1.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(0)
                p3.ChangeDutyCycle(0)
                p4.ChangeDutyCycle(0)
                break
    print("Attack")
    attack()
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(100)
    p4.ChangeDutyCycle(0)

def DetectWhite():
    while True:
        if not GPIO.input(LeftSensor)==1 and GPIO.input(CenterSensor)==1 and GPIO.input(RightSensor)==1:
            stop()
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
            p3.ChangeDutyCycle(0)
            p4.ChangeDutyCycle(0)
            backward()
            print("detect white")
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(100)
            p3.ChangeDutyCycle(0)
            p4.ChangeDutyCycle(100)
            sleep(0.3)
        else :
            sleep(0.1)
            break


while True:
    '''if GPIO.input(LeftSensor)==0 and GPIO.input(CenterSensor)==0 and GPIO.input(RightSensor)==0:
        print("stop, found white 3")
        stop()
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)
        break'''
    distance = measure_distance()
    if distance > 60 :
        print("turn around")
        turnAround()
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(100)
        p3.ChangeDutyCycle(100)
        p4.ChangeDutyCycle(0)
        #continue
            #safe distance
    else:
        print("Attack")
        stop()
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)
        attack()
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(100)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(100)
            #calculate duration

            #sleep(0.00001)
        #Search(distance)
    
    print("end")


GPIO.cleanup()
