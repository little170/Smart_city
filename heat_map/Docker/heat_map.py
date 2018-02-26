import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import paho.mqtt.client as mqtt
import json

BROKER = "140.114.79.70"
TOPIC = "iot-1/d/0242ac110002/evt/#"

def pub_image():
    
    PUB_TOPIC = "heat-map"
    PUB_BROKER = "140.114.79.70"
    f= open("image.png")
    filecontent = f.read()
    message = bytearray(filecontent)
    mqttc = mqtt.Client()
    mqttc.connect(PUB_BROKER, 1883)
    mqttc.publish(PUB_TOPIC, message)
    f.close()

def generate_image():
    # initialize
    # Bounds and number of the randomly generated data points
    ndata = 8
    xmin, xmax = 120.92, 120.95
    ymin, ymax = 24.84, 24.87

    # Generate random data
    x = np.array([120.9459257, 120.9369287, 120.9362630, 120.9307647, 120.9324798,
 120.9264003, 120.9276767, 120.9341295])
    y= np.array([24.8576173,  24.84146622, 24.84015902, 24.84956197, 24.84989913, 24.8574199,
 24.84402954, 24.86830318])

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

    if event == "pollution_air_mq5":
       z[0] = value
    elif event == "pollution_air_mq7":
       z[7] = value
    elif event == "pollution_air_mq131":
       z[4] = value/7
    elif event == "pollution_air_mq135":
       z[5] = value
    if count%20 == 0:
       count = 0
       generate_image()
       pub_image()

#initialize value
ndata = 8
z = np.random.random(ndata)
count = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
