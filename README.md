# IMAGIN
Itkpix Module Automated testinG INfrastructure

This project will have all the required scripts for the automatization of testing setup 

import links

https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git

https://github.com/cli/cli/blob/trunk/docs/install_linux.md

Always a first steps -

*git pull*

and end with - 

*git push*

# I2C
To check I2C bus -

*sudo i2cdetect -y 1*

*sudo i2cdetect -l*

I2C bus for this setup -

Relay Boards - 0x28

SHT sensor - 0x44

## These scripts will monitor the values 

    Air Temperture, Humidity, and Dew Point using SHT sensor
    Chuck Tempature using PT100 
    Module Temprature using NTC on flex
    Pressure switch 
    Vaccum switch
    Lid switch
