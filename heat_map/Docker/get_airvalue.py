import paho.mqtt.client as mqtt
import numpy as np
import json

BROKER = "140.114.79.70"
TOPIC = "iot-1/d/0242ac110002/evt/#"

def json_parse(msg):
    data = json.loads(msg)
    event = data['d']['event']
    value = data['d']['value']
    return event, value

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):

    event, value = json_parse(msg.payload)
    
    if event == "pollution_air_mq5":
       print('MQ5 value',value)
    elif event == "pollution_air_mq7":
       print('MQ7 value',value)
    elif event == "pollution_air_mq131":
       print('MQ131 value',value)
    elif event == "pollution_air_mq135":
       print('MQ135 value',value)
    

if __name__ == "__main__":
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(BROKER, 1883, 60)
   client.loop_forever()
