import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("", 5555))
    data = "some data"
    sock.sendall(bytes(data, "utf-8"))
##    result = sock.recv(1024)
##    print(result)
    sock.close()
