import socket
import select
import sqlite3
import time

class UserInformation:
    def __init__(self):
        self.login_time = time.time()
        self.total_time = 0
        self.room_id = None
        self.socket = None

class ChatRoomServer:
    def __init__(self):
        # Database
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        # Address
        HOST = socket.gethostname()
        PORT = 7777
        # Listen Socket initialize
        self.listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listen_socket.bind( (HOST,PORT) )
        self.listen_socket.listen(5)
        # Information
        self.clients = {}                   #<socket>:username
        self.users = {}                     #<username>:information
        self.inputs = [self.listen_socket]  #select read set
        self.rooms = {}                     #<roomid>:[members]

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
        return result

    #Main loop
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
                        self.user_offline(r)
                    else:
                        print '--------------service----------------'
                        print message
                        self.command_handle(r,message)
        self.listen_socket.close()
    
    #need handle................................
    def command_handle(self,c_socket,message):
        command = message.strip()
        if c_socket not in self.clients:
            self.user_handle(c_socket,command)
        else:
            #[command]
            if command == 'quitroom':
                self.quit_room(c_socket)
            else:
                #[command]<user>(value)
                if command.startswith('chatto'):
                    pass
                else:
                    if command.find(' ') == -1:
                        raise Exception('Command error')
                    if command.startswith('createroom'):
                        self.create_room(c_socket,command[len('createroom'):])
                    elif command.startswith('enterroom'):
                        self.enter_room(c_socket,value)
                    elif command.startswith('chatall'):
                        self.chatall(c_socket,value)

    def create_room(self,c_socket,roomid):
        if self.rooms.has_key(roomid):
            c_socket.sendall('Room %s is exist!\r\n' % (roomid,))
        else:
            username = self.clients[c_socket]
            self.rooms[roomid] = set([username])
            self.users[username].room_id = roomid
            c_socket.sendall('Room %s create success!\r\n' % (roomid,))
            self.print_status()

    def enter_room(self,c_socket,roomid):
        if not self.rooms.has_key(roomid):
            c_socket.sendall('Room %s is not exist!\r\n' %(roomid,))
        else:
            username = self.clients[c_socket]
            self.rooms[roomid].add(username)
            self.users[username].room_id = roomid
            c_socket.sendall('Enter the room %s !\r\n' % (roomid,))
            self.print_status()

    def quit_room(self,c_socket):
        username = self.clients[c_socket]
        if self.users[username].room_id == None:
            c_socket.sendall('You are not in the room!\r\n')
        else:
            roomid = self.users[username].room_id
            self.rooms[roomid].remove(username)
            self.users[username].room_id = None
            c_socket.sendall('Quit the room %s !\r\n' % (roomid,))
            if len(self.rooms[roomid]) == 0:
                del self.rooms[roomid]
            self.print_status()

    def chatall(self,c_socket,message):
        username = self.clients[c_socket]
        message = username + ':' + message +'\r\n'
        for user_socket in self.clients.keys():
            if user_socket != c_socket:
                user_socket.sendall(message)

    def chatroom(self,c_socket,message):
        username = self.clients[c_socket]
        message = username + ':' + message +'\r\n'
        if self.users[username].room_id == None:
            c_socket.sendall('You are not in the room!\r\n')
        else:
            for user in self.rooms[self.users[username].room_id]:
                if user != username:
                    self.users[user].socket.sendall(message)

    def chatto(self,c_socket,user,message):
        username = self.clients[c_socket]
        message = username + ':' + message +'\r\n'
        self.users[user].socket.sendall(message)

    #Login ro Register
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
                    self.user_offline(c_socket)
                else:
                    print username,password
                    if not self.user_login(username,password):
                        c_socket.sendall('Login error please try again!\r\n')
                    else:
                        c_socket.sendall('Login success,welcome to the game lobby!\r\n' )
                        #user information load
                        self.clients[c_socket] = username
                        self.users[username] = UserInformation()
                        self.users[username].total_time = self.get_total_time(username)
                        self.users[username].socket = c_socket
                        break
        elif command in ('Register','register'):
            self.user_register(c_socket)
        else :
            c_socket.sendall('Command Error!\r\n')
        return is_login_success  
    

    def user_login(self,username,password):
        query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
        return self.is_exist(query)

    def user_register(self,c_socket):
        c_socket.sendall('Please entry your username and password:\r\n')
        while True:  
            try:
                c_socket.sendall('Username:')
                username = self.readline(c_socket)
                c_socket.sendall('Password:')
                password = self.readline(c_socket)
                disconnected = False
            except Exception:
                disconnected = True
            if disconnected:
                self.user_offline(c_socket)
            else:
                query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
                if self.is_exist(query):
                    c_socket.sendall('The username is exist,please entry another one!\r\n')
                else :
                    #Database
                    storage = '''insert into user (name,password,onlineTime) values ('%s','%s',0)''' % (username,password)
                    self.cursor.execute(storage)
                    self.conn.commit()
                    c_socket.sendall('Register success,please login!\r\n')
                    break

    def user_offline(self,c_socket):
        #inputs remove
        self.inputs.remove(c_socket)
        if self.clients.has_key(c_socket):
            print '***********************************************\n'
            print self.clients[c_socket],' offline'
            print '***********************************************\n'
            #online time update
            username = self.clients[c_socket]
            information = self.users[username]
            query = ''' UPDATE user SET onlineTime = %d WHERE name = '%s' ''' % (time.time()-information.login_time+information.total_time,self.clients[c_socket] )
            self.store(query)
            #information remove
            if information.room_id != None:
                self.quit_room(c_socket)
            del self.clients[c_socket]
            del self.users[username]
            
        c_socket.close()
    
    def get_command(self,message,number):
        strs = (message.strip()+' ').split(' ')
        if len(strs)<number:
            raise Exception('command error')
        result = []
        value = ''
        for s in strs:
            #command 
            if s != '' and len(result)!=number-1:
                result.append(s)
            elif len(result) == number-1:
                value += s
        result.append(value) 
        if number == 2:
            if result[0] not in ('chatall','chatroom','createroom','enterroom'):
                raise Exception('command error')
        elif number == 3:
            if result[0] != 'chatto':
                raise Exception('command error')
            

    def get_total_time(self,username):
        query = '''SELECT onlineTime FROM user WHERE name = '%s' ''' % (username,)
        total_time = 0
        item = self.cursor.execute(query)
        result = item.fetchone()
        if result != None:
            total_time = result[0]
        return total_time

    def is_exist(self,query):
        exist = False
        #Database
        item = self.cursor.execute(query)
        if item.fetchone() != None:
            exist = True
        return exist
    def store(self,query):
        self.cursor.execute(query)
        self.conn.commit()

    def quit(self):
        self.cursor.close()
        self.conn.close()
    
    def print_status(self):
        print '------------------------------------------------------------'
        print 'rooms:',self.rooms
        print 'users:',self.users
        print '------------------------------------------------------------'

    def fun(self):
        #Database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute('create table user(name varchar(20) primary key, password varchar(20), onlineTime INT)')
        cursor.execute('insert into user (name,password,onlineTime) values (\'zhanghuanzj\',\'12345678\',0)')
        cursor.close()
        conn.commit()
        conn.close()

server = ChatRoomServer()
server.get_command('  chatall   jfdlj  ')
try:
    server.process()
finally:
    server.quit()

