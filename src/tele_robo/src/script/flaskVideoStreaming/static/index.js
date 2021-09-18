window.addEventListener('load', ()=>{
        
  resize();
  axis();
  $('#cusDso').hide();
  list = ["Jupiter","Moon","DSO"];
  currentVal = 0;
  radius = 5;
  clickableX = 120;
  clickableY = 40;
  generalColor = '#7CFC00';
});
  var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

var mouseX, mouseY;

canvas.addEventListener("mouseup", mouseUp, false);
function resize(){
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
  }

function changeClickableRigion(flag){
  if(flag == true){
    clickableY = 140;    
  }else{
    clickableY = 40;
  } 
}

$('#objects').bind('DOMNodeInserted DOMNodeRemoved', function() {
  if($('#objects').text() == 'Moon'){
    radius = 10;
    $('#cusDso').hide();
    generalColor = 'black';
    changeClickableRigion(false);
  }else if($('#objects').text() == 'Jupiter'){
    radius = 5;
    $('#cusDso').hide();
    changeClickableRigion(false);
    generalColor = '#7CFC00';
  }else{
    $('#cusDso').show();
    generalColor = '#7CFC00';
    changeClickableRigion(true);
    $("#customRadius").focus();
  }
});


function drawX(x, y) {
  if (x <clickableX && y <clickableY){
    $("#objects").text(list[currentVal]);
    currentVal += 1;
    if (currentVal>2){
      currentVal = 0;
    }
  }else{
    if($('#objects').text() == 'DSO'){
      if ($("#customRadius").val() == ''){
        radius = 15;
      }else{
        radius = $("#customRadius").val();
      }
    }
    ctx.beginPath();
    ctx.strokeStyle = generalColor;
    
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,0.4)';
    ctx.moveTo(x,y);
    ctx.lineTo(x,canvas.height/2);
    ctx.stroke();
    
    ctx.moveTo(x,y);
    ctx.lineTo(canvas.width/2,y);
    ctx.stroke();
  }

}

function axis(){
  
    ctx.strokeStyle = '#FFFC91';
    ctx.beginPath();
    ctx.moveTo(canvas.width/2, 0);
    ctx.lineTo(canvas.width/2, canvas.height);
    ctx.stroke();

    ctx.moveTo(0, canvas.height/2);
    ctx.lineTo(canvas.width, canvas.height/2);
    ctx.stroke();
}
function mouseUp(e) {
    mouseX = e.pageX - canvas.offsetLeft;
    mouseY = e.pageY - canvas.offsetTop;
    console.log(mouseX,mouseY)
    drawX(mouseX, mouseY);
}
