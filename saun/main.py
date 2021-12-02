#!/usr/bin/env python3

#VNC
#172.17.54.164:5901  172.17.154.183
#madis or password

from math import pi
from threading import BrokenBarrierError
import time
import movement
import keyboard
import cameraImage
import sys
import pidSpeed as pidS
from websockets import connect
from client import Client
from ps4controller import controller
from ps4controller import getgamestate


#Command Line Arguments
korv = "Sinine"                 #"roosa", "sinine"
move_style = "controller"       # "auto", "controller"

blue = True
#robot = "SaunMadis"
#go = False
#ws = connect("ws://localhost:8080")
#cl = Client(ws)
#cl.start()
#go, blue = cl.getter()

if blue:
    korv = "Sinine"
else:
    korv = "Roosa"

print("Stardin controlleri threadi")
cntrl = controller()
cntrl.start()


#"Otsin_palli", "Liigun_pallini","Otsin_korvi", "Viskan_palli", "Stop"
gamestate="Otsin_palli"




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



screenHalfX=320
ballX =[]
basketX = []

spinSpeed = 10
speed = 20
while True:
    while move_style == "controller":
        cameraImage.get_image("Pall")
        move_style = getgamestate()
        
        if move_style =="auto":
            print("alustan mangu tsuklit")
            break
        #if go == True:
        #   move_style ="auto"
        #   break


    
    while move_style =="auto":
        
        move_style= getgamestate()
        
        if move_style =="controller":
            print("CONTROLLER MOVEMENT ACTIVATED")
            movement.stop()
            break

        if gamestate =="Otsin_palli":

            cameraImage.get_image("Pall")
            ballX=cameraImage.getCords()

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

            cameraImage.get_image("Pall")
            ballX=cameraImage.getCords()

            if ballX[0] !=0:
                print("Liigun palli poole!")
                # 320:380 depth sensori jaoks, et pall jääks õigele kaugusele
                #palli x-koordinaat tuleb viia ekraani keskele ja siis otse liikuda
                #---mis saab kui keystone ära kaob või see muutub ( mitu palli )
                
                #print(ballX[0])
                #pid_controller(ballX[0])

                pid = pidS.pidSpeed(ballX[0])
                movement.setMovement(90, speed, pid)


                #y=420  x = 320

                #kui pall piisavalt lähedal, otsib korvi
                if ballX[1] > 600:

                    gamestate="Otsin_korvi"

            #kui pall ära kaob vahepeal
            elif ballX[0] == 0 :
                gamestate = "Otsin_palli"

            else:
                gamestate = "Otsin_palli"



        elif gamestate =="Otsin_korvi":

            cameraImage.get_image(korv)
            basketX=cameraImage.getCords()

            print("Otsin korvi!")
            #keerleb ümber palli paremale kuni vastase korv ilmub ekraanile
            movement.setMovement(0, spinSpeed, 5)
            
            if basketX[0] != 0:
                pid = pidS.pidSpeed(basketX[0])
                movement.setMovement(0, spinSpeed, pid)

                if basketX[0] > 630 and basketX[0] < 650:
                    korvi_kaugus = cameraImage.getDepth()
                    print("Korvi kaugus: " + str(korvi_kaugus))

                    # kauguse annab meetrites
                    if korvi_kaugus > 0.5:  # 0.5 on õige

                        print("Viskan palli")
                        gamestate = "Viskan_palli"
                    else:
                        print("Korv liiga lähedal, otsin uut palli")

                        # otsib uut palli, kuidas discardid roboti ees oleva palli ?
                        gamestate = "Otsin_palli"
            #korvi kaugus üle 50cm ? depthsensor?
            #kui ei ole, otsin uut palli ? või tuleks see check enne pallini jõudmist teha ?
            

    #käivitab throweri ja sõidab otse
        elif gamestate =="Viskan_palli":
            print("Viskan palli")

            #peaks jälgima viskamise ajal ka palli
            movement.throwBall(2000)

            gamestate="Otsin_palli"
            


        
        if keyboard.is_pressed("q"):
            movement.stop()
            print("Stopped by keypress")
            break
