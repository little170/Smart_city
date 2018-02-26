import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time 

BROKER = "140.114.79.70"
TOPIC = "iot-1/d/+/evt/#"

def pub_image(pollution_range):
    
    PUB_TOPIC = "heat-map"
    PUB_BROKER = "140.114.79.70"
    f= open("image.png")
    filecontent = f.read()
    message = bytearray(filecontent)
    mqttc = mqtt.Client()
    mqttc.connect(PUB_BROKER, 1883)
    mqttc.publish(PUB_TOPIC, message)
    f.close()
    message = '{"d":{"timestamp":%s,"value":"%s","event":"heat_map_result"}}' % (time.time(),pollution_range)
    PUB_TOPIC = "iot-1/d/0242ac100302/evt/heatmap/json"
    mqttc.publish(PUB_TOPIC, message)

def generate_image():
    # initialize
    # Bounds and number of the randomly generated data points
    ndata = 8
    xmin, xmax = 120.92, 120.95
    ymin, ymax = 24.84, 24.87

    # Generate random data
    x = np.array([120.92, 120.92, 120.95, 120.95])
    y= np.array([24.84,  24.87, 24.84, 24.87])

    # Size of regular grid
    ny, nx = 128,128

    # Generate a regular grid to interpolate the data.
    xi = np.linspace(xmin, xmax, nx)
    yi = np.linspace(ymin, ymax, ny)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate using delaunay triangularization 
    zi = mlab.griddata(x,y,z,xi,yi,interp='linear')

    # Plot the results
    plt.figure()
    plt.pcolormesh(xi,yi,zi)
    plt.scatter(x,y,c=z)
    plt.colorbar()
    plt.axis([xmin, xmax, ymin, ymax])
    print('save image...')
    plt.savefig('image.png')
    plt. close(0)

def json_parse(msg):
    data = json.loads(msg)
    event = data['d']['event']
    value = data['d']['value']
    return event, value

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    event, value = json_parse(msg.payload)
    global z
    global count
    count = count + 1
    pollution_range = "None"
    if event == "pollution_air_mq5":
       z[3] = value
       if value > 20:
          pollution_range="Main entraince"
    elif event == "pollution_air_mg811_rpi3":
       z[0] = value
       if value > 20:
          pollution_range="Delta"
    elif event == "pollution_air_mg811_rpi2":
       z[1] = value
       if value > 20:
          pollution_range="Dormitories"
    elif event == "pollution_air_mg811_rpi1":
       z[2] = value
       if value > 20:
          pollution_range="Parking Ramp"
    if count%20 == 0:
       count = 0
       generate_image()
       pub_image(pollution_range)

#initialize value
ndata = 4
z = np.random.random(ndata)
count = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
