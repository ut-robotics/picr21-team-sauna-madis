#!/usr/bin/env python3

#VNC
#172.17.54.164:5901
#madis or password

import movement
import keyboard
import cameraImage


#"Otsin_palli", "Liigun_pallini","Otsin_korvi", "Viskan_palli"
gamestate="Otsin_palli"
screenHalfX=320
ballX =[]

while True:

    if gamestate =="Otsin_palli":
        print("Hakkan palli otsima!")


        # salvestab palli kordinaadid listis
        if ballX[0] != 0:

            #Kas pall on üle joone check?
            print("Leidsin palli")
            gamestate="Liigun_pallini"

        #keerab paremale kuni ekraanile ilmub palli keypoint
        movement.spinRight()
    elif gamestate =="Liigun_pallini":
        print("Liigun palli poole!")
        #palli x-koordinaat tuleb viia ekraani keskele ja siis otse liikuda
        #---mis saab kui keystone ära kaob või see muutub ( mitu palli )
        if ballX[0] < screenHalfX-20:
            movement.turnRight()
        elif ballX[0] > screenHalfX+20:
            movement.turnLeft()
        else:
            movement.forward()


    elif gamestate =="Otsin_korvi":
        print("Otsin korvi!")
        #keerab paremale kuni korv ilmub ekraanile
        movement.spinAroundBall()
        

        #korvi kaugus üle 50cm ? depthsensor?
        #kui ei ole, otsin palli ? või tuleks see check enne pallini jõudmist teha ?
        #
        if cameraImage.getDepth > 0.5:
            gamestate="Viskan_palli"
        else:
            gamestate="Otsin_palli"


#käivitab throweri ja sõidab otse
    elif gamestate =="Viskan_palli":
        print("Viskan palli")
        movement.throwBall()

        gamestate="Otsin_palli"
        



    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break
