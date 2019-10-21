from . import mqtt
#from BeaconManager.models import Node

mqtt.MQTT_CLIENT.loop_start()

#client1 = mqtt.mqttClientClass("mqtt.bconimg.com",1883,"arslantopic")
#client1.prepare()
#client1.start()