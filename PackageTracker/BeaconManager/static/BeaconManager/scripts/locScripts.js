var nodeimg = new Image();
var tagimg = new Image();
var canvasWidth = 640;
var canvasHeight = 360;
var TAGS;
var NODES_TABLE;
var TAGS_LOCS = {};

$(document).ready(function () {
    setInterval(getLocData, 10000);     //recall after every 10 seconds
    init();
});

function init() {
    nodeimg.src = IMG_LOC_NODE;
    tagimg.src = IMG_LOC_TAG;
    document.getElementById("locCanvas").style.background = "url('" + IMG_LOC_LAYOUT + "')";
    NODES_TABLE = document.getElementById("nodesdataTable").getElementsByTagName('td');
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
        ctx.drawImage(nodeimg, res[0], res[1]);
    }
    //print tags on map
    for (var eachTag in TAGS_LOCS) {
        var Tname = eachTag;
        var Tx = TAGS_LOCS[eachTag][0];
        var Ty = TAGS_LOCS[eachTag][1];
        if (Tx>0 && Ty>0) {
            ctx.drawImage(tagimg, Tx, Ty);        //draw circle on location
            //ctx.drawImage(Tname, Tx, Ty+5);    //write tag's name over the drawn circle
        }
        
    }
    window.requestAnimationFrame(draw);
}

function calculation() {
    var nodesData = {};
    //get only those tags which have 3 transmitting nodes
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
    //calculate x,y coordinates of each tag in "nodesData"
    for (var t in nodesData) {
        var xa, ya, xb, yb, xc, yc, ra, rb, rc, X, Y;
        var temp = nodesData[t];
        //get distances of tag from each node (after dividing by map scale)
        ra = temp[0][0] / LAYOUT_SCALE;
        rb = temp[1][0] / LAYOUT_SCALE;
        rc = temp[2][0] / LAYOUT_SCALE;
        //get distances of each tag
        [xa, ya] = getNodeCoordinates(temp[0][1]);
        [xb, yb] = getNodeCoordinates(temp[1][1]);
        [xc, yc] = getNodeCoordinates(temp[2][1]);
        //get x,y coordinates of tag
        [X, Y] = calculateDistance(xa, ya, xb, yb, xc, yc, ra, rb, rc);
        //save tag's mac as a key and its x,y coordinates as vale un TAGS_LOC
        console.log(t, X, Y);
        TAGS_LOCS[t] = [X, Y];
    }
    //calculateDistance(100,100,160,120,70,150,50,36.06,60.83);
    return true;
}

function calculateDistance(xa,ya,xb,yb,xc,yc,ra,rb,rc) {
    var S = (Math.pow(xc, 2.0) - Math.pow(xb, 2.0) + Math.pow(yc, 2.0) - Math.pow(yb, 2.0) + Math.pow(rb, 2.0) - Math.pow(rc, 2.0)) / 2.0;
    var T = (Math.pow(xa, 2.0) - Math.pow(xb, 2.0) + Math.pow(ya, 2.0) - Math.pow(yb, 2.0) + Math.pow(rb, 2.0) - Math.pow(ra, 2.0)) / 2.0;
    var y = ((T * (xb - xc)) - (S * (xb - xa))) / (((ya - yb) * (xb - xc)) - ((yc - yb) * (xb - xa)));
    var x = ((y * (ya - yb)) - T) / (xb - xa);
    return ([Math.round(x), Math.round(y)]);
 // now x, y  is the estimated receiver position
}

function getNodeCoordinates(nodeMac) {
    for (var i = 0; i < NODES_TABLE.length; i++) {
        if (NODES_TABLE[i].innerText == nodeMac) {
            return (NODES_TABLE[i + 1].innerText.split(','));
        }
    }
    return null;
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
            LOCS = indata.locations;
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
            if (LOCS.length > 0) {
                for (var j = 0; j < LOCS.length; j++) {
                    TAGS_LOCS[LOCS[j].tagMac] = [LOCS[j].locX, LOCS[j].locY];
                    console.log(LOCS[j].tagMac, LOCS[j].locX, LOCS[j].locY);
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
    //var v = calculation();
}