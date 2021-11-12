##################################################################
# Name: Ryan Erbelding
# Description: GUI and control for a robot arm
##################################################################
import RPi.GPIO as GPIO
from tkinter import *
from time import sleep


class Gui(Canvas):
    def __init__(self, master):
        # super that uses the super class of Canvas from Tkinter
        super().__init__(master, bg="white", width="800", height="800")
        # creates the title at the top of the GUI
        t = Label(master, text='ATLAS V1', font=('Arial', 25))
        master.attributes('-fullscreen', True)
        t.pack()        

    # function that creates the sliders and the buttons of the GUI
    def makeSliders(self, master):
        super().__init__(master)

        # creating the sliders and setting their positions
        w1 = Scale(master, from_=180, to=0, length=150, bg='red')
        w1.place(x=100, y=200)
        w2 = Scale(master, from_=180, to=0, length=150, bg='red')
        w2.place(x=200, y=200)
        w3 = Scale(master, from_=180, to=0, length=150, bg='red')
        w3.place(x=300, y=200)
        w4 = Button(master, text = '90*',
                    command=lambda: Movement.rotateWrist())
        w4.place(x=400, y=150)
        w5 = Button(master, text = 'Up',
                    command = lambda: Movement.moveServo(0, wrist_serv))
        w5.place(x=500, y=100)
        w6 = Button(master, text = 'Forward',
                    command = lambda: Movement.moveServo(90, wrist_serv))
        w6.place(x=600, y=150)
        w7 = Button(master, text = 'Down',
                    command = lambda: Movement.moveServo(180, wrist_serv))
        w7.place(x=500, y=200)
        w8 = Button(master, text = 'Open',
                    command=lambda: Movement.moveServo(120, hand_serv))
        w8.place(x = 500, y = 300)
        w9 = Button(master, text = 'Close',
                    command = lambda:Movement.moveServo(0, hand_serv))
        w9.place(x=500,y=400)
        w2.set(150)
        w3.set(170)
        # creating the button to move the arm after parameters are set using the movement class
        btn = Button(master, text='Move',
                     command=lambda: Movement.buttonClick(w1.get(), w2.get(), w3.get()))
        btn.place(x=100, y=100)

        # a second button added to make resetting the robot arm to base position easier
        btn1 = Button(master, text='Reset',
                      command=lambda: reset())
        btn1.place(x=200, y=100)

        # packing the GUI
        self.pack()

        # function that resets the arm
        def reset():
            global wrist
            # sets the sliders to zero
            w1.set(0)
            w2.set(150)
            w3.set(170)
            # resets the position of the motor
            Movement.moveServo(0, rotator_serv)
            Movement.moveServo(150, shoulder_serv)
            Movement.moveServo(170, elbow_serv)
            Movement.moveServo(140, wristRot_serv)
            Movement.moveServo(0, wrist_serv)
            Movement.moveServo(120, hand_serv)
            wrist = True
# class that holds all of the movement functionality
class Movement:
    def __init__(self):
        self.rotator_serv = rotator_serv
        self.shoulder_serv = shoulder_serv
        self.elbow_serv = elbow_serv
        self.wristRot_serv = wristRot_serv
        self.wrist_serv = wrist_serv
        self.hand_serv = hand_serv

    # function that is called when the Move button is clicked that moves each of the arms individually
    def buttonClick(w1, w2, w3):
        print("w1 = {}, w2 = {}, w3 = {}".format(w1, w2, w3))
        Movement.moveServo(w1, rotator_serv)

        Movement.moveServo(w2, shoulder_serv)

        Movement.moveServo(w3, elbow_serv)
        

    # function that moves the shoulder using degree to duty conversion and inputing it
    def moveServo(angle, servo):
        if angle >= 180:
            angle = 179
  
        
        duty = angle // 18 + 3
        servo.ChangeDutyCycle(duty)
        sleep(1.5)
        if servo == shoulder_serv:
            pass
        else:
            servo.ChangeDutyCycle(0)
        
    def rotateWrist():
        global wrist
        if wrist == True:
            Movement.moveServo(50, wristRot_serv)
            
            wrist = False
        else:
            Movement.moveServo(140, wristRot_serv)            
            wrist = True
    
"""
#############################################################
################        MAIN CODE         ###################
#############################################################
"""

############################################################
#################    CONTROL SETUP      ####################
############################################################
GPIO.setwarnings(False)
wrist = True
# setting the GPIO pins to each of the arm servos
rotator_pin = 17
shoulder_pin = 13
elbow_pin = 6
wristRot_pin = 4
wrist_pin = 18
hand_pin = 20

# GPIO setmode
GPIO.setmode(GPIO.BCM)

# setting up each pin as an output
GPIO.setup(rotator_pin, GPIO.OUT)
GPIO.setup(shoulder_pin, GPIO.OUT)
GPIO.setup(elbow_pin, GPIO.OUT)
GPIO.setup(wristRot_pin, GPIO.OUT)
GPIO.setup(wrist_pin, GPIO.OUT)
GPIO.setup(hand_pin, GPIO.OUT)

# setting up the servos signal to 50Hz and start
rotator_serv = GPIO.PWM(rotator_pin, 50)
shoulder_serv = GPIO.PWM(shoulder_pin, 50)
elbow_serv = GPIO.PWM(elbow_pin, 50)
wristRot_serv = GPIO.PWM(wristRot_pin, 50)
wrist_serv = GPIO.PWM(wrist_pin, 50)
hand_serv = GPIO.PWM(hand_pin, 50)

# starting servos
rotator_serv.start(0)
shoulder_serv.start(0)
elbow_serv.start(0)
wristRot_serv.start(0)
wrist_serv.start(0)
hand_serv.start(0)

# setting servos to a default position when program is started
Movement.moveServo(0, rotator_serv)
Movement.moveServo(150, shoulder_serv)
Movement.moveServo(170, elbow_serv)
Movement.moveServo(140, wristRot_serv)
Movement.moveServo(0, wrist_serv)
Movement.moveServo(120, hand_serv)

#############################################################
#################      GUI SETUP    #########################
#############################################################

# sets the width and height of the GUI
WIDTH = 800
HEIGHT = 800

# create the window
window = Tk()
window.geometry("{}x{}".format(WIDTH, HEIGHT))
window.title("ATLAS V1")

# create the coordinate system as a Tkinter canvas inside the window
s = Gui(window)
s.makeSliders(window)
print(s.makeSliders(window))
# print(Movement(s.makeSliders(window)))
window.mainloop()
