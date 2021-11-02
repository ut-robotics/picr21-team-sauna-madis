import threading
#import main
import cameraImage

if __name__ == "__main__":
    cameraThread = threading.Thread(target=cameraImage())
    mainThread = threading.Thread(target=main())

    cameraThread.start()
    print("Alustasin cameraImage threadi")
    mainThread.start()
    print("Alustasin main threadi")