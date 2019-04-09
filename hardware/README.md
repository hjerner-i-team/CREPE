# Rock, Paper, Scissors demonstration
A demonstration of the CREPE communication framwork utilizing hardware, sensor data and network communications. 



### Intention
This demonstration is a simple example use case of the CREPE framework, demonstrating how CREPE allows for seemless and effortless experimentation with biological neurons. 

The demo setup will capture the IR profile of a rock/paper/scissor and trasnmitt this in json format through wifi to CREPE. CREPE will communcate the data further to the biological neurons, interpretate the results and transmitt these back to the demo setup, which will display the result on a display. 


### Setup of demo, physical components and configuraton

**Components:**
- Raspberry Pi Model 3 B+
  - [Product Info](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- Generic Powerbank (2.1A output)
- Arduino Uno       
  - [Datasheet](https://www.terraelectronica.ru/pdf/show?pdf_file=%2Fz%2FDatasheet%2FU%2FUNO_R3(CH340G).pdf&fbclid=IwAR2FrlMjTS1hMZOYdpzgNwjVe-th5LTBIL-3l3MgKYxddCArinXqffufGAc)
- ESP8266 (ESP-01) module (Wifi module)
  - [Datasheet](http://wiki.ai-thinker.com/_media/esp8266/docs/a001ps01a2_esp-01_product_specification_v1.2.pdf?fbclid=IwAR2E6Dpguf-HQLodjZ8DdVEVA4pAAcRWWhqb_sUmmcb46i1hmuMgdBjYaW4)
- Adafruit AMG8833   (IR-sensor)
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-amg8833-8x8-thermal-camera-sensor.pdf?timestamp=1552457921)
- Adafruit 1.44" Color TFT LCD Display 
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-44-color-tft-with-micro-sd-socket.pdf?timestamp=1552457427)

**Overview of complete setup:**
The harware is mounted inside a 3D printed container, powered by a power bank also mounted inside. A 1.44" TFT LCD dislay is mounted on he exterior of the container. The AMG8833 IR-sensor is mounted in the interior of the box, capturing data through a slot in the box. An adjustable plate is attached to the bottom of the container. This plate is equipped with a button, registering the hand of the subject. This button is connected to the Arduino.

**Raspberry Pi: setup**
The Arduino Uno is through a PCB shield equipped with the IR-sensor, wifi module and the LCD Display. It captures the IR profile of a rock/paper/scissor and transmits this to CREPE in json format. Results recieved from CREPE are displayed on the display. Capturing of data is triggered by the button mounted on the adjustable plate. 

### Requisites 
- The Arduino Uno used is an un-official Arduino. It requires an USB-driver to connect to Windows. [Driver link]()

### Installation

"Plug an play repository. To recreate this demonstration, Download the repository and follow instructions given in comments on each source file. Clone to Raspberry Pi. All code in this repository is intended to run on the Raspberry Pi 3 B+.
A step by step series of examples that tell you how to get a development env running"

Enter the Raspberry Pi configuration tool and enable SPI and I2C to enable use of the GPIO pins to communicate with the AMG8833 IR sensor and the LCD display. Enable SSH and/or VNC if you wish to remotely control the Raspberry Pi. 
```
sudo raspi-config --> enable SPI, I2C, SSH, VNC.
```

Copy the file main.py and the folder "graphics" onto the desktop of your Raspberry Pi. 
OPTIONAL: Copy the file main_with_visualization.py onto the desktop of your Raspberry Pi. This version is used for debugging, but will display a human-interpretable, interpolated image of the IR data collected by the sensor.

Installing Adafruit's Python library for the AMG8833 IR sensor.
```
sudo pip3 install adafruit-circuitpython-amg88xx
```

Installing ["Adafruit" ST7735R Library](https://github.com/KYDronePilot/Adafruit_ST7735r). This is an unofficial library derived from another official Adafruit LCD driver library. The motivation behind the use of this library is due to that the LCD display used in this project was originally intended for use with an Arduino, and thus the official Adafruit libraries are written for Arduino.  changed to enable use of the ST7735R LDC driver with Raspberry Pi. 

```
sudo apt-get install build-essential python-dev python-smbus python-pip python-imaging python-numpy
sudo pip3 install RPi.GPIO
clone https://github.com/KYDronePilot/Adafruit_ST7735r
sudo python3 setup.py install (in the cloned git repository)
```

Create systemd unit to enable the main python script to run on boot. This configuration will also restart the script in the event of a failure. This [tutorial](https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/) can be used as reference if something goes wrong.
```
sudo nano /lib/systemd/system/CREPE.service
```

```
[Unit]
Description=CREPE Hardware Example

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
Environment=PYTHONUNBUFFERED=1
ExecStart=/bin/bash -c '/usr/bin/python3 /home/pi/Desktop/main.py > /home/pi/Desktop/CREPE.log 2>&1'
Restart=on-failure
RestartSec=5s
KillMode=process
TimeoutSec=infinity

[Install]
WantedBy=graphical.target
```

Now we need to register the service and enable it with systemctl such that it will run upon next boot.
```
sudo chmod 644 /lib/systemd/system/CREPE.service
sudo systemctl daemon-reload
sudo systemctl enable CREPE.service
```

Upon reboot, check that the service is running:
```
sudo systemctl status CREPE.service
```

OPTIONAL: Instally numpy, scipy and matplotlib if you want to use main_with_visualization.py, which will display a human-interpretable, interpolated image of the IR data collected by the sensor.
libatlas-base-dev is needed to mitigate the error (ImportError: lib77blas.so.3 cannot open shared object file)
```
sudo apt-get install libatlas-base-dev 
pip3 install matplotlib scipy colour
```

End with an example of getting some data out of the system or using it for a little demo

## Use



## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

