import paho.mqtt.client as mqtt
import msgpack
import math

tagsData = {}

def getTagsInfo():
    return tagsData

def getDistance(rssi):
    measureTx = -59
    if (rssi == 0):
        return -1.0     
    ratio = rssi*1.0/measureTx
    if (ratio < 1.0):
        return math.pow(ratio,10)
    else:
        distance =  (0.89976)*math.pow(ratio,7.7095) + 0.111    
    return round(distance,2)
    #return math.pow(10,((measureTx-rssi)/(10*2)))



def on_connect(client, userdata, flags, rc):
    print("connected with code: " + str(rc))
    client.subscribe("arslantopic")

def on_message(client, userdata, msg):
    messageDict = msgpack.unpackb(msg.payload, use_list=True, raw=False)
    messageDevices = messageDict["devices"]
    messageDevicesCount = len(messageDevices)
    for dev in messageDevices:
        dat = dev.hex()
        mac = dat[2:14]
        rssi = int(dat[14:16],16) - 256
        tagsData[mac.upper()]=[rssi,getDistance(rssi)]
    #print(tagsData.items())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("mqtt.bconimg.com", 1883, 60)

