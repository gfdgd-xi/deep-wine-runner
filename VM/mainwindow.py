import socket
s = socket.socket()
host = socket.gethostname()
port = 8020
s.bind((host, port))
s.listen(5)
while True:
    client, addr = s.accept()
    print(addr)
    client.send("A".encode("utf-8"))
    client.close()