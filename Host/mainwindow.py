import time
import socket
import traceback
while True:
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", 8080))
        info = "Apple".encode("utf-8")
        len = s.send(info)
        ret = s.recv(1024)
        if info == ret:
            print("success")
        break
    except:
        traceback.print_exc()
        time.sleep(0.1)
exit()
while True:
    
    if not ret:
        s.close()

