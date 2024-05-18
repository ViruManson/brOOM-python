import math
import tkinter



# import {getKey} from './Input.js';    ###  change to pygame
frameInteval = 2000 #milliseconds
P2 = math.pi/2
P3 = 3*math.pi/2
DR = 0.0174533 #one degree in radians
numberOfRays = 100; #Can be changed to increase "resolution on the walls"     #but actually should be 100 so that the textures arent messed up.
FOV = 60; #kind of but not really
#canvas = document.getElementById("screen");        ### should be pygame or something
#ctx = canvas.getContext("2d", { alpha: false });   ### should be pygame or something
floorOffset =  48.375 * numberOfRays/100 #48.375 for 100 rays
px=128; py=128; pdx=0; pdy=0; pa=0; #player position, deltaX, deltaY and angle of player

#with 100 rays, resolution becomes 1280x720
pointWidth = 1920/numberOfRays
pointHeight = 1080/numberOfRays

root = tkinter.Tk()
root.geometry('%dx%d+%d+%d' % (1920, 1080, 0, 0))
root.minsize(1536, 804)
frame = tkinter.Canvas(root, width=1920, height=1080)
frame.pack()

def toHex(int):
    value = hex(round(int))[2:]
    if value == "0":
        value = "00"
    return value

def fixAng(input):
    if(input<   0): input+=2*math.pi
    if(input>2*math.pi): input-=2*math.pi
    return input

def Movement(key):
    global px, py, pdx, pdy, pa
    #rotates in radians if A or D is pressed
    if key.char == 'a':     ###  All get key should be some keyreg from like pygame
        pa-=0.1
        if(pa<   0):
            pa+=2*math.pi
        pdx=math.cos(pa)*5
        pdy=math.sin(pa)*5
    if key.char == 'd':
        pa+=0.1
        if(pa>2*math.pi):
            pa-=2*math.pi
        pdx=math.cos(pa)*5
        pdy=math.sin(pa)*5
    
    #Offset to point infront of and behind player
    xo=0
    if(pdx<0):  xo=(-20)
    else:       xo=20

    yo=0
    if(pdy<0):  yo=(-20)
    else:       yo=20

    #Gets the current square of the player (i think) and some offsets for collision
    #math.floor is to immitate int variables.
    ipx=math.floor(px/64); ipx_add_xo=math.floor((px+xo)/64); ipx_sub_xo=math.floor((px-xo)/64)
    ipy=math.floor(py/64); ipy_add_yo=math.floor((py+yo)/64); ipy_sub_yo=math.floor((py-yo)/64)

    if key.char == 'w':

        #checks if the grid in front is empty, if so move forward
        if(mapW[ipy*mapX        +  ipx_add_xo]==0): px+=pdx
        if(mapW[ipy_add_yo*mapX +  ipx       ]==0): py+=pdy
    
    if key.char == 's':

        #checks if the grid behind is empty, if so move backwards
        if(mapW[ipy*mapX        +  ipx_sub_xo]==0): px-=pdx
        if(mapW[ipy_sub_yo*mapX +  ipx       ]==0): py-=pdy

    

def Interactions(key):
    global px, py, pdx, pdy, pa
    #Offset to point infront of and behind player
    Reach = 25
    xo=0
    if(pdx<0):
        xo=(-Reach)
    else: xo=Reach
    yo=0
    if(pdy<0):
        yo=(-Reach)
    else: yo=Reach

    ipx=math.floor(px/64); ipx_add_xo=math.floor((px+xo)/64)
    ipy=math.floor(py/64); ipy_add_yo=math.floor((py+yo)/64)

    if (key.char == 'e'):
        if(mapW[ipy_add_yo*mapX+ipx_add_xo]==4): mapW[ipy_add_yo*mapX+ipx_add_xo]=0
    


def dist(ax,ay,bx,by,ang):
    return(math.sqrt((bx-ax)*(bx-ax) + (by-ay)*(by-ay)))


def drawCanvasPixel(x, y, Color):

    frame.create_rectangle(x*pointWidth, y*pointHeight, (x+1)*pointWidth+1, (y+1)*pointHeight+1, fill=Color, outline="")
    """
    ctx.fillStyle = "rgb"+Color     ###  ändra från ctx till typ pygame
    ctx.fillRect(x*pointWidth, y*pointHeight, pointWidth+1, pointHeight+1)
    ctx.fillStyle = "rgb(0,0,0)"; #reverts color to black after a fill. Which tixes it in some way
    """


