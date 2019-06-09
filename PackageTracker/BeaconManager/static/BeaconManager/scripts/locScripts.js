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
var TAGS;
var NODES;

function init() {
    nodeimg.src = IMG_LOC_NODE;
    tagimg.src = IMG_LOC_TAG;
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

    for (var i in TAGS) {
        ctx.drawImage(tagimg, Math.round(TAGS[i].location), 30);
        ctx.fillText(TAGS[i].name, Math.round(TAGS[i].location), 30);
    }

    window.requestAnimationFrame(draw);
}

$(document).ready(function () {
    setInterval(getLocData, 5000);
    init();
});

function getLocData() {
    $.ajax({
        type: "GET",
        url: "/BeaconManager/tagsLocData",
        dataType: 'json',
        cache: "false",
        data: {},
        success: function (indata) {
            TAGS = indata.tags;
            NODES = indata.nodes;
            if (TAGS.length > 0) {
                $("#tagsdata tbody > tr").remove();
                for (var i = 0; i < TAGS.length; i++) {
                    //console.log(tags[i].name);
                    $("#tagsdata tbody").append(
                        "<tr>" +
                        "<th scope='row'>" + (i + 1) + "</th>" +
                        "<td>" + TAGS[i].name + "</td>" +
                        "<td>" + TAGS[i].location + "</td>" +
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
}