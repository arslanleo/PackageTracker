import paho.mqtt.client as pahomqtt
import msgpack, math, logging
from django.db import connection

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

logger.info("Server Started...")

########### MQTT CODE IMPLEMENTATION ###############
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
        distance = math.pow(ratio,10)
    else:
        distance =  (0.89976)*math.pow(ratio,7.7095) + 0.111    
    return round(distance,2)
    #return math.pow(10,((measureTx-rssi)/(10*2)))

def on_connect(client, userdata, flags, rc):
    #print("connected with code: " + str(rc))
    logger.debug("Connected to MQTT ip with code: " + str(rc))
    #client.subscribe([("mqttTopic83",1),("mqttTopic85",1)])
    (result, mid) = client.subscribe(MQTT_TOPICS)
    logger.debug("Subscription call's Result: " + str(result) + ", MID: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    logger.debug("Successfully subscribed with code: " + str(mid) + " and QOS: " + str(granted_qos))

def on_message(client, userdata, msg):
    messageDict = msgpack.unpackb(msg.payload, use_list=True, raw=False)
    messageDevMac = messageDict["mac"]
    #print(messageDevMac)
    messageDevices = messageDict["devices"]
    messageDevicesCount = len(messageDevices)
    for dev in messageDevices:
        dat = dev.hex()
        mac = dat[2:14]
        rssi = int(dat[14:16],16) - 256
        dist = getDistance(rssi)
        tagsData[(mac.upper(),messageDevMac.upper())]=[rssi,dist]      #key: tag's mac, locating node's mac
        logger.debug("MQTT DATA: " + messageDevMac.upper() + " " + mac.upper() + " " + str(rssi) + " " + str(dist))
    #print(tagsData.items())

for r in my_custom_sql():
    MQTT_TOPICS.append((r[0],0))

client = pahomqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect_async(MQTT_URL, MQTT_PORT, 60)

