'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import motor_runner
import rgb
import json
from datetime import datetime
from pprint import pprint
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

#import ultrasonic
drop =0 
publish_response=0

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
         json.dump(data, fp)

def button_callback():
    rgb.cyanOff()
    rgb.whiteZero()
    print("Motor Run: ")
    print("Button was pushed!")
    motor_runner.pulse(5)
    message = {}
    message['action']     =  "feedActivity"
    message['data'] = "1" 
    message['type'] = "appDrop"
    message['quantity_dropped']  = "150"
    message['food_remaining_container'] = "300"
    message['timeStamp']=time.asctime( time.localtime(time.time()) )
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish("device", messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    rgb.whiteOff()
    rgb.cyanSlow();
    print("--------------\n\n")

def physical_button_press():
    rgb.cyanOff()
    rgb.whiteZero()
    print("Motor Run: ")
    print("Button was pushed!")
    message = {}
    message['action']     =  "feedActivity"
    message['data'] = "1" 
    message['type'] = "buttonDrop"
    message['quantity_dropped']  = "150"
    message['food_remaining_container'] = "300"
    message['timeStamp']=time.asctime( time.localtime(time.time()) )
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish("device", messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    motor_runner.pulse(5)
    rgb.whiteOff()
    rgb.cyanSlow();
    print("--------------\n\n")

def sch_drop():
    rgb.cyanOff()
    rgb.whiteZero()
    print("Motor Run: ")
    print("schedule drop!")
    motor_runner.pulse(5)
    message = {}
    message['action']     =  "feedActivity"
    message['data'] = "1" 
    message['type'] = "scheduleDrop"
    message['scheduleTime'] = "[7:20]"
    message['quantity_dropped']  = "150"
    message['food_remaining_container'] = "300"
    message['autoFeed'] = "1"
    message['timeStamp']=time.asctime( time.localtime(time.time()) )
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish("device", messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    rgb.whiteOff()
    rgb.cyanSlow();
    print("--------------\n\n")

def pet_activity():
    rgb.cyanOff()
    rgb.whiteZero()
    message = {}
    message['time']     =time.asctime( time.localtime(time.time()) )
    message['pet_id']   = "oliver"
    message['photo_path'] = "www.hungrytail.com" 
    message['quantity_eaten'] = "100" 
    message['food_remaing_bowl'] = "100"
    message['food_remaing'] = "500"
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish("device", messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    rgb.whiteOff()
    rgb.cyanSlow();
    print("--------------\n\n")


def update_for_next_feed(val):
    tmp=sch[val]
    fhour=tmp[0]
    fmins=tmp[1]
    fauto=tmp[2]
    fstat=tmp[3]
    fwght=tmp[4]

rgb.blueOn()
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(19,GPIO.RISING,callback=physical_button_press) # Setup event on pin 10 rising edge

AllowedActions = ['both', 'publish', 'subscribe']
feed_time1= []
feed_wght=[] 
auto_feed=[]

# Custom MQTT message callback
def customCallback(client, userdata, message):
    rgb.cyanOff()
    rgb.whiteZero()
    print("Publish Recieved from Server")
    rgb.whiteOff()
    rgb.cyanSlow();
    print(message.topic);
    alldata=json.loads(message.payload.decode("utf-8"));
    action=alldata['action']
    if(action=="write"):
        filename=alldata['fileName']
        data=alldata['data']
        writeToJSONFile('./',filename,data) 
        message = {}
        message['success'] = 1 
        message['timeStamp'] = time.asctime( time.localtime(time.time()) )
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish("device", messageJson, 0)
        print('Published topic %s: %s\n' % (action, messageJson))
    elif(action=='read'):
        filename=alldata['fileName']
        with open(filename) as json_file:  
             data = json.load(json_file)
        message = {}
        message['fileName'] = filename 
        message['data'] = data 
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish("device", messageJson, 0)
        print('Published topic %s: %s\n' % (action, messageJson))
    elif(action=='calibrate'):
        wieght=alldata['weight']
        timestamp=alldata['timeStamp']
        message = {}
        message['success'] = 1 
        #message['timeStamp'] = time.asctime( time.localtime(time.time()) )
        message['timeStamp'] = timestamp 
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish("device", messageJson, 0)
        print('Published topic %s: %s\n' % (action, messageJson))
    elif(action=='appDrop'):
        quantity=alldata['quantity']
        timestamp=alldata['timeStamp']
        #Store Data into SQL, Read in While Loop"
        button_callback()
        message = {}
        message['success'] = 1 
        message['timeStamp'] = timestamp      
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish("device", messageJson, 0)
        print('Published topic %s: %s\n' % (action, messageJson))
    elif(action=='deviceStatus'):
        timestamp=alldata['timeStamp']
        message = {}
        message['colorCode'] = "[125,255,75]" 
        message['food_remaining_bowl'] = "50" 
        message['food_remaining_container']  = "230"
        message['timeStamp'] = timestamp      
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish("device", messageJson, 0)
        print('Published topic %s: %s\n' % (topic, messageJson))
    print("--------------\n\n")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="server", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="subscribe",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic
rgb.blueOff()
rgb.cyanFast()
if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
rgb.cyanSlow()


with open('schedule.json') as json_data:
    data = json.load(json_data)
    data= data['data']
    sch= data['feedSchedules']
    length=len(sch) - 1
    tmp = sch[0]
    fhour=tmp[0]
    fmins=tmp[1]
    fauto=tmp[2]
    fstat=tmp[3]
    fwght=tmp[4]

if args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    hours=datetime.now().hour
    mins=datetime.now().minute
    if hours==fhour and mins == fmins:
        loopCount=loopCount + 1
        update_for_next_feed(loopCount)
        print ("DROP::Food Drop Actual time %s:%s" % (fmins,fmins))
        print ("DROP::current time is %s:%s" % (hours, mins))
        sch_drop()
    time.sleep(1)

