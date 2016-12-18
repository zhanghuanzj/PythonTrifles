import socket
import select
import threading
import sqlite3

class ChatRoomServer:
    def __init__(self):
        # Address
        HOST = socket.gethostname()
        PORT = 7777
        # Listen Socket initialize
        self.listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listen_socket.bind( (HOST,PORT) )
        self.listen_socket.listen(5)
        # Information
        self.clients = {}   
        self.inputs = [self.listen_socket]

    def process(self):
        while True:
            print 'Wating for request...'
            rs,ws,es = select.select(self.inputs,[],[])
            for r in rs:
                if r is self.listen_socket:     #listen socket
                    connect_socket,addr = self.listen_socket.accept()
                    print 'Connected from :', addr
                    self.inputs.append(connect_socket)
                    connect_socket.sendall('Login or Register?\r\n')
                else:                           #client socket
                    t = threading.Thread(target=self.client_handle,args=(r,))
                    t.start()
        self.listen_socket.close()

    def client_handle(self,c_socket):
        if c_socket not in self.clients:
            self.user_handle(c_socket)
        else:
            try:
                message = c_socket.recv(1024)
                disconnected = not message
            except socket.error:
                disconnected = True
            if disconnected:
                print c_socket.getpeername(),' disconnected'
                self.inputs.remove(c_socket)
                del self.clients[c_socket]
                c_socket.close()
            else:
                print message
    
    def user_handle(self,c_socket):
        is_login_success = False
        command = c_socket.recv(1024)
        if command in ( 'Login', 'login'):
            while True:
                c_socket.sendall('Please entry the username and password:\r\n')
                info = c_socket.recv(1024).split(' ')
                username = info[0]
                password = info[1]
                print username,password
                if not self.user_login(username,password):
                    c_socket.sendall('Login error please try again!\r\n')
                else:
                    c_socket.sendall('Login success,welcome to the game lobby!\r\n' )
                    self.clients[c_socket] = username
                    break
        elif command in ('Register','register'):
            self.user_register(c_socket)
        else :
            c_socket.sendall('Command Error!\r\n')
        return is_login_success  
    
    def is_exist(self,query):
        exist = False
        #Database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        item = cursor.execute(query)
        if item.fetchone() != None:
            exist = True
        cursor.close()
        conn.close()
        return exist

    def user_login(self,username,password):
        query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
        return self.is_exist(query)

    def user_register(self,c_socket):
        c_socket.sendall('Please entry your username and password:\r\n')
        while True:   
            info = c_socket.recv(1024).split(' ')
            username = info[0]
            password = info[1]
            query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
            if self.is_exist(query):
                c_socket.sendall('The username is exist,please entry another one!\r\n')
            else :
                #Database
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()
                storage = '''insert into user (name,password) values ('%s','%s')''' % (username,password)
                cursor.execute(storage)
                conn.commit()
                cursor.close()
                conn.close()
                c_socket.sendall('Register success,please login!\r\n')
                break

    def fun():
        #Database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('create table user(name varchar(20) primary key, password varchar(20))')
        cursor.execute('insert into user (name,password) values (\'zhanghuanzj\',\'12345678\')')
        cursor.close()
        conn.commit()
        conn.close()

server = ChatRoomServer()
server.process()
