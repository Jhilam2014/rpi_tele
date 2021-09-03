window.addEventListener('load', ()=>{
        
  resize();
  cross();
});
  var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

var mouseX, mouseY;

canvas.addEventListener("mouseup", mouseUp, false);
function resize(){
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
  }
function drawX(x, y) {
    ctx.beginPath();
    ctx.strokeStyle = 'white';
    ctx.moveTo(x - 2, y - 2);
    ctx.lineTo(x + 2, y + 2);
    ctx.stroke();

    ctx.moveTo(x + 2, y - 2);
    ctx.lineTo(x - 2, y + 2);
    ctx.stroke();
    
}

function cross(){
    ctx.strokeStyle = 'green';
    ctx.beginPath();
    ctx.moveTo(canvas.width/2, 0);
    ctx.lineTo(canvas.width/2, canvas.height);
    ctx.stroke();
}
function mouseUp(e) {
    mouseX = e.pageX - canvas.offsetLeft;
    mouseY = e.pageY - canvas.offsetTop;
    console.log(mouseX,mouseY)
    drawX(mouseX, mouseY);
}
