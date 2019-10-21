import paho.mqtt.client as pahomqtt
import math, logging, json
from django.db import connection
from scipy.optimize import minimize
from .kalman import SingleStateKalmanFilter

########### GLOBAL VARIABLES DECLARATION ###############
tagsData = {}
tempTagsData = {}
FILTERS = {}
LOCATIONS = {}
GATEWAYS = {}
KNOWNTAGS = []
MQTT_PORT = 1883
MQTT_URL = "mqtt.eclipse.org"
MQTT_TOPICS = []
TOPICS_QOS = 1
logger = logging.getLogger(__name__)        # This retrieves a Python logging instance (or creates it)
MQTT_CLIENT = pahomqtt.Client("P1") #create new instance
#parameters for filtering algorithm
WINDOW_LENGTH = 10


########### MISC FUCTIONS ###############

def initializationRoutine():
    logger.info("Server Started...")
    [r1,r2] = my_custom_sql()
    for r in r1:
        MQTT_TOPICS.append((r[0],TOPICS_QOS))   #fetch all topics from database and populate the topics variable
        [_x,_y] = r[2].split(",")
        _xx = float(_x)
        _yy = float(_y)
        GATEWAYS[r[1]] = (_xx,_yy)   #fetch all gateways MACs and locations from database and populate the GATEWAYS variable
    for r in r2:
        KNOWNTAGS.append(r[0])    #fetch all known tags from database and populate the KNOWNTAGS variable

    MQTT_CLIENT.on_connect = on_connect
    MQTT_CLIENT.on_subscribe = on_subscribe
    MQTT_CLIENT.on_message = on_message #attach function to callback
    logger.debug("connecting to broker")

    MQTT_CLIENT.connect_async(MQTT_URL, MQTT_PORT, 60)   #connect to broker
        
    return

def my_custom_sql():
    '''
    Gets the mqqt data from the database
    '''
    with connection.cursor() as cursor:
        cursor.execute("SELECT topic, node_id, location FROM BeaconManager_node")
        rows = cursor.fetchall()
        cursor.execute("SELECT tagID FROM BeaconManager_tag")
        rows2 = cursor.fetchall()
    return [rows,rows2]

def getTagsInfo():
    return tagsData

def checkConnectedGateways(beaconMac):
    '''
    Check if there are 3 gateways providing distance of the given beacon
    If yes, then return MACs of those 3 gateways
    '''
    count = 0
    gateways = []
    for (tagMac,GateMac) in tagsData.keys():
        if tagMac == beaconMac:
            gateways.append(GateMac)
            count +=1
            if count == 3:
                return gateways
    return 0

def circle_distance(x1,y1,x2,y2):
    '''
    Calculate Distance between two points
    '''
    dx = math.pow(x2-x1,2.0)
    dy = math.pow(y2-y1,2.0)
    return math.sqrt(dx+dy)

def mse(x, locations, distances):
    '''
    Mean Square Error
    locations: [ (lat1, long1), ... ]
    distances: [ distance1, ... ]
    '''
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = circle_distance(x[0], x[1], location[0], location[1])
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(locations)

def getLocation(locations,distances,initial_location):
    ''' initial_location: (lat, long)
    locations: [ (lat1, long1), ... ]
    distances: [ distance1,     ... ]
    '''
    
    result = minimize(
	    mse,                         # The error function
	    initial_location,            # The initial guess
	    args=(locations, distances), # Additional parameters for mse
	    method='L-BFGS-B',           # The optimisation algorithm
	    options={
		    'ftol':1e-5,         # Tolerance
		    'maxiter': 1e+7      # Maximum iterations
	    })
    
    location = result.x
    return location

def getDistance(rssi,rssiCalibrated = -59):
    '''
    Converts RSSI to Distance Value
    '''
    if rssi == rssiCalibrated:
        return 1.00
    elif rssi == 0:
        return -1.00
    elif rssi > rssiCalibrated:
        dist = math.pow(((rssi*1.00)/rssiCalibrated),10)
        return round(dist,2)
    else:
        dist = (0.89976*(math.pow(((rssi*1.00)/rssiCalibrated),7.7095))+0.111)
        return round(dist,2) 

########### MQTT CODE IMPLEMENTATION ###############

