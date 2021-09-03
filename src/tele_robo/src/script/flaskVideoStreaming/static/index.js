var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

var mouseX, mouseY;

canvas.addEventListener("mouseup", mouseUp, false);

function drawX(x, y) {
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.moveTo(x - 20, y - 20);
    ctx.lineTo(x + 20, y + 20);
    ctx.stroke();

    ctx.moveTo(x + 20, y - 20);
    ctx.lineTo(x - 20, y + 20);
    ctx.stroke();
}

function mouseUp(e) {
    mouseX = e.pageX - canvas.offsetLeft;
    mouseY = e.pageY - canvas.offsetTop;
    console.log(mouseX,mouseY)
    drawX(mouseX, mouseY);
}