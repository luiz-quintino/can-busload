'''
Busload calc version 1.0
autho: Luiz Quintino
email: luiz.quintino@gmail.com
'''
def getType(type='clock'):
    bar = 'ctx = c.getContext("2d"); ctx.shadowBlur = 10; ctx.shadowOffsetX = 10;'\
        'ctx.shadowOffsetY = 10; ctx.shadowColor = "grey"; ctx.fillStyle = "black";'\
        'ctx.fillRect(100, 10, 100, 200);'\
        'ctx.shadowOffsetX = 0; ctx.shadowOffsetY = 0;'\
        'var gred = ctx.createLinearGradient(0,0,300,100); gred.addColorStop(0,"red"); gred.addColorStop(1,"white");'\
        'var gyel = ctx.createLinearGradient(0,0,300,100);gyel.addColorStop(0,"yellow");gyel.addColorStop(1,"white");'\
        'var ggr = ctx.createLinearGradient(0,0,300,200); ggr.addColorStop(0,"green"); ggr.addColorStop(1,"white");'\
        'ctx.fillStyle = gred;ctx.fillRect(100, 10, 100, 70);'\
        'ctx.fillStyle = gyel; ctx.fillRect(100, 70, 100, 40);'\
        'ctx.fillStyle = ggr; ctx.fillRect(100, 110, 100, 100);'\
        'ctx.font = "bold 10px Arial"; ctx.fillStyle = "black";ctx.fillText("100%", 205, 15);'\
        'ctx.font = "bold 10px Arial"; ctx.fillStyle = "black";ctx.fillText("70%", 205, 75);'\
        'ctx.font = "bold 10px Arial"; ctx.fillStyle = "black";ctx.fillText("50%", 205, 115);'\
        'ctx.font = "bold 10px Arial"; ctx.fillStyle = "black";ctx.fillText("0%", 205, 215);'\
        'ctx.font = "bold 15px Arial"; ctx.fillText("Bussload", 120, 235);'\
        'ctx.translate(100,(100 - pos) * 2 + 10);'\
        'ctx.beginPath();ctx.lineJoin = "round";ctx.lineTo(-20, 10);ctx.lineTo(-20, -10);ctx.lineTo(0,0);\nctx.fillStyle = "blue"; '\
        'ctx.fill();ctx.stroke();\nctx.fillText(buslload,-80,5);\n'

    clock = 'ctx = c.getContext("2d");pos = 2 * (pos+90) * Math.PI/140;var radius = c.height / 2;ctx.translate(radius,radius);var grd = ctx.createRadialGradient(0, 0, radius/3, 0, 0, radius*2);grd.addColorStop(0, "black");grd.addColorStop(1, "white");ctx.arc(0,0,radius*0.9,0,2*Math.PI);ctx.fillStyle = grd;ctx.fill();grad = ctx.createRadialGradient(0,0,radius*0.85, 0,0,radius);grad.addColorStop(0, "white");grad.addColorStop(0.5, "grey");grad.addColorStop(1, "white");ctx.strokeStyle = grad;ctx.lineWidth = radius*0.1;ctx.stroke();ctx.font="20px Arial";ctx.fillStyle = "white";ctx.textAlign = "center";ctx.fillText("Busload", 0, 60);ctx.fillText(busload,0,88);ctx.fillStyle = "white";drawNumbers(ctx, radius*.8, yb, rb);drawHand(ctx, pos, radius*0.7, radius*0.02);function drawHand(ctx, pos, length, width) {ctx.beginPath();ctx.strokeStyle = "red";ctx.lineWidth = 3;ctx.lineCap = "round";ctx.moveTo(0,0);ctx.rotate(pos);ctx.lineTo(-3,0);ctx.lineTo(-1, -length);ctx.lineTo(+1, -length);ctx.lineTo(3,0);ctx.lineTo(4,16);ctx.lineTo(-4,16);ctx.lineTo(-4,0);ctx.lineTo(0,0);ctx.fillStyle = "#F03838";ctx.fill();ctx.stroke();ctx.rotate(-pos);var grd = ctx.createRadialGradient(0, 0, 2, 0, 0, 28);grd.addColorStop(0, "red");grd.addColorStop(1, "white");ctx.beginPath();ctx.arc(0,0,10,0,2*Math.PI);ctx.fillStyle = grd;ctx.fill();}function drawNumbers(ctx, radius, yb,rb) {var ang;var num;ctx.font = radius * 0.20 + "px arial";ctx.textBaseline="middle";ctx.textAlign="center";for(num = 0; num < 11; num++){ang = (num+9) * Math.PI*2/14;ctx.rotate(ang);ctx.translate(0, -radius*0.80);ctx.rotate(-ang);var v = num * 10;ctx.fillText(v.toString(), 0, 0);ctx.rotate(ang);ctx.translate(0, radius*0.80);ctx.rotate(-ang);}ctx.beginPath();ctx.lineWidth = 9;ctx.strokeStyle = "yellow";ctx.arc(0,0,radius*1.02,yb*Math.PI/140,rb*Math.PI/140);ctx.stroke();ctx.beginPath();ctx.lineWidth = 9;ctx.strokeStyle = "red";ctx.arc(0,0,radius*1.02,rb*Math.PI/140,2*(155)*Math.PI/140);ctx.stroke();ctx.strokeStyle = "white";for(num = 0; num < 101; num++){ang = (num + 20 ) * Math.PI*2/140;ctx.rotate(ang);ctx.beginPath();ctx.moveTo(0,radius*1.1);if (num % 10 == 0){ctx.lineWidth = 2;ctx.lineTo(0,radius*0.95);} else {ctx.lineWidth = 0.6;ctx.lineTo(0,radius*0.98);}ctx.stroke();ctx.rotate(-ang);}}'

    if type == 'clock':
        return clock
    elif type == 'bar':
        return bar