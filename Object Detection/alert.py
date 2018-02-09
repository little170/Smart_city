import paho.mqtt.client as mqtt
import json
import commands
import os
import sys
import time

BROKER = "140.114.79.70"
#TOPIC = "iot-1/d/0242ac104a02/evt/#"  # Subscribe topic from Rpi O
TOPIC = "iot-1/d/0242ac100902/evt/#"  # Subscribe topic from Rpi O

def json_parse(msg):
    data = json.loads(msg)
    event = data['d']['event']
    value = data['d']['value']
    return event, value

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):

    event, value = json_parse(msg.payload)
    print event
    print value
    if event == "motion" and value==1:
       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep 'get-image-rpi3' |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS == 'Completed':
          os.system('kubectl delete pods get-image-rpi3')

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep 'yolo-rpi3' |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS == 'Completed':
          os.system('kubectl delete pods yolo-rpi3')

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep 'yolo-rpi3' |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS != 'Running':
           print('Deploy Rpi-yolo.....')
           os.system("kubectl create -f rpi-yolo.yaml")

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep 'get-image-rpi3' |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS != 'Running':
           print('Deploy Rpi-camera.....')
           os.system("kubectl create -f rpi-camera.yaml")
       
if __name__ == "__main__":
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(BROKER, 1883, 60)
   client.loop_forever()
