# Rock, Paper, Scissors demonstration
A demonstration of the CREPE communication framwork utilizing hardware, sensor data and network communications. 



### Intention
This demonstration is a simple example use case of the CREPE framework, demonstrating how CREPE allows for seemless and effortless experimentation with biological neurons. 

The demo setup will capture the IR profile of a rock/paper/scissor and trasnmitt this in json format through wifi to CREPE. CREPE will communcate the data further to the biological neurons, interpretate the results and transmitt these back to the demo setup, which will display the result on a display. 


### Setup of demo, physical components and configuraton

**Components:**
- Arudino Uno       
  - [Datasheet](https://www.terraelectronica.ru/pdf/show?pdf_file=%2Fz%2FDatasheet%2FU%2FUNO_R3(CH340G).pdf&fbclid=IwAR2FrlMjTS1hMZOYdpzgNwjVe-th5LTBIL-3l3MgKYxddCArinXqffufGAc)
- ESP8266 SMT module (Wifi module)
  - [Datasheet](http://wiki.ai-thinker.com/_media/esp8266/docs/a001ps01a2_esp-01_product_specification_v1.2.pdf?fbclid=IwAR2E6Dpguf-HQLodjZ8DdVEVA4pAAcRWWhqb_sUmmcb46i1hmuMgdBjYaW4)
- Adafruit AMG8833   (IR-sensor)
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-amg8833-8x8-thermal-camera-sensor.pdf?timestamp=1552457921)
- Adafruit 1.44" Color TFT LCD Display 
  - [Datasheet](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-1-44-color-tft-with-micro-sd-socket.pdf?timestamp=1552457427)

**Overveiw of complete setup:**
The harware is mounted inside a 3D printed container, powered by a power bank also mounted inside. A small LCD dislay is mounted on he exterior of the container. A IR-sensor is mounted n the interior of the box, capturing data througha slot in the box. A adjustable plate is attached to the bottom of the container. This plate is equipped with a button, registering the hand of the subject. This button is connected to the Arduino.

**Arduino: setup**
The Arduino Uno is through a PCB shield equipped with the IR-sensor, wifi module and the LCD Display. It captures the IR profile of a rock/paper/scissor and transmits this to CREPE in json format. Results recieved from CREPE are displayed on the display. Capturing of data is triggered by the button mounted on the adjustable plate. 

### Requisites 
- The Arduino Uno used is a un-officila arduino. It requires a special driver to connect to Windows. [Driver link]()


### Installation

"Plug an play repository. To recreate this demonstration, Download the repository and follow instructions given in comments on each source file. Upload to arduino. All code in this repository is intended to run on the Arduino.
A step by step series of examples that tell you how to get a development env running"

Say what the step will be

```
Give the example
```

And repeat

```
until finished
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