def on_connect(client, userdata, flags, rc):
    print("connected to broker with code: " + str(rc))
    logger.debug("Connected to MQTT broker ip with code: " + str(rc))
    #client.subscribe([("mqttTopic83",1),("mqttTopic85",1)])
    (result, mid) = client.subscribe(MQTT_TOPICS)
    logger.debug("Subscription call's Result: " + str(result) + ", MID: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    logger.debug("Successfully subscribed with code: " + str(mid) + " and QOS: " + str(granted_qos))

def on_message(client, userdata, msg):
    #parse received JSON data to a python dictionary
    msg_data = json.loads(msg.payload.decode("utf-8"))
    #seperate the gateway info and the beacons data
    gateway_info = msg_data[0]
    beacons_data = msg_data[1:]
    for beacon in beacons_data:
        _intRssi = int(beacon['rssi']) - 12     #remove the gain
        k = (beacon['mac'],gateway_info['mac'])     #create a pair of both MACs
        if k in tempTagsData.keys():        #if value already exists in dictionary
            tempTagsData[k].append(_intRssi)    #append current value at the end
            if len(tempTagsData[k]) >= WINDOW_LENGTH:
                chunk = tempTagsData[k]
                _t = max(chunk,key=chunk.count)     #select the value with maximum occurances in that chunk
                tempTagsData[k] = [_t]              #initialize the list again
                if k in FILTERS.keys():             #check if a filter already exists for current key
                    FILTERS[k].step(0, _t)          #if exists, add the current value to it FILTERS[k].current_state()
                    tagsData[k]=[FILTERS[k].current_state(),getDistance(FILTERS[k].current_state())]        #key: tag's mac, locating node's mac
                else:
                    FILTERS[k] = SingleStateKalmanFilter(x=_t)  #creates a new filter if it dosen't already exists
                #print(_t)
        else:
            tempTagsData[k] = [_intRssi]    #if doesn't exist then create a new one
        ##calculates locations of known tags
        #if(beacon['mac'] in KNOWNTAGS):
        #    _connectedGateways = checkConnectedGateways(beacon['mac'])
        #    if not(_connectedGateways == 0):
        #        _locations = [GATEWAYS[_connectedGateways[0]],GATEWAYS[_connectedGateways[1]],GATEWAYS[_connectedGateways[2]]]
        #        (_r0,_d0) = tagsData.get((beacon['mac'],_connectedGateways[0]))
        #        (_r1,_d1) = tagsData.get((beacon['mac'],_connectedGateways[1]))
        #        (_r2,_d2) = tagsData.get((beacon['mac'],_connectedGateways[2]))
        #        _distances = [_d0*10,_d1*10,_d2*10]
        #        (_loc0,_loc1) = getLocation(_locations,_distances,(0.0,0.0))
        #        LOCATIONS[beacon['mac']] = (int(_loc0),int(_loc1))
                #print(LOCATIONS.items())

def getTagLocation(NodesList,LayoutScale):
    foundLocations = []
    for _tagMac in KNOWNTAGS:       #check all of the tags available in the known tags list
        _connectedGateways = checkConnectedGateways(_tagMac)    #check if atleast 3 gateways are connected to that tag
        if not(_connectedGateways == 0):
            #check if NodesList contains all elements in _connectedGateways
            result =  all(elem in NodesList  for elem in _connectedGateways)
            if result:
                _locations = [GATEWAYS[_connectedGateways[0]],GATEWAYS[_connectedGateways[1]],GATEWAYS[_connectedGateways[2]]]
                (_r0,_d0) = tagsData.get((_tagMac,_connectedGateways[0]))
                (_r1,_d1) = tagsData.get((_tagMac,_connectedGateways[1]))
                (_r2,_d2) = tagsData.get((_tagMac,_connectedGateways[2]))
                _distances = [_d0/LayoutScale,_d1/LayoutScale,_d2/LayoutScale]
                (_loc0,_loc1) = getLocation(_locations,_distances,(0.0,0.0))
                foundLocations.append({"tagMac":_tagMac, "locX":round(int(_loc0)), "locY":round(int(_loc1))})
    #print(foundLocations)
    return foundLocations


initializationRoutine()