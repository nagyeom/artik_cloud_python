#-*- coding: utf-8 -*-

import json
import time

import certifi
import paho.mqtt.client as mqtt
import blinkLED

ARTIK_MQTT_URL = 'api.artik.cloud'
ARTIK_MQTT_PORT = 8883
ACTION_CHANNEL = '/v1.1/actions/YOUR_COLOR_SENSOR_DEVICE_ID'#color Sensor device ID

def on_connect(client, userdata, flags, rc):
    print 'connected with result code ' , str(rc)
    client.subscribe(ACTION_CHANNEL)

def on_message(client, userdata, msg):
   # print msg.topic, " " , str(msg.payload)
    try : 
        data = json.loads(msg.payload)
    except json.decoder.JSONDecodeError:
        print "can't decode payload : %s"%str(msg.payload)
    else:
        color= data['actions'][0]['parameters']['color']
        print color
        if color :
            runBlinkLED(color)
        else :
            pass

def on_log(client, userdata, level, buf):
    print buf

def on_subscribe(client, userdata, mid, granted_qos):
    print '*' * 20
    blinkLED.printNowTime()

def runBlinkLED(color):
    bk = blinkLED.BlinkLED(color)
    bk.turn_on()
    time.sleep(1)
    bk.turn_off()
    bk.exitGPIO()
    print '*' * 20
    blinkLED.printNowTime()

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log

    client.username_pw_set('YOUR_COLOR_SENSOR_DEVICE_ID',password='YOUR_COLOR_SENSOR_DEVICE_ID_TOKEN')
    client.tls_set(certifi.where())
    client.connect(ARTIK_MQTT_URL,port=ARTIK_MQTT_PORT,keepalive=60)
    client.loop_forever()