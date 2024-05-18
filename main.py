import math
import tkinter

# import {getKey} from './Input.js';    ###  change to pygame

pi = math.pi
P2 = pi/2
P3 = 3*pi/2
DR = 0.0174533 #one degree in radians
numberOfRays = 100; #Can be changed to increase "resolution on the walls"     #but actually should be 100 so that the textures arent messed up.
FOV = 60; #kind of but not really
#canvas = document.getElementById("screen");        ### should be pygame or something
#ctx = canvas.getContext("2d", { alpha: false });   ### should be pygame or something
floorOffset =  48.375 * numberOfRays/100 #48.375 for 100 rays
px=128; py=128; pdx=0; pdy=0; pa=0; #player position, deltaX, deltaY and angle of player

#with 100 rays, resolution becomes 1280x720
pointWidth = 1280/numberOfRays
pointHeight = 720/numberOfRays

root = tkinter.Tk()
root.geometry('%dx%d+%d+%d' % (1536, 804, 180, 100))
root.minsize(1536, 804)
frame = tkinter.Canvas(root, width=1536, height=804)
frame.pack()

root.mainloop()

def getKey(a):  ###  temp
    return

def fixAng(input):
    if(input<   0): input+=2*pi
    if(input>2*pi): input-=2*pi
    return input

def Movement():
    #rotates in radians if A or D is pressed
    if getKey("A"):     ###  All get key should be some keyreg from like pygame
        pa-=0.1
        if(pa<   0):
            pa+=2*pi
        pdx=math.cos(pa)*5
        pdy=math.sin(pa)*5
    if getKey("D"):
        pa+=0.1
        if(pa>2*pi):
            pa-=2*pi
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

    if (getKey("W")):

        #checks if the grid in front is empty, if so move forward
        if(mapW[ipy*mapX        +  ipx_add_xo]==0): px+=pdx
        if(mapW[ipy_add_yo*mapX +  ipx       ]==0): py+=pdy
    
    if (getKey("S")):

        #checks if the grid behind is empty, if so move backwards
        if(mapW[ipy*mapX        +  ipx_sub_xo]==0): px-=pdx
        if(mapW[ipy_sub_yo*mapX +  ipx       ]==0): py-=pdy

    

def Interactions():
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

    if (getKey("F")):
        if(mapW[ipy_add_yo*mapX+ipx_add_xo]==4): mapW[ipy_add_yo*mapX+ipx_add_xo]=0
    


def dist(ax,ay,bx,by,ang):
    return(math.sqrt((bx-ax)*(bx-ax) + (by-ay)*(by-ay)))


def drawCanvasPixel(x, y, Color):
    """
    ctx.fillStyle = "rgb"+Color     ###  ändra från ctx till typ pygame
    ctx.fillRect(x*pointWidth, y*pointHeight, pointWidth+1, pointHeight+1)
    ctx.fillStyle = "rgb(0,0,0)"; #reverts color to black after a fill. Which tixes it in some way
    """


