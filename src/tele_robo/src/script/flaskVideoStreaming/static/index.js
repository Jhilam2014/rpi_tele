window.addEventListener('load', ()=>{
        
    resize(); // Resizes the canvas once the window loads
    document.addEventListener('mousedown', startPainting);
    sketch();
    window.addEventListener('resize', resize);
});
    
const canvas = document.querySelector('#canvas');
   
const ctx = canvas.getContext('2d');
    
function resize(){
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
}
let coord = {x:0 , y:0}; 
let paint = false;

function getPosition(event){
  coord.x = event.clientX - canvas.offsetLeft;
  coord.y = event.clientY - canvas.offsetTop;
}
  
// The following functions toggle the flag to start
// and stop drawing
function startPainting(event){
  getPosition(event);
}
    
function sketch(){
    ctx.beginPath();
    
    ctx.moveTo(coord.x - 20, coord.y - 20);
    ctx.lineTo(coord.x + 20, coord.y + 20);
    ctx.stroke();

    ctx.moveTo(coord.x + 20, coord.y - 20);
    ctx.lineTo(coord.x - 20, coord.y + 20);
    ctx.stroke();
}

// document.getElementById("canvas").addEventListener("click", function(e){
//   var xPos = e.pageX - this.offsetLeft, 
//       yPos = e.pageY - this.offsetTop;
//       console.log(xPos,yPos);
//   addCrossHair(xPos, yPos);
// });
// var container = document.getElementById('canvas');
// function addCrossHair(x,y){
//   var img = $("<img>").attr("src", "https://i.imgur.com/TUmQf5n.png")
//   .css("height", 30)
//   .css("width", 30);
//   container.appendChild(img);
// }