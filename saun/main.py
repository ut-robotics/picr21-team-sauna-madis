#!/usr/bin/env python3

#VNC
#172.17.54.164:5901  172.17.154.183
#madis or password

from math import pi
import time
import movement
import keyboard
import cameraImage
import sys
import pidSpeed as pidS
from websockets import connect
from client import Client

#Command Line Arguments
korv = "roosa" # "roosa", "sinine" 
move_style = "auto" # "auto", "controller"

#blue = False
#robot = "SaunMadis"
#go = False
#ws = connect("ws://localhost:8080")
#cl = Client(ws)
#cl.start()



try:
    if len(sys.argv) != 0:
        for argument in sys.argv:
            if argument == "sinine":
                print("Ründan sininst")
                korv=argument
            elif argument == "controller":

                move_style = "controller"
except:
    print("Command line arguments empty, using defaults")

if move_style== "controller":
    import controllerMovement
    controllerMovement.main()
    print("Controller juhib")


#"Otsin_palli", "Liigun_pallini","Otsin_korvi", "Viskan_palli"
gamestate="Otsin_palli"
screenHalfX=320
ballX =[]

speed = 20



print("alustan mangu tsuklit")
while move_style =="auto":
    cameraImage.get_image("Pall")
    ballX=cameraImage.getCords()

    if gamestate =="Otsin_palli":
        print("Hakkan palli otsima!")
        # salvestab palli kordinaadid listis
        if ballX[0] != 0:
            #Kas pall on üle joone check?
            print("Leidsin palli")
            movement.stop()
            gamestate="Liigun_pallini"
        #keerab paremale kuni ekraanile ilmub palli keypoint
        movement.spinRight()

    elif gamestate =="Liigun_pallini":
        if ballX[0] !=0:
            print("Liigun palli poole!")
            # 320:380 depth sensori jaoks, et pall jääks õigele kaugusele
            #palli x-koordinaat tuleb viia ekraani keskele ja siis otse liikuda
            #---mis saab kui keystone ära kaob või see muutub ( mitu palli )
            
            #print(ballX[0])
            #pid_controller(ballX[0])

            pid = pidS.pidSpeed(ballX[0])
            movement.forwardspeed(speed, pid)

            #y=420  x = 320

            #kui pall piisavalt lähedal, otsib korvi
            if ballX[1] > 410:

                gamestate="Otsin_korvi"

        #kui pall ära kaob vahepeal
        elif ballX[0] == 0 :
            gamestate = "Otsin_palli"

        else:
            gamestate = "Otsin_palli"



    elif gamestate =="Otsin_korvi":
        print("Otsin korvi!")
        #keerleb ümber palli paremale kuni vastase korv ilmub ekraanile
        movement.spinAroundBall()
        

        #korvi kaugus üle 50cm ? depthsensor?
        #kui ei ole, otsin uut palli ? või tuleks see check enne pallini jõudmist teha ?
        
        
        korvi_kaugus = cameraImage.getDepth()
        print("Korvi kaugus: " + str(korvi_kaugus))

        #kauguse annab meetrites
        if korvi_kaugus > 0.1: #0.5 on õige
            
            print("Viskan palli")
            gamestate="Viskan_palli"
        else:
            print("Korv liiga lähedal, otsin uut palli")
            
            #otsib uut palli, kuidas discardid roboti ees oleva palli ?
            gamestate="Otsin_palli"


#käivitab throweri ja sõidab otse
    elif gamestate =="Viskan_palli":
        print("Viskan palli")

        #peaks jälgima viskamise ajal ka palli
        movement.throwBall(20)

        gamestate="Otsin_palli"
        



    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break
