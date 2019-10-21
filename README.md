# <img alt="logo" src="./pi_info/static/home_hub_logo.svg" height="48" width="48" > Home-Hub 
 
 Home automation project  
 
 *using raspberry pi 3B+ and*  
 
 - D1 mini esp8266 wifi devboard 
 - DHT22 temp and humidity sensor on breakout board 
 - Sonoff Basic R2
 - Mosquitto MQTT - Arduino language 
 - Python with Flask
 - D3.js for visualisations
 - Gunicorn wsgi
 - Supervisor
 - Nginx
 - AWS DynamoDB for remote state storage (Alexa integration)  
 
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
 Bridging with remote mqtt service
 ```properties
 # mosquitto.conf
 # Connection to RemoteMQTT

connection <connection name>
address <host:port>
topic <topic/name> both 0 "" remote/ # remote/ is a forwarded rename eg "topic/name" will be forwarded as "remote/topic/name"
remote_username <username>
remote_password <password>
try_private true
notifications false
cleansession true
start_type automatic
 ```
 reboot the pi: `sudo reboot`  
 Mosquitto is ready,  
 to verify: 
 To subscribe to a topic: `mosquittto_sub -d -u <usename> -P <password> -t test` 
 To publish a message in a topic: `mosquitto_pub -d -u <usename> -P <password> -t test -m "hello, world"`  
 install supervisor `sudo apt install supervisor`
 supervisor is a preferable solution to run the gunicorn server in the background and also start it automatically on reboot  
 install nginx `sudo apt install nginx` 
 postgres install:  
`sudo apt-get install postgresql`  
`sudo apt-get install python-psycopg2`  
`sudo apt-get install libpq-dev`  
then run `./database-setup.sh` script to set up db 

Requires local AWS cli credentials
 
To see Supervisor and the app logs:
```
http://<r-pi-host>:9001
```
after adding the following to the supervisor config:
```
[inet_http_server]
port=0.0.0.0:9001
```

Nginx config in `sites-enabled` in `home-hub.conf`
```
server {                                                                  
    listen 80;                                                           
     server_name <r-pi-host>;                                          
                                                                         
     location /static/ {                                                 
            alias /path/to/static/; 
                                                                         
     }                                                                   
     location / {                                                        
             include proxy_params;                                       
             proxy_pass http://localhost:5000;                           
     }                                                                   
}                                                                        
```
 
 ___ 
 ### Arduino IDE setup:  
 
 Additional Board manager urls: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`   
 Then install: `esp8266 by ESP8266 Community`   
 Board type: `ESP8266 Generic` (for fake WeMos D1 mini)   
 Flash Size `4M(3M SPIFFS)`   
 Baud rate: `115200`    
 Libraries:   
 Nick O'Leary PubSubClient   
 Patric Lapointe EspMQTTClient   
 beegee_tokyo DHT sensor library for ESPx   
 
 ___  
 ### Project Setup: 
 
 Requirement: Python 3.7  
 install pipenv: `pip install pipenv`    
 clone the project `cd pi-info`    
 install the dependencies with dev dependencies: `pipenv install --dev`   
 form the **Pipfile** this will create a virtual env with a version of python installed (3.7+)   
 start the flask server: `pipenv run python pi-info.py`  
 
 ### Local Development:  
  
 to install packages use: `pipenv install <package name>` this will install the required package and save the package name to the *Pipfile*   
 the development server is listening on: `http://localhost:9080/`
 
 ### Deployment:  
 run the `deploy.sh` script after initial setup 
 use `gunicorn` for production web server, a `wsgi` server - *not supported on windows*
