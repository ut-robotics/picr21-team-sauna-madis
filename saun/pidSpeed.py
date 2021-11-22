import time

speed=20
prev_time = time.time()
new_time = time.time()
integral_error = 0
e2 =0
Ki =0

def pidSpeed(palliX): #palli blobi x koordinaat

    global prev_time, new_time, Ki, e2, integral_error

    if palliX != 0:
        new_time = time.time()
        Ku = 1.5
        Tu = 1.25
        Kp = 0.6 * Ku
        Ki = (1.2 * Ku) / Tu
        Kd = (3 * Ku * Tu) / 40
        e = 320 - palliX

        integral_error += e * (new_time - prev_time)

        deriv_error = (e - e2) / (new_time - prev_time)

        e2 = e
        prev_time = new_time

        pid = Kp * e + Ki * integral_error + Kd * deriv_error

        pid = int(pid / 100)

        if pid > 15:
            pid = 15
        elif pid < -15:
            pid = -15

        return(pid)