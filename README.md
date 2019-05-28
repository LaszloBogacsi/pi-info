# Pi-Info
Home automation project

*using raspberry pi 3B+ and*

- D1 mini esp8266 devboard 
- DHT22 temp and humidity sensor on breakout board
- Mosquitto MQTT
- Arduiono language
- Python with flask

___
### Raspberry Pi setup:

install mosquitto: `sudo apt-get install mosquitto -y`  
install mosquitto client `sudo apt-get install mosquitto-clients -y`  
edit the conf file: `sudo nano /etc/mosquitto/mosquitto.conf`  
add these lines to allow only authenticated clients to connect
```
allow_anonymous false
password_file /etc/mosquitto/pwfile
listener 1883
```
create an encrypted password for a username at the specified password file location
`sudo mosquitto_passwd -c /etc/mosquitto/pwfile <username>`  

reboot the pi: `sudo reboot`  
Mosquitto is ready, to verify:  
To subscribe to a topic:  
`mosquittto_sub -d -u <usename> -P <password> -t test`  
To publish a message in a topic:  
`mosquitto_pub -d -u <usename> -P <password> -t test -m "hello, world"`
___

### Project Setup:
install pipenv: `pip install pipenv`  
clone the project `cd pi-info`   
install the dependencies with dev dependencies: `pipenv install --dev` form the **Pipfile**
this will create a vitrual env with a version of python installed (3.7+)  
start the flask server: `pipenv run python pi-info.py`  
the development server is listening on: `http://localhost:8080/`

### Local Development:
to install packages use:  
`pipenv install <package name>` this will install the required package and save the package name to the *Pipfile*
