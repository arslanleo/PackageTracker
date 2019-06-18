import paho.mqtt.client as pahomqtt
import msgpack
import math
from django.db import connection

tagsData = {}
MQTT_PORT = 1883
MQTT_URL = "mqtt.bconimg.com"
MQTT_TOPICS = []

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT topic FROM BeaconManager_node")
        row = cursor.fetchall()
    return row

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
    #client.subscribe([("mqttTopic83",1),("mqttTopic85",1)])
    client.subscribe(MQTT_TOPICS)

def on_message(client, userdata, msg):
    messageDict = msgpack.unpackb(msg.payload, use_list=True, raw=False)
    messageDevMac = messageDict["mac"]
    print(messageDevMac)
    messageDevices = messageDict["devices"]
    messageDevicesCount = len(messageDevices)
    for dev in messageDevices:
        dat = dev.hex()
        mac = dat[2:14]
        rssi = int(dat[14:16],16) - 256
        tagsData[(mac.upper(),messageDevMac.upper())]=[rssi,getDistance(rssi)]      #key: tag's mac, locating node's mac
    #print(tagsData.items())

for r in my_custom_sql():
    MQTT_TOPICS.append((r[0],1))

client = pahomqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect_async(MQTT_URL, MQTT_PORT, 60)

#Class definition
#class mqttClientClass:
#    def __init__(self, addr, prt, tpc, *args, **kwargs):
#        self.tagsData = {}
#        self.measureTx = -59
#        self.myClient = pahomqtt.Client()
#        self.address = addr
#        self.port = prt
#        self.topic = tpc

#        return super().__init__(*args, **kwargs)

#    def getTagsInfo(self):
#        return self.tagsData

#    def my_on_message(client, userdata, msg):
#        messageDict = msgpack.unpackb(msg.payload, use_list=True, raw=False)
#        messageDevices = messageDict["devices"]
#        messageDevicesCount = len(messageDevices)
#        for dev in messageDevices:
#            dat = dev.hex()
#            mac = dat[2:14]
#            rssi = int(dat[14:16],16) - 256
#            self.tagsData[mac.upper()]=[rssi,my_getDistance(rssi)]

#    def my_on_connect(client, userdata, flags, rc):
#        print("connected with code: " + str(rc))
#        client.subscribe(self.topic)
    
#    def my_getDistance(self, rssi):
#        if (rssi == 0):
#            return -1.0     
#        ratio = rssi*1.0/self.measureTx
#        if (ratio < 1.0):
#            return math.pow(ratio,10)
#        else:
#            distance =  (0.89976)*math.pow(ratio,7.7095) + 0.111    
#        return round(distance,2)
#        #return math.pow(10,((measureTx-rssi)/(10*2)))

#    def prepare(self):
#        self.myClient.on_connect = self.my_on_connect
#        self.myClient.on_message = self.my_on_message
#        self.myClient.connect_async(self.address, self.port, 60)

#    def start(self):
#        self.myClient.loop_start()

