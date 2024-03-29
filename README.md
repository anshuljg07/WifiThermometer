# Wifi Thermometer w/ Node.js Webserver

![Passing](https://github.com/matplotlib/matplotlib/workflows/Tests/badge.svg)
![CodeQl Passing](https://github.com/tesseract-ocr/tesseract/workflows/CodeQL/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
--------------------------------------------------------------------------------
--------------------------------
<p float="center">
  <img src="https://github.com/anshuljg07/WifiThermometer/assets/72891464/22886ecd-c724-41ec-b6a8-af877e9926d1" width="400" height="365"alt='YaleSoM logo'/>
  <img src="https://github.com/anshuljg07/WifiThermometer/assets/72891464/e1b47a5d-66c5-4bf2-af56-bac0d4641ae6" width="400" height="365"alt="CTRA logo"/> 
</p>

This repository houses the source code for a Wifi Thermometer consisting of two major components: a RaspberryPi Model 4B and a Node.js Webserver. 

### Raspberry Pi component:
- Involves peripheral hardware: ZF RR switch, DS16203 pushbutton, a standard 16x2 LCD display, a mobile power supply, and most importantly the DS18B20 Temperature sensor
- These peripherals are managed by a python script local to the Pi, which also handles socket communication between the server
- Can be remotely controlled through an SSH for non-local sensing
- Processes data and sends through standard API utilizing JSON packets

### Node.js WebServer component:
- Robust implementation capable of future scaling (track multiple sensors)
- use of asynchronous sockets + socket rooms for multi-client communication
- Fully implemented Twilio API for SMS messages

### Dyanmic FrontEnd:
- Utilizes vanilla HTML/CSS/JS
- Utilizes real-time updating, resizable, and graph changing implementation of Chart.js
- Dropdown menu to input phone number, choose temp graph, and set temperature limits

# Getting Started
## Installing/Configuring Node.js
### Install Node.js
This is the download site for the [Node.js Installer](https://nodejs.org/en/), after downloading this you will be prompted to install Node.
```
node -v
```
This will confirm that node is installed, and it will tell you the node.js version. In addition the Node Pacakge Manager (npm) will be installed when Node is installed. Check the version:
```
npm -v
```
The node-modules folder and the package.json and the package-lock.json need to be recreated for every local creation of the project. The node-modules included in this repository may not work on your machine. Thus it is a good idea to recreate those. This is done by initializing a new Node project:
```
npm init
```
This should lead you through a set up script, and once that is all done the project's related files will be configured.
This project uses certain packages and running this command should install all of them:
```
npm install
```

## Configuring the RaspberryPi
The Raspberry Pi set up is not specially configured to this project and most tutorials touching on downloading Pi OS will suffice. The only special configuration was enabling the One-wire interface to communicates with the temperature sensor, which can be done through the settings.
Special Python packages need to be installed, which are listed in the import statments of the Temperature.py script.

## Contributors
This project was developed and is currently maintained by Joseph Bartosyck. Rafael Ragel de la Tejera, and Anshul Gowda

## Get in Contact:
 [Anshul Gowda's LinkedIn](https://www.linkedin.com/in/anshul-gowda)
<br />
Rafael Rangel de la Tejera's LinkedIn
<br />
Joseph Bartosyck's de la Tejera's LinkedIn
