/*
window.onload = function () {
    var canvas = document.getElementById('locCanvas');      //select the canvas element
    var ctx = canvas.getContext('2d');      //create a 2d drawing object
    ctx.fillStyle = '#FF0000';      //define fill style (can be a color, gradient or pattern)
    ctx.fillRect(0, 0, 150, 75);
}
*/

var nodeimg = new Image();
var tagimg = new Image();
var canvasWidth = 640;
var canvasHeight = 360;
var mapScale = 0;
var TAGS;
var NODES_TABLE;

$(document).ready(function () {
    setInterval(getLocData, 10000);     //recall after every 10 seconds
    init();
});

function init() {
    nodeimg.src = IMG_LOC_NODE;
    tagimg.src = IMG_LOC_TAG;
    document.getElementById("locCanvas").style.background = "url('" + IMG_LOC_LAYOUT + "')";

    NODES_TABLE = document.getElementById("nodesdataTable").getElementsByTagName('td');
    //console.log(NODES_TABLE);
    
    window.requestAnimationFrame(draw);
}

function draw() {
    var canvas = document.getElementById('locCanvas');      //select the canvas element
    var ctx = canvas.getContext('2d');      //create a 2d drawing object     

    ctx.globalCompositeOperation = 'destination-over';
    ctx.clearRect(0, 0, canvasWidth, canvasHeight); // clear canvas

    ctx.fillStyle = 'rgba(0, 0, 0, 1.0)';       //define fill style (can be a color, gradient or pattern)
    ctx.strokeStyle = 'rgba(0, 153, 255, 0.4)';
    ctx.font = 'small-caps bold 8px serif';
    ctx.textAlign = 'center';
    ctx.save();
    //ctx.translate(150, 150);
    //print nodes on map
    for (var n = 1; n < NODES_TABLE.length; n += 2) {
        var res = NODES_TABLE[n].innerText.split(',');
        //console.log(res[0]);
        //console.log(res[1]);
        ctx.drawImage(nodeimg, res[0], res[1]);
    }

    for (var i in TAGS) {
        ctx.drawImage(tagimg, Math.round(TAGS[i].location), 30);        //draw circle on location
        //ctx.fillText(TAGS[i].name, Math.round(TAGS[i].location), 30);     //write tag's name over the drawn circle
    }
    //var stat = calculation();
    window.requestAnimationFrame(draw);
}

function calculation() {
    //get details of nodes displayed on the page
    var nodesData = {};
    //var nodesTable = document.getElementById("nodesdataTable").getElementsByTagName('td');
    //for (var k in table) {
    //    console.log(table[k].innerText);
    //}
    if (TAGS.length > 0) {
        for (var i = 0; i < TAGS.length; i++) {
            var tempMac = TAGS[i].mac;
            if (tempMac in nodesData == false) {
                var tempList = [];
                for (var j = 0; j < TAGS.length; j++) {
                    if (TAGS[j].mac == tempMac) {
                        tempList.push([TAGS[j].location, TAGS[j].snode]);
                    }
                }
                if (tempList.length >= 3) {
                    nodesData[tempMac] = tempList;
                }
            }
        }
    }
    else {
        return false;
    }
    console.log(nodesData);
    return true;
}

function getLocData() {
    $.ajax({
        type: "GET",
        url: "/BeaconManager/tagsLocData",
        dataType: 'json',
        cache: "false",
        data: {},
        success: function (indata) {
            TAGS = indata.tags;
            //NODES = indata.nodes;
            if (TAGS.length > 0) {
                $("#tagsdata tbody > tr").remove();
                for (var i = 0; i < TAGS.length; i++) {
                    //console.log(tags[i].name);
                    $("#tagsdata tbody").append(
                        "<tr>" +
                        "<th scope='row'>" + (i + 1) + "</th>" +
                        "<td>" + TAGS[i].name + "</td>" +
                        "<td>" + TAGS[i].location + "</td>" +
                        "<td>" + TAGS[i].snode + "</td>" +
                        "</tr>"
                    );
                }
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert("Error occurred: " + thrownError);
        },
        statusCode: {
            404: function () {
                alert("server offline");
            }
        }
    });
    var v = calculation();
}