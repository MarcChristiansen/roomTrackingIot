const livingRatio = document.querySelector("#living").innerHTML;
const toiletRatio = document.querySelector("#toilet").innerHTML;


function getColour(value){
    var hue = ((1 - value) * 120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
}

livingColour = getColour(livingRatio);
toiletColour = getColour(toiletRatio);

function loop(){
    scaleCanvas();
    ctx.clearRect(0, 0, canvas.width, canvas.height);  
    drawLiving(livingColour);
    drawToilet(toiletColour);
    drawRoomOutline();
    drawScaledText(320, 350, 50, "Living Room " + (livingRatio * 100) + "%");
    drawScaledText(170, 760, 50, "Toilet " + (toiletRatio * 100) + "%");

    window.requestAnimationFrame(loop);
}

window.requestAnimationFrame(loop);