import RPi.GPIO as GPIO
from time import sleep

class StepperHandler():
	
	__CLOCKWISE = 1
	__ANTI_CLOCKWISE = 0
	
	def __init__(self, enablePin, stepPin, directionPin, delay=0.208, stepsPerRevolution=200):
		
		# Configure instance
		self.CLOCKWISE = self.__CLOCKWISE
		self.ANTI_CLOCKWISE = self.__ANTI_CLOCKWISE
		self.EnablePin = enablePin
		self.StepPin = stepPin
		self.DirectionPin = directionPin
		self.Delay = delay
		self.RevolutionSteps = stepsPerRevolution
		self.CurrentDirection = self.CLOCKWISE
		self.CurrentStep = 0

		# Setup gpio pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.StepPin, GPIO.OUT)
		GPIO.setup(self.EnablePin, GPIO.OUT)
		GPIO.setup(self.DirectionPin, GPIO.OUT)

	def Step(self, stepsToTake, direction = __CLOCKWISE):
		print("Step Pin: " + str(self.StepPin) + " Direction Pin: " + str(self.DirectionPin) + " Delay: " + str(self.Delay))
		print("Taking " + str(stepsToTake) + " steps.")

		# Set the direction
		GPIO.output(self.EnablePin, GPIO.LOW)
		GPIO.output(self.DirectionPin, direction)

		# Take requested number of steps
		for x in range(stepsToTake):
			print("Step " + str(x))
			GPIO.output(self.StepPin, GPIO.HIGH)
			self.CurrentStep += 1
			sleep(self.Delay)
			GPIO.output(self.StepPin, GPIO.LOW)
			sleep(self.Delay)
			
		GPIO.output(self.EnablePin, GPIO.HIGH)

# Define pins
ENABLE_PIN = 14
STEP_PIN = 15
DIRECTION_PIN = 18

# Create a new instance of our stepper class (note if you're just starting out with this you're probably better off using a delay of ~0.1)
stepperHandler = StepperHandler(ENABLE_PIN, STEP_PIN, DIRECTION_PIN, 0.005)

# Go forwards once
stepperHandler.Step(400)

# Go backwards once
stepperHandler.Step(400, stepperHandler.ANTI_CLOCKWISE)
