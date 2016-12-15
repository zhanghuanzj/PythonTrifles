import socket
import select

# Address
HOST = socket.gethostname()
PORT = 7777
# Listen Socket initialize
listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_socket.bind( (HOST,PORT) )
listen_socket.listen(5)

inputs = [listen_socket]

while True:
    print 'Wating for request...'
    rs,ws,es = select.select(inputs,[],[])
    for r in rs:
        if r is listen_socket:
            connect_socket,addr = listen_socket.accept()
            print 'Connected from :', addr
            inputs.append(connect_socket)
        else:
            try:
                message = r.recv(1024)
                disconnected = not message
            except socket.error:
                disconnected = True
            if disconnected:
                print r.getpeername(),' disconnected'
                inputs.remove(r)
            else:
                print message
listen_socket.close()