#-*- coding: utf-8 -*-

import json
import time
import sys

import certifi
import paho.mqtt.client as mqtt


ARTIK_MQTT_URL = 'api.artik.cloud'
ARTIK_MQTT_PORT = 8883
PUBLISH_CHANNEL = '/v1.1/messages/YOUR_GATEWAY_DEVICE_ID' #deviceID
ACTION_CHANNEL = '/v1.1/actions/YOUR_GATEWAY_DEVICE_ID'

class LinkerMQTT():
    def __init__(self):
        """
        선언과 동시에 mqtt connect
        """
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        self.client.username_pw_set('YOUR_GATEWAY_DEVICE_ID',password='YOUR_GATEWAY_DEVICE_ID_TOKEN')
        self.client.tls_set(certifi.where())
        self.client.connect_async(ARTIK_MQTT_URL,port=ARTIK_MQTT_PORT,keepalive=60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print "connected with result code " , str(rc)
        if rc ==0:
            self.client.subscribe(ACTION_CHANNEL)

    def on_publish(self, client, userdata, mid):
        print 'published'

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print 'subscribed'

    def on_message(self, client, userdata, msg):
        print msg.topic," ",str(msg.payload)

    def on_log(self, client, userdata, level, buf):
        print buf

    # def connectMQTT(self):
    #     self.client = mqtt.Client()
    #     self.client.on_connect = self.on_connect
    #     self.client.on_message = self.on_message
    #     self.client.on_publish = self.on_publish
    #     self.client.on_log = self.on_log
    #     self.client.username_pw_set('YOUR_GATEWAY_DEVICE_ID',password='YOUR_GATEWAY_DEVICE_ID_TOKEN')
    #     self.client.tls_set(certifi.where())
    #     self.client.connect_async(ARTIK_MQTT_URL,port=ARTIK_MQTT_PORT,keepalive=60)
    #     self.client.loop_start()
    
    def pubColor(self, colorDict):
        self.client.publish(PUBLISH_CHANNEL, json.dumps(colorDict))


def colorSwitcher(client):
    """
    사용자로부터 color값을 입력받고 client - publish 한다.
    """
    while True:
        print "input color (red/green/blue) : "
        color = raw_input()
        if color == 'red' or colr == 'green' or color == 'blue':
            print color , type(color)
            colorDict = {'color':color}
            client.pubColor(colorDict)
        else :
            print "Please choose correct color of red/green/blue."
            continue

if __name__ == "__main__":
    try :
        mq = LinkerMQTT()
    except Exception as e:
        print e
    except KeyboardInterrupt :
        print "Exit the program."
        sys.exit(0)
    else:
        colorSwitcher(mq)