def drawRays3D():
    Color = ""
    r=0;mx=0;my=0;mp=0;dof=0
    rx=0;ry=0;ra=0;xo=0;yo=0;disT=0
    ra=pa-DR*(FOV/2)
    if(ra<0):
        ra+=2*pi
    if(ra>2*pi): ra-=2*pi

    r=0
    while r<numberOfRays:
        r+=1
        
        vmt=0;hmt=0 #vertical and horizontal map texture number

        # ----Check horizontal line----
        dof=0
        disH=1000000;hx=px;hy=py
        aTan=-1/math.tan(ra)
        if(ra>pi):      #looking up
            ry=(((py)>>6)<<6)-0.0001
            rx=(py-ry) *aTan+px
            yo=-64
            xo=-yo*aTan 

        if(ra<pi):      
            ry=(((py)>>6)<<6)+64; rx=(py-ry) *aTan+px; yo=+64; xo=-yo*aTan #looking down
         
        if(ra==0 | ra==pi):
            rx=px; ry=py; dof=8 #looking straight left or right

        while (dof<8):
            mx=(rx)>>6; my=(ry)>>6; mp=my*mapX+mx
            if(mp>0 & mp<mapX*mapY & mapW[mp]>0):
                hmt=mapW[mp]-1; hx=rx; hy=ry; disH=dist(px,py,hx,hy,ra); dof=8; # hit wall
            else: rx+=xo; ry+=yo; dof+=1 #next line
        

        # ----Check vertical line----
        dof=0
        disV=1000000; vx=px,vy=py
        nTan=-math.tan(ra)
        if(ra>P2 & ra<P3): rx=(((px)>>6)<<6)-0.0001; ry=(px-rx) *nTan+py; xo=-64; yo=-xo*nTan #looking left
        if(ra<P2 | ra>P3): rx=(((px)>>6)<<6)+64;     ry=(px-rx) *nTan+py; xo=+64; yo=-xo*nTan #looking right
        if(ra==0 | ra==pi): rx=px; ry=py; dof=8 #looking straight up or down

        while (dof<8):
            mx=(rx)>>6; my=(ry)>>6; mp=my*mapX+mx
            if(mp>0 & mp<mapX*mapY & mapW[mp]>0): vmt=mapW[mp]-1; vx=rx; vy=ry; disV=dist(px,py,vx,vy,ra); dof=8 # hit wall
            else: rx+=xo; ry+=yo; dof+=1 #next line
        
        Shade = 1
        if(disV<disH): hmt=vmt; rx=vx; ry=vy; disT=disV; Shade=0.5
        if(disH<disV): rx=hx; ry=hy; disT=disH

        # ----Draw walls----
        ca=pa-ra
        if(ca<0): ca+=2*pi
        if(ca>2*pi): ca-=2*pi
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
            if(ra<pi):
                tx=31-tx #x walls
        else:
            tx=math.floor(ry/2)%32
            if(ra>P2 & ra<P3): tx=31-tx # y walls
            
        #loops through the points that are located where the "column line height based on distance thing" would be
        PointInColumnIndex = numberOfRays/2 - math.floor(lineH/100*numberOfRays/2)
        while PointInColumnIndex < numberOfRays/2 + math.floor(lineH/100*numberOfRays/2):
            PointInColumnIndex +=1
            c = 255/All_Textures[math.floor(ty)*32 + math.floor(tx)] * Shade #changes colors of the current point to the right value form the texture map
            ##Color = `(${c}, ${c}, ${c})`
            if(hmt==0): Color = f"({c}, {c/2}, {c/2})" #checkerboard red
            if(hmt==1): Color = f"({c}, {c}, {c/2})" #Brick yellow
            if(hmt==2): Color = f"({c/2}, {c/2}, {c})" #window blue
            if(hmt==3): Color = f"({c/2}, {c}, {c/2})" #door green
            drawCanvasPixel(r, PointInColumnIndex, Color)
            ty+=ty_step #iterates the y value of texture map
        
    
        # ----Draw floors----
        PointInColumnIndex = numberOfRays/2 + math.floor(lineH/100*numberOfRays/2)
        while PointInColumnIndex < numberOfRays:
            PointInColumnIndex +=1
            dy=PointInColumnIndex-(numberOfRays/2); deg=ra; raFix = math.cos(fixAng(pa-ra))
            tx=px/2 + math.cos(deg)*floorOffset*32/dy/raFix
            ty=py/2 + math.sin(deg)*floorOffset*32/dy/raFix
            mp=mapF[math.floor(ty/32)*mapX+math.floor(tx/32)]*32*32
            c = 255/All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] * 0.7 #changes colors of the current point to the right value form the texture map
            Color = f"({c/1.3}, {c/1.3}, {c})"
            drawCanvasPixel(r, PointInColumnIndex, Color)

    
        #----Draw ceiling----
        PointInColumnIndex = 0
        while PointInColumnIndex < numberOfRays/2 - math.floor(lineH/100*numberOfRays/2):
            PointInColumnIndex +=1
            dy=PointInColumnIndex-(numberOfRays/2); deg=ra; raFix = math.cos(fixAng(pa-ra))
            tx=px/2 - math.cos(deg)*floorOffset*32/dy/raFix
            ty=py/2 - math.sin(deg)*floorOffset*32/dy/raFix
            mp=mapC[math.floor(ty/32)*mapX+math.floor(tx/32)]*32*32
            c = 255/All_Textures[(math.floor(ty)&31)*32 + (math.floor(tx)&31)+mp] * 0.7; #changes colors of the current point to the right value form the texture map
            Color = f"(${c/2}, ${c/1.2}, ${c/2})";            
            drawCanvasPixel(r, PointInColumnIndex, Color)
        
        ra+=DR/(numberOfRays/FOV)
        if(ra<0):
            ra+=2*pi
        if(ra>2*pi):
            ra-=2*pi
    



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
def frame():
    Movement()
    drawRays3D()
    Interactions()
    #requestAnimationFrame(frame)  ###   pygame

#requestAnimationFrame(frame)
