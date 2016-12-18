import socket
import select
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
        self.clients = {}                   #user information
        self.inputs = [self.listen_socket]  #select read set
        self.rooms = {}

    def readline(self,c_socket):
        result = ''
        while True:
            c = c_socket.recv(1024)
            result += c
            if c.endswith('\n'):
                break;
            elif c == '':
                message = self.clients[c_socket]+' offline'
                raise Exception(message)
        print 'result:',result
        return result.strip()

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
                    try:
                        message = self.readline(r)
                        disconnected = False
                    except Exception:
                        disconnected = True
                    if disconnected:
                        self.offline_handle(r)
                    else:
                        print '--------------service----------------'
                        print message
                        self.client_handle(r,message)
        self.listen_socket.close()
    


    def client_handle(self,c_socket,message):
        if c_socket not in self.clients:
            self.user_handle(c_socket,message)
        else:
            index = message.find(' ')
            command = message[:index].lower()
            value = message[index+1:]
            #print 'com:',command
            #print 'val:',value
            if command == 'createroom':
                if self.rooms.has_key(value):
                    c_socket.sendall('Room ID is exist!\r\n')
                else:
                    self.rooms[value] = set([self.clients[c_socket]])
                    s = 'Room %s create success!\r\n' % (value,)
                    c_socket.sendall(s)
                    print self.rooms
                    print self.clients
    
    def user_handle(self,c_socket,command):
        is_login_success = False
        if command in ( 'Login', 'login'):
            while True:
                try:
                    c_socket.sendall('Please entry the username:\r\n')
                    username = self.readline(c_socket)
                    c_socket.sendall('Please entry the password:\r\n')
                    password = self.readline(c_socket)
                    disconnected = False
                except Exception:
                    disconnected = True
                if disconnected:
                    self.offline_handle(c_socket)
                else:
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
            try:
                info = self.readline(c_socket).split(' ')
                disconnected = False
            except Exception:
                disconnected = True
            if disconnected:
                self.offline_handle(c_socket)
            else:
                info = c_socket.recv(1024).strip().split(' ')
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

    def offline_handle(self,c_socket):
        self.inputs.remove(c_socket)
        if self.clients.has_key(c_socket):
            print '***********************************************\n'
            print self.clients[c_socket],' offline'
            print '***********************************************\n'
            del self.clients[c_socket]
        c_socket.close()

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
