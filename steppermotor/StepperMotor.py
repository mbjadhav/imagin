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

Direction To parking -
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

		self.Xmin = 9 #actually pin max
		self.Xmax = 10 #not assigned pin
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

	def sourceSecure(self):
		print("Parking radiation source in source holder")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor
		
		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymin)==1:
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
		while GPIO.input(self.Xmax)==1:
			GPIO.output(self.StepX, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepX, GPIO.LOW)
			sleep(self.Delay)
		
		GPIO.output(self.DirectionY, self.ANTI_CLOCKWISE)
		while GPIO.input(self.Ymax)==1:
			GPIO.output(self.StepY, GPIO.HIGH)
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)
		
		GPIO.output(self.EnableW, GPIO.HIGH)   #w-motor
		GPIO.output(self.EnableY, GPIO.HIGH)	#y-motor 
		GPIO.output(self.EnableX, GPIO.HIGH)	#x-motor
	
	def sourcePrepare(self):
		print("Preparing for source scan")

		# Hard set motor pins for parking
		GPIO.output(self.EnableW, GPIO.LOW)   #w-motor
		GPIO.output(self.EnableY, GPIO.LOW)	#y-motor 
		GPIO.output(self.EnableX, GPIO.LOW)	#x-motor

		GPIO.output(self.DirectionY, self.CLOCKWISE)
		while GPIO.input(self.Ymin)==1:
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
		while GPIO.input(self.Xmax)==1:
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
			if enablePin == self.EnableY and GPIO.input(self.Ymin)==0 and direction == 1:
				print("Y directional movement out of bound")
				break
			elif enablePin == self.EnableY and GPIO.input(self.Ymax)==0 and direction == 0:
				print("Y directional movement out of bound")
				break
			elif enablePin == self.EnableX and GPIO.input(self.Xmin)==0 and direction == 1:
				print("X directional movement out of bound")
				break
			elif enablePin == self.EnableX and GPIO.input(self.Xmax)==0 and direction == 0:
				print("X directional movement out of bound")
				break
			elif enablePin == self.EnableW and GPIO.input(self.Wmin)==0 and direction == 1:
				print("W directional movement out of bound")
				break
			elif enablePin == self.EnableW and GPIO.input(self.Wmax)==0 and direction == 0:
				print("W directional movement out of bound")
				break

	def moveY(self, stepsToTake, direction = __CLOCKWISE):

		print("Y Step Pin: " + str(self.StepY) + " Direction Pin: " + str(self.DirectionY) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(self.EnableY, GPIO.LOW)
		GPIO.output(self.DirectionY, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
		    #print("Step " + str(x))
			GPIO.output(self.StepY, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(self.StepY, GPIO.LOW)
			sleep(self.Delay)
			if GPIO.input(self.Ymin)==0 and direction == 1:
				print("Y directional movement out of bound")
				break
			elif GPIO.input(self.Ymax)==0 and direction == 0:
				print("Y directional movement out of bound")
				break
	
	def moveX(self, stepsToTake, direction = __ANTI_CLOCKWISE):
		
		print("X Step Pin: " + str(self.StepX) + " Direction Pin: " + str(self.DirectionX) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(self.EnableX, GPIO.LOW)
		GPIO.output(self.DirectionX, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
		    #print("Step " + str(x))
			GPIO.output(self.StepX, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(self.StepX, GPIO.LOW)
			sleep(self.Delay)
			if GPIO.input(self.Xmin)==0 and direction == 1:
				print("X directional movement out of bound")
				break
			elif GPIO.input(self.Xmax)==0 and direction == 0:
				print("X directional movement out of bound")
				break

	def moveW(self, stepsToTake, direction = __ANTI_CLOCKWISE):
		
		print("W Step Pin: " + str(self.StepW) + " Direction Pin: " + str(self.DirectionW) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(self.EnableW, GPIO.LOW)
		GPIO.output(self.DirectionW, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
		    #print("Step " + str(x))
			GPIO.output(self.StepW, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(self.StepW, GPIO.LOW)
			sleep(self.Delay)
			if GPIO.input(self.Wmin)==0 and direction == 1:
				print("W directional movement out of bound")
				break
			elif GPIO.input(self.Wmax)==0 and direction == 0:
				print("W directional movement out of bound")
				break

	def move2Chip1(self):
		
		print("Moving Sr90 radiation source with activity 37 MBq to Chip-1")
		self.sourcePrepare()
		self.moveW(850, 0)
		self.moveX(9000, 1)
		self.moveY(6000, 0)# Set the direction
		
	def move2Chip2(self):
		
		print("Moving Sr90 radiation source with activity 37 MBq to Chip-2")
		self.sourcePrepare()
		self.moveW(850, 0)
		self.moveX(5500, 1)
		self.moveY(6000, 0)# Set the direction

	def move2Chip3(self):
		
		print("Moving Sr90 radiation source with activity 37 MBq to Chip-3")
		self.sourcePrepare()
		self.moveW(540, 0)
		self.moveX(20000, 1)
		self.moveY(6000, 0)# Set the direction

	def move2Chip4(self):
		
		print("Moving Sr90 radiation source with activity 37 MBq to Chip-4")
		self.sourcePrepare()
		self.moveW(540, 0)
		self.moveX(23500, 1)
		self.moveY(6000, 0)# Set the direction

	def move2QuadCenter(self):
		
		print("Moving Sr90 radiation source with activity 37 MBq to Quad Center")
		self.sourcePrepare()
		self.moveW(600, 0)
		self.moveX(19000, 1)
		self.moveY(6000, 0)# Set the direction
