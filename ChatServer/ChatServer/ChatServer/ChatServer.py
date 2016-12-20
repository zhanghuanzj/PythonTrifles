import socket
import select
import sqlite3
import time
import random

CONNECTED,LOGIN,REGISTER,ENTER,ENROLL,ONLINE = 0,1,2,3,4,5

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items)==0

    def push(self,item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise Exception('Expression error')
        else:
            return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

class UserInformation:
    def __init__(self):
        self.login_time = time.time()
        self.total_time = 0
        self.room_id = None
        self.socket = None

class GameInformation:
    def __init__(self,num):
        self.number = num
        self.username = None
        self.value = None
        self.time = None

class ConnectionInformation:
    def __init__(self):
        self.state = CONNECTED
        self.username = None
        self.password = None

class ChatRoomServer:
    def __init__(self):
        # Database
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.gaming = False
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
        self.games = {}                     #game

    #Main loop
    def process(self):
        while True:
            print 'Wating for request...'
            current_time = time.localtime(time.time())
            if (not self.gaming) and current_time[4] in (9,11,30,57,56):
                self.game_start()
            rs,ws,es = select.select(self.inputs,[],[],2)
            for r_socket in rs:
                if r_socket is self.listen_socket:     #listen socket
                    connect_socket,addr = self.listen_socket.accept()
                    print 'Connected from :', addr
                    self.inputs.append(connect_socket)
                    self.clients[connect_socket] = ConnectionInformation()
                    connect_socket.sendall('Login or Register?\r\n')
                else:                           #client socket
                    try:
                        message = self.readline(r_socket)
                        disconnected = False
                    except Exception:
                        disconnected = True
                    if disconnected:
                        self.user_offline(r_socket)
                    else:
                        print '--------------service----------------'
                        print message
                        self.command_handle(r_socket,message)
        self.listen_socket.close()
    
    def command_handle(self,c_socket,message):
        if self.clients[c_socket].state == CONNECTED:
            if message == 'login':
                self.clients[c_socket].state = LOGIN
                c_socket.sendall('Please entry the username:\r\n')
            elif message == 'register':
                self.clients[c_socket].state = REGISTER
                c_socket.sendall('Please entry the username:\r\n')
            else:
                c_socket.sendall('Command error!\r\n')
        elif self.clients[c_socket].state == LOGIN:
            self.clients[c_socket].username = message
            self.clients[c_socket].state = ENTER
            c_socket.sendall('Please entry the password:\r\n')
        elif self.clients[c_socket].state == ENTER:
            self.clients[c_socket].password = message
            self.user_login(c_socket)
        elif self.clients[c_socket].state == REGISTER:
            self.clients[c_socket].username = message
            self.clients[c_socket].state = ENROLL
            c_socket.sendall('Please entry the password:\r\n')
        elif self.clients[c_socket].state == ENROLL:
            self.clients[c_socket].password = message
            self.user_register(c_socket)
        elif self.clients[c_socket].state == ONLINE:
            #[command]
            if message == 'quitroom':
                self.quit_room(c_socket)
            else:
                try:
                    #[command]<user>(value)
                    if message.startswith('chatto '):
                        result = self.get_command(message,3)
                        user,words = result[1], result[2]
                        self.chatto(c_socket,user,words)
                    #[command](value)
                    else:
                        result = self.get_command(message,2)
                        command,value = result[0],result[1]
                        print "+++++:",result
                        if command == 'createroom':
                            self.create_room(c_socket,value)
                        elif command == 'enterroom':
                            self.enter_room(c_socket,value)
                        elif command == 'chatall':
                            self.chatall(c_socket,value)
                        elif command == 'chatroom':
                            self.chatroom(c_socket,message)
                except Exception:
                    c_socket.sendall('Command error!\r\n') 

    
    def create_room(self,c_socket,roomid):
        if self.rooms.has_key(roomid):
            c_socket.sendall('Room %s is exist!\r\n' % (roomid,))
        else:
            username = self.clients[c_socket].username
            self.rooms[roomid] = set([username])
            self.users[username].room_id = roomid
            c_socket.sendall('Room %s create success!\r\n' % (roomid,))
            self.print_status()

    def enter_room(self,c_socket,roomid):
        if not self.rooms.has_key(roomid):
            c_socket.sendall('Room %s is not exist!\r\n' %(roomid,))
        else:
            username = self.clients[c_socket].username
            self.rooms[roomid].add(username)
            self.users[username].room_id = roomid
            c_socket.sendall('Enter the room %s !\r\n' % (roomid,))
            self.print_status()

    def quit_room(self,c_socket):
        username = self.clients[c_socket].username
        if self.users[username].room_id == None:
            c_socket.sendall('You are not in the room!\r\n')
        else:
            roomid = self.users[username].room_id
            self.rooms[roomid].remove(username)
            self.users[username].room_id = None
            c_socket.sendall('Quit the room %s !\r\n' % (roomid,))
            if len(self.rooms[roomid]) == 0:
                del self.rooms[roomid]
                del self.games[roomid]
            self.print_status()

    def chatall(self,c_socket,message):
        username = self.clients[c_socket].username
        message = username + ':' + message +'\r\n'
        for user_socket in self.clients.keys():
            if user_socket != c_socket:
                user_socket.sendall(message)

    def chatroom(self,c_socket,message):
        username = self.clients[c_socket].username
        message = username + ':' + message +'\r\n'
        if self.users[username].room_id == None:
            c_socket.sendall('You are not in the room!\r\n')
        else:
            for user in self.rooms[self.users[username].room_id]:
                if user != username:
                    self.users[user].socket.sendall(message)
    
    def chatto(self,c_socket,user,message):
        username = self.clients[c_socket].username
        message = username + ':' + message +'\r\n'
        query = '''SELECT * FROM user WHERE name = '%s' ''' % (user,)
        if self.is_exist(query):
            if self.users.has_key(user):
                self.users[user].socket.sendall(message)
            else:
                c_socket.sendall('%s is not online!\r\n' % (user,))
        else:
            c_socket.sendall('There is no user named %s!\r\n' % (user,))

    def user_login(self,c_socket):
        username = self.clients[c_socket].username
        password = self.clients[c_socket].password
        query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
        if not self.is_exist(query):
            self.clients[c_socket].state = LOGIN
            c_socket.sendall('Login error please try again!\r\n')
        else:
            self.clients[c_socket].state = ONLINE
            c_socket.sendall('Login success,welcome to the game lobby!\r\n' )
            #user information load
            self.users[username] = UserInformation()
            self.users[username].total_time = self.get_total_time(username)
            self.users[username].socket = c_socket

    def user_register(self,c_socket):
        username = self.clients[c_socket].username
        password = self.clients[c_socket].password
        query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
        if self.is_exist(query):
            self.clients[c_socket].state = REGISTER
            c_socket.sendall('The username is exist,please entry another one!\r\n')
        else :
            #Database
            storage = '''insert into user (name,password,onlineTime) values ('%s','%s',0)''' % (username,password)
            self.cursor.execute(storage)
            self.conn.commit()
            self.clients[c_socket].state = LOGIN
            c_socket.sendall('Register success,please login!\r\n')
            c_socket.sendall('Please entry the username:\r\n')

    def user_offline(self,c_socket):
        username = self.clients[c_socket].username
        #inputs remove
        self.inputs.remove(c_socket)
        if self.clients[c_socket].state == ONLINE:
            print '***********************************************\n'
            print self.clients[c_socket].username,' offline'
            print '***********************************************\n'
            #online time update
            information = self.users[username]
            query = ''' UPDATE user SET onlineTime = %d WHERE name = '%s' ''' % (time.time()-information.login_time+information.total_time,username)
            self.store(query)
            #information remove
            if information.room_id != None:
                self.quit_room(c_socket)
            del self.users[username] 
        del self.clients[c_socket]     
        c_socket.close()
        self.print_status()
    
    def game_start(self):
        self.games.clear()
        for roomid in self.rooms.keys():
            number = []
            while len(number)<4:
                number.append(random.randint(1,10))
            self.games[roomid] = GameInformation(number)
            message = '-----------------21Game begin:'+str(number)+'---------------\r\n'
            for user in self.rooms[roomid]:
                self.users[user].socket.sendall(message)

    def readline(self,c_socket):
        result = ''
        while True:
            c = c_socket.recv(1024)
            result += c
            if c.endswith('\n'):
                break;
            elif c == '':
                message = self.clients[c_socket].username+' offline'
                raise Exception(message)
        return result.strip() 
           
    def get_command(self,message,number):
        strs = (message.strip()+' ').split(' ')
        result = []
        value = ''
        for s in strs:
            #command 
            if s != '' and len(result)!=number-1:
                result.append(s)
            elif len(result) == number-1:
                value += s+' '
        result.append(value.strip())
        if len(result)<number:
            raise Exception('command error')
        if number == 2:
            if result[0] not in ('chatall','chatroom','createroom','enterroom'):
                raise Exception('command error')
        elif number == 3:
            if result[0] != 'chatto':
                raise Exception('command error')
        return result
            

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

def evalue(expression):
    result = None
    op_stack = Stack()
    num_stack = Stack()
    index ,length= 0,len(expression)
    print eval(expression)
    while True:
        if index >= len():
            break


server = ChatRoomServer()
#print server.get_command('  chatall   jfdlj  ',2)
#print server.get_command('  chatto jack   jfdlj  ',3)
#print server.get_command('  chatto tom  d d ',3)
#print server.get_command('  chatall    ',2)
#print server.get_command('  chatto jack ',3)
#print server.get_command('  chatt tom',3)
exp = '((5-2)*(3+4))'
print exp.split(' +-*/()')
#evalue('3+3*5')
#print server.get_command('chatto zhangh fjosjo',3)
#try:
#    server.process()
#finally:
#    server.quit()

