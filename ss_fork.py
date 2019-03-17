import socket
import threading
import socketserver

class ForkedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

##        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        print("read", data, " in ", cur_thread)
##        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
##        socket.sendto(data.upper(), self.client_address)

class ForkedUDPServer(socketserver.ForkingMixIn, socketserver.UDPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 5555

    server = ForkedUDPServer((HOST, PORT), ForkedUDPRequestHandler)
    with server:
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        while 1:
            pass

##        client(ip, port, "Hello World 1")
##        client(ip, port, "Hello World 2")
##        client(ip, port, "Hello World 3")

##        server.shutdown()
