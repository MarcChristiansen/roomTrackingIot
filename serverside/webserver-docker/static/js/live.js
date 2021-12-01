const container = document.querySelector("#canvasContainer");
const nav = document.querySelector("#nav");
const canvas = document.querySelector("#live");
const ctx = canvas.getContext("2d");
let livingActive = false;
let toiletActive = false;

function scaleCanvas(){
    const availableHeight = window.innerHeight - nav.offsetHeight;
    const availableWidth = window.innerWidth;

    if(availableHeight < availableWidth){
        canvas.height = availableHeight;
        canvas.width = availableHeight;
    } else {
        canvas.height = availableWidth;
        canvas.width = availableWidth;
    }
}

function scaleX(coordinate){
    return coordinate / 1000 * canvas.width;
}

function scaleY(coordinate){
    return coordinate / 1000 * canvas.height;
}

function drawScaledLine(startX, startY, endX, endY, width){
    ctx.beginPath();
    ctx.moveTo(scaleX(startX), scaleY(startY));
    ctx.lineTo(scaleX(endX), scaleY(endY));
    ctx.lineWidth = scaleX(width);
    ctx.stroke();
}

function drawScaledRect(x, y, width, height, colour){
    ctx.beginPath();
    ctx.fillStyle = colour;
    ctx.fillRect(scaleX(x), scaleY(y), scaleX(width), scaleY(height));
}

function drawScaledText(x, y, fontSize, text){
    ctx.fillStyle = "black";
    ctx.font = scaleX(fontSize) + "px Arial";
    ctx.fillText(text, scaleX(x), scaleY(y));
}

function drawRoomOutline(){
    drawScaledLine(45, 50, 955, 50, 10);
    drawScaledLine(50, 50, 50, 950, 10);
    drawScaledLine(45, 950, 955, 950, 10);
    drawScaledLine(950, 950, 950, 50, 10);

    drawScaledLine(45, 550, 505, 550, 10);
    drawScaledLine(500, 550, 500, 600, 10);
    drawScaledLine(500, 600, 450, 750, 10);
    drawScaledLine(500, 750, 500, 950, 10);
}

function drawLiving(){
    if(livingActive){
        drawScaledRect(50, 50, 900, 500, "green");
        drawScaledRect(500, 500, 450, 450, "green");
    }
}

function drawToilet(){
    if(toiletActive){
        drawScaledRect(50, 550, 450, 400, "green");
    }
}

function setLiving(active){
    livingActive = active;
}

function setToilet(active){
    toiletActive = active;
}

function loop(){
    scaleCanvas();
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawLiving();
    drawToilet();
    drawRoomOutline();
    drawScaledText(370, 350, 50, "Living Room");
    drawScaledText(220, 760, 50, "Toilet");

    window.requestAnimationFrame(loop);
}

window.requestAnimationFrame(loop);