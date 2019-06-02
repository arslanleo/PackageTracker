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

$(document).ready(function () {
    var trigger = $('.hamburger'),
        overlay = $('.overlay'),
        isClosed = false;

    trigger.click(function () {
        hamburger_cross();
    });

    function hamburger_cross() {

        if (isClosed == true) {
            overlay.hide();
            trigger.removeClass('is-open');
            trigger.addClass('is-closed');
            isClosed = false;
        } else {
            overlay.show();
            trigger.removeClass('is-closed');
            trigger.addClass('is-open');
            isClosed = true;
        }
    }

    $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
    });
});