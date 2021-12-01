function loop(){
    scaleCanvas();
    ctx.clearRect(0, 0, canvas.width, canvas.height);   
    drawRoomOutline();
    drawScaledText(370, 350, 50, "Living Room");
    drawScaledText(220, 760, 50, "Toilet");

    window.requestAnimationFrame(loop);
}

window.requestAnimationFrame(loop);