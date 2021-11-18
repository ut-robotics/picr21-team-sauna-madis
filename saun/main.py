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

#Command Line Arguments
korv = "roosa" # "roosa", "sinine" 
move_style = "auto" # "auto", "controller"


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

speed=20
prev_time = time.time()
new_time = time.time()
integral_error = 0
e2 =0
Ki =0

def pid_controller(palliX):
    global prev_time, new_time, Ki, e2, integral_error

    if palliX != 0: 
        new_time = time.time()
        Ku = 1.5
        Tu = 1.25
        Kp = 0.6*Ku
        Ki = (1.2*Ku)/Tu
        Kd = (3*Ku*Tu)/40
        e = 320-palliX
    #     Kp = 1.2
        p= Kp * e
    #     print(Kp)
        integral_error += e * (new_time - prev_time)
        
    #     print(Ki)
        deriv_error = (e - e2) / (new_time - prev_time)
    #     print(Kd)
        e2 = e
        prev_time = new_time
        
        pid = Kp*e+Ki*integral_error+Kd*deriv_error

        #print("speed: " + str(speed))
        pid=int(pid/100)
        #print("pid: " + str(pid))
        if pid > 10:
            pid=15
        elif pid < -10:
            pid = -15
        movement.forwardspeed(speed, pid)



print("alustan mangu tsuklit")
while move_style =="auto":
    cameraImage.get_image()
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
            pid_controller(ballX[0])

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
            
            #otsib uut palli, kuidas discardid roboti ees olev pall ?
            gamestate="Otsin_palli"


#käivitab throweri ja sõidab otse
    elif gamestate =="Viskan_palli":
        print("Viskan palli")

        #peaks jälgima viskamise ajal ka palli
        movement.throwBall()

        gamestate="Otsin_palli"
        



    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break
