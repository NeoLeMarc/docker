#!/usr/bin/eny python
from flask import Flask, render_template, Response, jsonify, request, redirect
import time, requests

USERNAME=""
PASSWORD=""
ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ""

import paho.mqtt.client as c
import threading

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True

history = []

def get_request(url):
    r = requests.get(url = url)
    return r

def delete_request(url):
    r = requests.delete(url = url)
    return r

def post_request(url, params):
    r = requests.post(url = url, data = params)
    return r

class MQTTHandler(object):

    def __init__(self):
        pass

    def registerRemoteClient(self, remoteClient):
        self.remoteClient = remoteClient

    def sendCommand(self, target, command):
        history.append({'handler' : type(self).__name__,
                        'target'  : target,
                        'command' : command,
                        'timestamp' : time.time(),
                        'localtime' : time.asctime()})
        self.on_command(target, command)

class LocalMQTT(MQTTHandler):
    def on_command(self, target, command):
        print("Local command handler: %s %s" % (target, command))

        if target == "poseserver":
            if command in ['learning', 'lock']:
                self.client.publish('ifttt-bridge/poseserver', command, True)
                print("Published command")
            else:
                print("Rejecting unknown command " + command)
        if target == "mqtt-controller":
            if command in ['start-game', 'start-hell', 'reset', 'lock']:
                self.client.publish('ifttt-bridge/mqtt-controller', command, True)
                print("Published command")

                ## Also trigger http request
                #if command == 'start-game':
                #    get_request("http://iotserver01.iot.ka.xcore.net:5001/start_game")
                #elif command == 'start-hell':
                #    get_request("http://iotserver01.iot.ka.xcore.net:5001/start_hell")
                #elif command == 'reset':
                #    delete_request("http://iotserver01.iot.ka.xcore.net:5001/scheduled_game")
                #elif command == 'lock':
                #    post_request("http://iotserver01.iot.ka.xcore.net:5001/lock", {'lockStatus' : 'locked'})

            else:
                print("Rejecting unknown command " + command)

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
        client.subscribe("ifttt-bridge/out")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


    def updateWithMessage(self, client, container, field, message):
        if field in container:
            container[field] = message.payload.decode("utf-8")
        else:
            print("Unknown field: %s" % field)


    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg

    def __init__(self):
        self.client = c.Client("ifttt-bridge-local")
        self.client.on_connect=self.on_connect
        self.client.on_message=self.on_message
        self.client.connect("iotserver01.iot.ka.xcore.net")
        self.client.loop_start()


class AdafruitMQTT(MQTTHandler):
    def on_command(self, target, command):
        print("Adafruit command handler: %s %s" % (target, command))

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        print("(Adafruit) Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
        client.subscribe("NeoLeMarc/feeds/ifttt")  # Subscribe to the topic “digitest/test1”, receive any messages published on it
        print("(Adafruit) subscribed")

    def updateWithMessage(self, client, container, field, message):
        if field in container:
            container[field] = message.payload.decode("utf-8")
        else:
            print("(Adafruit) Unknown field: %s" % field)


    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("(Adafruit) Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        
        if msg.payload.decode("utf-8") in ['learning', 'lock']:
           self.remoteClient.sendCommand('poseserver', msg.payload.decode("utf-8")) 

        if msg.payload.decode("utf-8") in ['start-game', 'start-hell', 'reset', 'lock']:
           self.remoteClient.sendCommand('mqtt-controller', msg.payload.decode("utf-8")) 

    def __init__(self):
        self.client = c.Client("ifttt-bridge-remote")
        self.client.on_connect=self.on_connect
        self.client.on_message=self.on_message
        self.client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        self.client.connect("io.adafruit.com")
        self.client.loop_start()

localMQTT = LocalMQTT()
adafruitMQTT = AdafruitMQTT()

localMQTT.registerRemoteClient(adafruitMQTT)
adafruitMQTT.registerRemoteClient(localMQTT)

@app.route("/")
def hello_world():
    return render_template("index.html", history=history, reversed=reversed) 

