import socket
import select
import sqlite3
import time
import random
from string import maketrans
from threading import Timer 

CONNECTED,LOGIN,REGISTER,ENTER,ENROLL,CHECK,ONLINE = 0,1,2,3,4,5,6

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
        self.begin_time = time.time()

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
        self.is_first = True
        self.gaming = 30
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
            print 'Waiting for request...'
            # 21Game
            current_time = time.localtime(time.time())
            if current_time[4] in (0,30):
                if self.is_first or (current_time[4] != self.gaming):
                    self.gaming = current_time[4]
                    self.game_start()

            rs,ws,es = select.select(self.inputs,[],[],2)
            for r_socket in rs:
                if r_socket is self.listen_socket:     #listen socket
                    connect_socket,addr = self.listen_socket.accept()
                    print 'Connected from :', addr
                    self.inputs.append(connect_socket)
                    self.clients[connect_socket] = ConnectionInformation()
                    connect_socket.sendall('$:Login or Register?\r\n')
                else:                           #client socket
                    try:
                        message = self.readline(r_socket)
                        disconnected = False
                    except Exception:
                        disconnected = True
                    if disconnected:
                        self.user_offline(r_socket)
                    else:
                        print '----------------------------service----------------------------'
                        self.command_handle(r_socket,message)
        self.listen_socket.close()
    
    def command_handle(self,c_socket,message):
        if self.clients[c_socket].state == CONNECTED:
            if message == 'login':
                self.clients[c_socket].state = LOGIN
                c_socket.sendall('$:Please entry the username:\r\n')
            elif message == 'register':
                self.clients[c_socket].state = REGISTER
                c_socket.sendall('$:Please entry the username:\r\n')
            else:
                c_socket.sendall('$:Command error!\r\n')
        elif self.clients[c_socket].state == LOGIN:
            self.clients[c_socket].username = message
            self.clients[c_socket].state = ENTER
            c_socket.sendall('$:Please entry the password:\r\n')
        elif self.clients[c_socket].state == ENTER:
            self.clients[c_socket].password = message
            self.user_login(c_socket)
        elif self.clients[c_socket].state == REGISTER:
            self.clients[c_socket].username = message
            self.clients[c_socket].state = ENROLL
            c_socket.sendall('$:Please entry the password:\r\n')
        elif self.clients[c_socket].state == ENROLL:
            self.clients[c_socket].password = message
            self.clients[c_socket].state = CHECK
            c_socket.sendall('$:Please entry the password again:\r\n')
        elif self.clients[c_socket].state == CHECK:
            if self.clients[c_socket].password == message:
                self.user_register(c_socket)
            else:
                c_socket.sendall('$:Password is not consistent!\r\n')
                self.clients[c_socket].state = REGISTER
        elif self.clients[c_socket].state == ONLINE:
            #[command]
            if message == 'quitroom':
                self.quit_room(c_socket)
            elif message == 'quit':
                self.user_offline(c_socket)
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
                        if command == 'createroom':
                            self.create_room(c_socket,value)
                        elif command == 'enterroom':
                            self.enter_room(c_socket,value)
                        elif command == 'chatall':
                            self.chatall(c_socket,value)
                        elif command == 'chatroom':
                            self.chatroom(c_socket,value)
                        elif command == '21game':
                            self.game_handle(c_socket,value)
                except Exception:
                    c_socket.sendall('$:Command error!\r\n') 

    
    def create_room(self,c_socket,roomid):
        if self.rooms.has_key(roomid):
            c_socket.sendall('$:Room %s is exist!\r\n' % (roomid,))
        else:
            username = self.clients[c_socket].username
            self.rooms[roomid] = set([username])
            self.users[username].room_id = roomid
            c_socket.sendall('$:Room %s create success!\r\n' % (roomid,))
            self.print_status()

    def enter_room(self,c_socket,roomid):
        if not self.rooms.has_key(roomid):
            c_socket.sendall('$:Room %s is not exist!\r\n' %(roomid,))
        else:
            username = self.clients[c_socket].username
            self.rooms[roomid].add(username)
            self.users[username].room_id = roomid
            c_socket.sendall('$:Enter the room %s !\r\n' % (roomid,))
            self.print_status()

    def quit_room(self,c_socket):
        username = self.clients[c_socket].username
        if self.users[username].room_id == None:
            c_socket.sendall('$:You are not in the room!\r\n')
        else:
            roomid = self.users[username].room_id
            self.rooms[roomid].remove(username)
            self.users[username].room_id = None
            c_socket.sendall('$:Quit the room %s !\r\n' % (roomid,))
            if len(self.rooms[roomid]) == 0:
                del self.rooms[roomid]
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
            c_socket.sendall('$:You are not in the room!\r\n')
        else:
            message = 'Room['+self.users[username].room_id+']:'+message
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
                c_socket.sendall('$:%s is not online!\r\n' % (user,))
        else:
            c_socket.sendall('$:There is no user named %s!\r\n' % (user,))

    def user_login(self,c_socket):
        username = self.clients[c_socket].username
        password = self.clients[c_socket].password
        query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
        if not self.is_exist(query):
            self.clients[c_socket].state = LOGIN
            c_socket.sendall('$:Login error please try again!\r\n')
        else:
            # someone has login,offline first!
            if self.users.has_key(username):
                self.user_offline(self.users[username].socket)
            self.clients[c_socket].state = ONLINE
            c_socket.sendall('$:Login success,welcome to the game lobby!\r\n' )
            #user information load
            self.users[username] = UserInformation()
            self.users[username].total_time = self.get_total_time(username)
            self.users[username].socket = c_socket
            self.print_status()

    def user_register(self,c_socket):
        username = self.clients[c_socket].username
        password = self.clients[c_socket].password
        query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
        if self.is_exist(query):
            self.clients[c_socket].state = REGISTER
            c_socket.sendall('$:The username is exist,please entry another one!\r\n')
        else :
            #Database
            storage = '''insert into user (name,password,onlineTime) values ('%s','%s',0)''' % (username,password)
            self.cursor.execute(storage)
            self.conn.commit()
            self.clients[c_socket].state = LOGIN
            c_socket.sendall('$:Register success,please login!\r\n')
            c_socket.sendall('$:Please entry the username:\r\n')

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
        self.is_first = False
        self.games.clear()  #clear the game information
        for roomid in self.rooms.keys():
            number = []
            while len(number)<4:
                number.append(random.randint(1,10))
            message = '-----------------21Game begin:'+str(number)+'---------------\r\n'
            number.sort()
            self.games[roomid] = GameInformation(number)
            for user in self.rooms[roomid]:
                self.users[user].socket.sendall(message)
        #15 seconds game time
        Timer(15,self.game_over).start()
    
    def game_over(self):
        for roomid in self.games.keys():
            if self.games[roomid].username != None:
                second = self.games[roomid].time - self.games[roomid].begin_time
                message = 'Room[%s]:The winner is %s,value is %d,use %.2f seconds!\r\n' % (roomid,self.games[roomid].username,self.games[roomid].value,second)
            else:
                message = 'Room[%s]:No winner!\r\n' % (roomid,)
            for user in self.rooms[roomid]:
                self.users[user].socket.sendall(message)
          
    def game_handle(self,c_socket,expression):
        if self.gaming:
            username = self.clients[c_socket].username
            roomid = self.users[username].room_id
            if roomid == None:
                c_socket.sendall("$:You are not in the room, can't participate in the 21Game!\r\n")    
            else:
                try:
                    if self.games[roomid].value != 21:
                        value = self.evalue(expression,self.games[roomid].number)
                        if value == 21 or value > self.games[roomid].value: #better
                            self.games[roomid].value = value
                            self.games[roomid].time = time.time()
                            self.games[roomid].username = username
                    c_socket.sendall("$:Result submitted!\r\n") 
                except Exception:
                    c_socket.sendall("$:Expression Error!\r\n") 
        else:
            c_socket.sendall('$:21Game not begin!\r\n')

    def get_numbers(self,expression):
        table = maketrans('+-*/()','      ')
        numbers = expression.translate(table).split(' ')
        check_list = []
        for num in numbers:
            if num.isdigit():
                check_list.append(int(num))
            elif num!='':
                raise Exception('Expression Error!')
        if len(check_list)!=4:
            raise Exception('Expression Error!')
        return check_list
    
    def evalue(self,expression,game_number):
        #number check
        check_list = self.get_numbers(expression)
        check_list.sort()
        for i in range(4):
            if check_list[i]!=game_number[i]:
                raise Exception('Expression Error!')
        return eval(expression)

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
            if result[0] not in ('chatall','chatroom','createroom','enterroom','21game'):
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
        print 'clients:',self.clients
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
try:
    server.process()
finally:
    server.quit()

