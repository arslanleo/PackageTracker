/*
'use strict'

var path = document.location.pathname;

console.log(path)

var mqtt = require('./static/BeaconManager/scripts/mqtt.js')
var client = mqtt.connect({ port: 1883, host: 'mqtt.bconimg.com', keepalive: 10000 });

client.subscribe('arslantopic')
client.on('message', function (topic, message) {
    console.log(message)
})
*/