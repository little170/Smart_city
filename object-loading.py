import os
import paho.mqtt.client as mqtt

BROKER = "192.168.0.99"
TOPIC = "iot-1/d/hihi/evt/image_capture"  # Subscribe topic from Rpi O

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
   os.system("cp /home/nmsl-nuc/FogComputingPlatform-MQTT-Panel/public/images/object-loading.gif /home/nmsl-nuc/FogComputingPlatform-MQTT-Panel/public/images/result.jpg")

if __name__ == "__main__":
   client = mqtt.Client()
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect(BROKER, 1883, 60)
   client.loop_forever()
