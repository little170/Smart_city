import paho.mqtt.client as mqtt
import json
import commands
import os
import sys
import time

BROKER = "192.168.0.99"
TOPIC = "iot-1/d/+/evt/motion/json"  # Subscribe topic from Rpi O

def json_parse(msg):
    data = json.loads(msg)
    event = data['d']['event']
    value = data['d']['value']
    return event, value

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    device_id =  msg.topic[8:12]
    print device_id
    if device_id == "rpi1": 
       camera_yaml = 'rpi1-camera.yaml'       
       yolo_yaml = 'rpi1-yolo.yaml'
       camera_pod = 'get-image-rpi1'
       yolo_pod = 'yolo-rpi1'
    elif device_id == "rpi2":
       camera_yaml = 'rpi2-camera.yaml'       
       yolo_yaml = 'rpi2-yolo.yaml'
       camera_pod = 'get-image-rpi2'
       yolo_pod = 'yolo-rpi2'
    elif device_id == "rpi3" :
       camera_yaml = 'rpi3-camera.yaml'       
       yolo_yaml = 'rpi3-yolo.yaml'
       camera_pod = 'get-image-rpi3'
       yolo_pod = 'yolo-rpi3'

    event, value = json_parse(msg.payload)
    if event == "motion" and value==1:
       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep " + camera_pod + " |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS == 'Completed':
          os.system('kubectl delete pods ' + camera_pod)

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep "+ yolo_pod+" |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS == 'Completed':
          os.system('kubectl delete pods ' + yolo_pod)

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep " + yolo_pod + " |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS != 'Running' and POD_STATUS != 'ContainerCreating' and POD_STATUS != 'Terminating':
           print('Deploy Rpi-yolo.....')
           os.system("kubectl create -f "+yolo_yaml)

       r, POD_STATUS= commands.getstatusoutput(
                               "kubectl get po -a | grep " + camera_pod + " |tr -s ' ' |cut -d ' ' -f 3")
       if POD_STATUS != 'Running' and POD_STATUS != 'ContainerCreating' and POD_STATUS != 'Terminating':
           print('Deploy Rpi-camera.....')
           os.system("kubectl create -f "+ camera_yaml)
       time.sleep(1)
if __name__ == "__main__":
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(BROKER, 1883, 60)
   client.loop_forever()
