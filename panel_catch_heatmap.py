import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.
print 'Demo: heat map'
def on_connect(client, userdata, flags, rc):
  print "Connected with result code "+str(rc)
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
  client.subscribe('heat-map')
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  print 'Loading Image...'
  PATH = '/home/nmsl-nuc/FogComputingPlatform-MQTT-Panel/public/images/'
  f = open(PATH+'heatmap.jpg','w')
  f.write(msg.payload)
  f.close()
  print 'panel receive image'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.0.99', 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