def drawRays3D():
    global px, py, pdx, pdy, pa, mapS
    frame.delete("all")
    Color = ""
    r=0;mx=0;my=0;mp=0;dof=0
    rx=0;ry=0;ra=0;xo=0;yo=0;disT=1
    ra=pa-DR*(FOV/2)
    if(ra<0):
        ra+=2*math.pi
    if(ra>2*math.pi): ra-=2*math.pi

    r=0
    while r<numberOfRays:
        vmt=0;hmt=0 #vertical and horizontal map texture number

        # ----Check horizontal line----
        dof=0
        disH=1000000;hx=px;hy=py
        aTan=-1/math.tan(ra)
        if(ra>math.pi):      #looking up
            ry=((math.floor((py)/64))*64)-0.0001
            rx=(py-ry) *aTan+px
            yo=-64
            xo=-yo*aTan 

        if(ra<math.pi):      
            ry=((math.floor((py)/64))*64)+64; rx=(py-ry) *aTan+px; yo=+64; xo=-yo*aTan #looking down
         
        if(ra==0 or ra==math.pi):
            rx=px; ry=py; dof=8 #looking straight left or right

        while (dof<8):
            mx=math.floor((rx)/64); my=math.floor((ry)/64); mp=my*mapX+mx
            if(mp>0 and mp<mapX*mapY and mapW[mp]>0):
                hmt=mapW[mp]-1; hx=rx; hy=ry; disH=dist(px,py,hx,hy,ra); dof=8; # hit wall
            else: rx+=xo; ry+=yo; dof+=1 #next line
        

        # ----Check vertical line----
        dof=0
        disV=1000000; vx=px; vy=py
        nTan=-math.tan(ra)
        if(ra>P2 and ra<P3): rx=((math.floor((py)/64))*64)-0.0001; ry=(px-rx) *nTan+py; xo=-64; yo=-xo*nTan #looking left
        if(ra<P2 or ra>P3): rx=((math.floor((py)/64))*64)+64;     ry=(px-rx) *nTan+py; xo=+64; yo=-xo*nTan #looking right
        if(ra==0 or ra==math.pi): rx=px; ry=py; dof=8 #looking straight up or down

        while (dof<8):
            mx=(rx)*64; my=(ry)*64; mp=my*mapX+mx
            if(mp>0 and mp<mapX*mapY and mapW[mp]>0): vmt=mapW[mp]-1; vx=rx; vy=ry; disV=dist(px,py,vx,vy,ra); dof=8 # hit wall
            else: rx+=xo; ry+=yo; dof+=1 #next line
        
        Shade = 1
        if(disV<disH): 
            hmt=vmt
            rx=vx
            ry=vy
            disT=disV
            Shade=0.5

        if(disH<disV):
            rx=hx
            ry=hy
            disT=disH

        # ----Draw walls----
        ca=pa-ra
        if(ca<0): ca+=2*math.pi
        if(ca>2*math.pi): ca-=2*math.pi
        disT=disT*math.cos(ca); #fix fisheye
        lineH=(mapS*100)/disT
        ty_step = 32/lineH*100/numberOfRays
        ty_off = 0

        #if(lineH>100) {ty_off = (lineH-100)/2; lineH=100;} #line height # was not needed for some reason. only caused distortion. 100 can be increseed for less distortion
        
        #adds texture to the walls, also fixes their dirrection and shading
        ty = ty_off*ty_step+hmt*32
        tx = 0
        if(Shade==1):
            tx=math.floor(rx/2)%32
            if(ra<math.pi):
                tx=31-tx #x walls
        else:
            tx=math.floor(ry/2)%32
            if(ra>P2 and ra<P3): tx=31-tx # y walls
            
        #loops through the points that are located where the "column line height based on distance thing" would be
        PointInColumnIndex = numberOfRays/2 - math.floor(lineH/100*numberOfRays/2)
        while PointInColumnIndex < numberOfRays/2 + math.floor(lineH/100*numberOfRays/2):
            if All_Textures[math.floor(ty)*32 + math.floor(tx)] == 0:
                c = 0
            else:
                c = 255/All_Textures[math.floor(ty)*32 + math.floor(tx)] * Shade #changes colors of the current point to the right value form the texture map
            ##Color = `#cccccc`8bit color in hex
            if(hmt==0): Color = f"#{toHex(c)}{toHex(c/2)}{toHex(c/2)}" #checkerboard red
            if(hmt==1): Color = f"#{toHex(c)}{toHex(c)}{toHex(c/2)}" #Brick yellow
            if(hmt==2): Color = f"#{toHex(c/2)}{toHex(c/2)}{toHex(c)}" #window blue
            if(hmt==3): Color = f"#{toHex(c/2)}{toHex(c)}{toHex(c/2)}" #door green
            drawCanvasPixel(r, PointInColumnIndex, Color)
            ty+=ty_step #iterates the y value of texture map
            PointInColumnIndex +=1
        
        
        # ----Draw floors----
        PointInColumnIndex = numberOfRays/2 + math.floor(lineH/100*numberOfRays/2)
        while PointInColumnIndex < numberOfRays:
            dy=PointInColumnIndex-(numberOfRays/2); deg=ra; raFix = math.cos(fixAng(pa-ra))
            print(dy)
            tx=px/2 + math.cos(deg)*floorOffset*32/dy/raFix
            ty=py/2 + math.sin(deg)*floorOffset*32/dy/raFix
            mp=mapF[math.floor(ty/32)*mapX+math.floor(tx/32)]*32*32
            if All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] == 0:
                c = 0
            else:
                c = 255/All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] * 0.7 #changes colors of the current point to the right value form the texture map
            Color = f"#{toHex(c/1.3)}{toHex(c/1.3)}{toHex(c)}"
            drawCanvasPixel(r, PointInColumnIndex, Color)
            PointInColumnIndex +=1
            

    
        #----Draw ceiling----
        PointInColumnIndex = 0
        while PointInColumnIndex < numberOfRays/2 - math.floor(lineH/100*numberOfRays/2):
            dy=PointInColumnIndex-(numberOfRays/2); deg=ra; raFix = math.cos(fixAng(pa-ra))
            tx=px/2 - math.cos(deg)*floorOffset*32/dy/raFix
            ty=py/2 - math.sin(deg)*floorOffset*32/dy/raFix
            mp=mapC[math.floor(ty/32)*mapX+math.floor(tx/32)]*32*32
            if All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] == 0:
                c = 0
            else:
                c = 255/All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] * 0.7; #changes colors of the current point to the right value form the texture map
            Color = f"#{toHex(c/2)}{toHex(c/1.2)}{toHex(c/2)}" 
            drawCanvasPixel(r, PointInColumnIndex, Color)
            PointInColumnIndex +=1
        
        ra+=DR/(numberOfRays/FOV)
        if(ra<0):
            ra+=2*math.pi
        if(ra>2*math.pi):
            ra-=2*math.pi

        r+=1
    root.after(frameInteval, drawRays3D)


