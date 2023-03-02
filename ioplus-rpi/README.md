[![ioplus-rpi](res/sequent.jpg)](https://www.sequentmicrosystems.com)

# ioplus-rpi

Command Line, Python, and Node-Red for [Home Automation Stackable Card for Raspberry Pi](https://sequentmicrosystems.com/products/raspberry-pi-home-automation-card)

![IO-PLUS](res/IO-PLUS.jpg)

## Setup

Enable Raspberry Pi I2C communication by opening a terminal and typing:
```bash
~$ sudo raspi-config
```
Go to the *Interface Options* menu then *I2C* and enable the port.

## Usage

```bash
~$ git clone https://github.com/SequentMicrosystems/ioplus-rpi.git
~$ cd ioplus-rpi/
~/ioplus-rpi$ sudo make install
```

Now you can access all the functions of the relays board through the command "ioplus". Use -h option for help:
```bash
~$ ioplus -h
```

If you clone the repository any update can be made with the following commands:

```bash
~$ cd ioplus-rpi/  
~/ioplus-rpi$ git pull
~/ioplus-rpi$ sudo make install
``` 

## Commands

	-v		Display the ioplus command version number
	-h		Display the list of command options or one command option details
	-warranty	Display the warranty
	-pinout		Display the board io connector pinout
	-list:		List all ioplus boards connected,return the # of boards and stack level for every board
	board		Display the board status and firmware version number
	relwr:		Set relays On/Off
	relrd:		Read relays status
	reltest:	Turn ON and OFF the relays until press a key
	gpiowr:		Set gpio pins On/Off
	gpiord:		Read gpio status
	gpiodirwr:	Set gpio pins direction I/O  0- output; 1-input
	gpiodirrd:	Read gpio direction 0 - output; 1 - input
	gpioedgewr:	Set gpio pin counting edges  0- count disable; 1-count rising edges; 2 - count falling edges; 3 - count both edges
	gpioEdgerd:	Read gpio counting edges 0 - none; 1 - rising; 2 - falling; 3 - both
	gpiocntrd:	Read gpio edges count for one GPIO imput pin
	gpiocntrst:	Reset gpio edges count for one GPIO imput pin
	optrd:		Read optocoupled inputs status
	optedgerd:	Read optocoupled counting edges 0 - none; 1 - rising; 2 - falling; 3 - both
	optedgewr:	Set optocoupled channel counting edges  0- count disable; 1-count rising edges; 2 - count falling edges; 3 - count both edges
	optcntrd:	Read potocoupled inputs edges count for one pin
	optcntrst:	Reset optocoupled inputs edges count for one pin
	optencwr:	Enable / Disable optocoupled quadrature encoder, encoder 1 connected to opto ch1 and 2, encoder 2 on ch3 and 4 ... 
	optencrd:	Read optocoupled quadrature encoder state 0- disabled 1 - enabled
	optcntencrd:	Read potocoupled encoder count for one channel
	optcntencrst:	Reset optocoupled encoder count 
	odrd:		Read open drain output pwm value (0% - 100%)
	odwr:		Write open drain output pwm value (0% - 100%), Warning: This function change the output of the coresponded DAC channel
	dacrd:		Read DAC voltage value (0 - 10V)
	dacwr:		Write DAC output voltage value (0..10V), Warning: This function change the output of the coresponded open-drain channel
	adcrd:		Read ADC input voltage value (0 - 3.3V)
	adccal:		Calibrate one ADC channel, the calibration must be done in 2 points at min 2V apart
	adccalrst:	Reset the calibration for one ADC channel
	daccal:		Calibrate one DAC channel, the calibration must be done in 2 points at min 5V apart
	daccalrst:	Reset calibration for one DAC channel
	wdtr:		Reload the watchdog timer and enable the watchdog if is disabled
	wdtpwr:		Set the watchdog period in seconds, reload command must be issue in this interval to prevent Raspberry Pi power off
	wdtprd:		Get the watchdog period in seconds, reload command must be issue in this interval to prevent Raspberry Pi power off
	wdtipwr:	Set the watchdog initial period in seconds, This period is loaded after power cycle, giving Raspberry time to boot
	wdtiprd:	Get the watchdog initial period in seconds. This period is loaded after power cycle, giving Raspberry time to boot
	wdtopwr:	Set the watchdog off period in seconds (max 48 days), This is the time that watchdog mantain Raspberry turned off 
	wdtoprd:	Get the watchdog off period in seconds (max 48 days), This is the time that watchdog mantain Raspberry turned off 
	iotest:		Test the ioplus with loopback card inserted 
	pwmfrd:		Read open-drain pwm frequency in Hz 
	pwmfwr:		Write open dran output pwm frequency in Hz [10..64000]
