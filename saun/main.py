#!/usr/bin/env python3

#VNC
#172.17.54.164:5900
#madis

import movement
import keyboard
import cameraImage

#"Otsin_palli", "Liigun_pallini","Otsin_korvi", "Viskan_palli"
gamestate=""
screenHalfX=320

while True:
    if gamestate =="Otsin_palli":
        #keerab paremale kuni ekraanile ilmub palli keypoint
        movement.spinRight()
        #salvestan palli kordinaadid listina
        ballX = cameraImage.getCords()

        if ballX[0] != 0:
            gamestate="Liigun_pallini"


    elif gamestate =="Liigun_pallini":
        #palli x-koordinaat tuleb viia ekraani keskele ja siis otse liikuda
        if ballX[0] < 
    elif gamestate =="Otsin_korvi":
        #keerab paremale kuni korv ilmub ekraanile
        movement.spinRight()
    elif gamestate =="Viskan_palli":
        movement.throwBall()
        



    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break