mapX=8; mapY=8; mapS=mapX*mapY
mapW = [ #map of the walls
    2,2,2,2,2,4,2,2, 
    2,0,0,0,3,0,0,2, 
    2,0,0,0,0,1,0,4, 
    4,0,0,0,0,1,0,2, 
    2,0,4,2,0,0,0,2, 
    2,0,0,0,0,3,0,2, 
    2,0,0,0,3,0,0,2, 
    2,2,2,2,2,2,2,2,
]

mapF = [ #map of floor
    0,0,0,0,0,0,0,0, 
    0,2,2,2,2,2,2,0, 
    0,2,2,2,2,2,2,0, 
    0,2,2,2,2,2,2,0, 
    0,2,2,2,0,0,0,0, 
    0,2,2,2,0,0,0,0, 
    0,2,2,2,0,0,0,0, 
    0,0,0,0,0,0,0,0,
]

mapC = [ #map of ceiling
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,3,0,0,0, 
    0,0,0,0,3,0,0,0, 
    0,0,0,0,3,0,0,0, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0, 
    0,0,0,0,0,0,0,0,
]

All_Textures = [ #all 32x32 textures
    #Checkerboard
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,

    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,

    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,

    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 
    1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0, 

    #Brick
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,

    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,

    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,

    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,

    #Window
    1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,1,0,1,0,1,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,1,0,1,0,1,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,1,0,1,0,1,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,1,0,1,0,1,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,
    1,0,1,0,1,0,1,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,1,0,1,0,1,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,    
        
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 

    1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,   
        
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,  
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 
    1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 

    #Door
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,    
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,    
    0,0,0,1,1,1,1,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,1,1,1,1,0,0,0,  
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,  
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,   
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,     

    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,  
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,    
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,    
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,   
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,  
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,  
    0,0,0,1,0,0,0,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,0,0,0,1,0,0,0,  
    0,0,0,1,1,1,1,1, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 1,1,1,1,1,0,0,0,  

    0,0,0,0,0,0,0,0, 0,0,0,0,0,1,0,1, 1,0,1,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,0,0,0,0,0,0,0, 0,0,1,1,1,1,0,1, 1,0,1,1,1,1,0,0, 0,0,0,0,0,0,0,0,   
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,    
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,    
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,   
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0, 
    
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,  
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,     
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,   
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,   
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,   
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,  
    0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1, 1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,   
    0,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,
]

#Updates every when the browser wants to

   
    #requestAnimationFrame(frame)  ###   pygame

root.after(frameInteval, drawRays3D)
root.bind("<Key>", Movement)
root.bind("<Key>", Interactions)
root.mainloop()

#requestAnimationFrame(frame)
