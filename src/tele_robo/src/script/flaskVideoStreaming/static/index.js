// // wait for the content of the window element
// // to load, then performs the operations.
// // This is considered best practice.
// window.addEventListener('load', ()=>{
        
//     resize(); // Resizes the canvas once the window loads
//     document.addEventListener('mousedown', startPainting);
//     document.addEventListener('mouseup', stopPainting);
//     document.addEventListener('mousemove', sketch);
//     window.addEventListener('resize', resize);
// });
    
// const canvas = document.querySelector('#canvas');
   
// // Context for the canvas for 2 dimensional operations
// const ctx = canvas.getContext('2d');
    
// // Resizes the canvas to the available size of the window.
// function resize(){
//   ctx.canvas.width = window.innerWidth;
//   ctx.canvas.height = window.innerHeight;
// }
    
// // Stores the initial position of the cursor
// let coord = {x:0 , y:0}; 
   
// // This is the flag that we are going to use to 
// // trigger drawing
// let paint = false;
    
// // Updates the coordianates of the cursor when 
// // an event e is triggered to the coordinates where 
// // the said event is triggered.
// function getPosition(event){
//   coord.x = event.clientX - canvas.offsetLeft;
//   coord.y = event.clientY - canvas.offsetTop;
// }
  
// // The following functions toggle the flag to start
// // and stop drawing
// function startPainting(event){
//   paint = true;
//   getPosition(event);
// }
// function stopPainting(){
//   paint = false;
// }
    
// function sketch(event){
//   if (!paint) return;
//   ctx.beginPath();
    
//   ctx.lineWidth = 5;
   
//   // Sets the end of the lines drawn
//   // to a round shape.
//   ctx.lineCap = 'round';
    
//   ctx.strokeStyle = 'green';
      
//   // The cursor to start drawing
//   // moves to this coordinate
//   ctx.moveTo(coord.x, coord.y);
   
//   // The position of the cursor
//   // gets updated as we move the
//   // mouse around.
//   getPosition(event);
   
//   // A line is traced from start
//   // coordinate to this coordinate
//   ctx.lineTo(coord.x , coord.y);
    
//   // Draws the line.
//   ctx.stroke();
// }

document.getElementById("canvas").addEventListener("click", function(e){
  var xPos = e.pageX - this.offsetLeft, 
      yPos = e.pageY - this.offsetTop;
  addMarkerImages(chart, xPos, yPos);
});


var customMarkers= [];

function addMarkerImages(chart, xPos, yPos){
  var container = $('<div/>').css("height", 30)
  .css("width", 30)
  .addClass("imageToolTip");
  var toolTip = $('<span class="tooltiptext">Information to be shown on mouseover</span>');
  var img = $("<img>").attr("src", "https://i.imgur.com/TUmQf5n.png")
  .css("height", 30)
  .css("width", 30);
  img.appendTo(container);
  toolTip.appendTo(container);
  customMarkers.push(
    {
      container: container.appendTo($("#chartContainer>.canvasjs-chart-container")),
      xPos: xPos, 
      yPos: yPos, 
      xValue: Math.round(chart.axisX[0].convertPixelToValue(xPos)),
      yValue: Math.round(chart.axisY[0].convertPixelToValue(yPos)) 
    });        
  positionMarkerImage(customMarkers[customMarkers.length - 1].container, customMarkers[customMarkers.length - 1].xPos , customMarkers[customMarkers.length - 1].yPos); 
}

function positionMarkerImage(customMarker, xPos, yPos){ 
  customMarker.css({"position": "absolute", 
                    "display": "block",
                    "top": yPos - customMarker.height()/2,
                    "left": xPos - customMarker.width()/2
                   });
}