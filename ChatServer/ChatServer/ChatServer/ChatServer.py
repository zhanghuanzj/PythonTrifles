import socket
import select
import threading
import sqlite3

#database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('create table user(name varchar(20) primary key, password varchar(20))')
cursor.execute('insert into user (name,password) values (\'zhanghuanzj\',\'12345678\')')
cursor.close()
conn.commit()
conn.close()

def client_handle(c_socket):
    try:
        message = c_socket.recv(1024)
        disconnected = not message
    except socket.error:
        disconnected = True
    if disconnected:
        print c_socket.getpeername(),' disconnected'
        inputs.remove(c_socket)
        c_socket.close()
    else:
        print message

clients = {}   
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
            connect_socket.send('Login or Register?')
        else:
            t = threading.Thread(target=client_handle,args=(r,))
            t.start()
listen_socket.close()

