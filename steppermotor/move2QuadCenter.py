from StepperMotor import StepperMotor

stepperHandler = StepperMotor(0.001)
# Create a new instance of our stepper class (note if you're just starting out with this you're probably better off using a delay of ~0.1)
stepperHandler.move2QuadCenter()
