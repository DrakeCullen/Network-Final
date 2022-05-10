# Kattis Candy Dispenser
### By Drake Cullen and Nathan Briner

<br>

## Command Line Interface
Add your .kattisrc file to this directory. Available at: https://open.kattis.com/download/kattisrc <br>
In order to run the submit client, follow the template below:

```bat
python submit.py -l [language] -i [Candy Machine IP] -p [Problem name] [file]

```

Note: the -i and -p flags are optional

<br> 

## Setup ESP32
Navigate to https://github.com/DrakeCullen/Network-Final/blob/master/ESP32_spinning_dc.ino. Download the source code and paste it into the arduino IDE. Change the ssid and password to your network. 
<br> <br>
Add the following URL under file > prefernces > additional board manager: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json. Now download the esp32 board and upload the code. Open the serial monitor to find the IP address of your ESP32.
<br> <br>
You will need to attach the esp32 to an L298n board with the pins specified in the arduino c code. Furthermore, attach the motor to a 9V battery and to the L298n board.

<br>

## 3D Model

The 3D model used in this project was created by JBVCreative, link below.
https://www.youtube.com/watch?v=jyCKpVE5A0U&ab_channel=JBVCreative

<br>

## Java App

The candy dispenser is also compatible with our Java app  kattis Assistant. When clearing completed problems on the problem wishlist page of the app candy will be dispensed based on the problem's difficulty. Link below. 
https://github.com/DrakeCullen/java-final-project

<br>

## Setup your own Heroku Flask Server
The app interacts with a flask server hosted on heroku. This step is not necessary, but will help you better understand how everything works together. Here is a link to our code: https://github.com/DrakeCullen/Kattis-Website

<br>

## Link to videos of the project
https://drive.google.com/drive/folders/1cVMn_1U1KTwUpIPHuIQlbaGjGENJCsd9?usp=sharing
