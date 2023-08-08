import RPi.GPIO as GPIO
from time import sleep

import argparse
parser = argparse.ArgumentParser(description = "")
parser.add_argument('--flyingtime', '-t', help='time in second', action='store', default='10')
args = parser.parse_args()

'''
motor pins
En0 14
St0 15
Dir0 18
min0 4
max0 17
-----
En1 23
St1 24
Dir1 25
min1 27
max1 22
-----
En2 16
St2 20
Dir2 21
min2    currently using pin GPIO 10 for min 
max2 10 not using max as pin gpio 10 is used for min

Direction To Origin -
x-motor: anti-clockwise
y-motor: anti-clockwise
w-motor: clockwise 

'''

class StepperMotor():
	
	__CLOCKWISE = 1
	__ANTI_CLOCKWISE = 0
	
	def __init__(self,  delay=0.208, stepsPerRevolution=20):
		
		# Configure instance
		self.CLOCKWISE = self.__CLOCKWISE
		self.ANTI_CLOCKWISE = self.__ANTI_CLOCKWISE
		self.Delay = delay
		self.RevolutionSteps = stepsPerRevolution
		self.CurrentDirection = self.CLOCKWISE
		self.CurrentStep = 0

		self.EnableX = 16
		self.StepX = 20
		self.DirectionX = 21
		self.EnableY = 23
		self.StepY = 24
		self.DirectionY = 25
		self.EnableW = 14
		self.StepW = 15
		self.DirectionW = 18

		self.Xmin = 10 #actually pin max
		self.Xmax = 9  #not assigned pin
		self.Ymin = 27
		self.Ymax = 22
		self.Wmin = 4
		self.Wmax = 17

		self.MotorChannels = (self.EnableX, self.StepX, self.DirectionX, self.EnableY, self.StepY, self.DirectionY,self.EnableW, self.StepW, self.DirectionW)
		self.MotorLimitChannels = (self.Xmin, self.Xmax, self.Ymin, self.Ymax, self.Wmin, self.Wmax)

		# Setup gpio pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(self.MotorChannels, GPIO.OUT)
		GPIO.setup(self.MotorLimitChannels, GPIO.IN)

	def set_parking(self):
		print("Parking radiation source in source holder")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor

		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymax)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionW, self.CLOCKWISE)
		while GPIO.input(self.Wmin)==1:
			GPIO.output(self.StepW, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepW, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionX, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Xmin)==1:
			GPIO.output(self.StepX, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepX, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionY, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Ymin)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.EnableW, GPIO.HIGH)   #w-motor
		GPIO.output(self.EnableY, GPIO.HIGH)	#y-motor 
		GPIO.output(self.EnableX, GPIO.HIGH)	#x-motor
	
	def get_ready(self):
		print("Getting Ready for source scan")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor

		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymax)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionW, self.CLOCKWISE)
		while GPIO.input(self.Wmin)==1:
			GPIO.output(self.StepW, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepW, GPIO.LOW)
			sleep(self.Delay)

		GPIO.output(self.DirectionX, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Xmin)==1:
			GPIO.output(self.StepX, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepX, GPIO.LOW)
			sleep(self.Delay)

	def step(self, enablePin, stepPin, directionPin, stepsToTake, direction = __CLOCKWISE):
		
		GPIO.setup(stepPin, GPIO.OUT)
		GPIO.setup(enablePin, GPIO.OUT)
		GPIO.setup(directionPin, GPIO.OUT)

		print("Step Pin: " + str(stepPin) + " Direction Pin: " + str(directionPin) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(enablePin, GPIO.LOW)
		GPIO.output(directionPin, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
		    #print("Step " + str(x))
			GPIO.output(stepPin, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(stepPin, GPIO.LOW)
			sleep(self.Delay)

		#GPIO.output(senablePin, GPIO.HIGH)

# Define pins
ENABLE_PIN = 14
STEP_PIN = 15
DIRECTION_PIN = 18

stepperHandler = StepperMotor(0.001)
# Create a new instance of our stepper class (note if you're just starting out with this you're probably better off using a delay of ~0.1)
stepperHandler.get_ready()
# Go forwards once
#stepperHandler.Step(100)
stepperHandler.step(ENABLE_PIN, STEP_PIN, DIRECTION_PIN, 900, stepperHandler.ANTI_CLOCKWISE)
stepperHandler.step(23, 24, 25, 2000, stepperHandler.ANTI_CLOCKWISE)
sleep(float(args.flyingtime))
stepperHandler.set_parking()
# Go backwards once
#stepperHandler.Step(100, stepperHandler.ANTI_CLOCKWISE)
