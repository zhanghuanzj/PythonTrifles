#coding=utf-8
import socket
import select
import sqlite3
import time
import json
import math

CONNECTED, LOGIN, REGISTER, ENTER, ENROLL, CHECK, ONLINE = 0, 1, 2, 3, 4, 5, 6
timer_interval = 1
AttackDistance = {'zombie':1,'hunter':2,'tank':2.5}
ZombiePosition = [(-32,0,-20,100),(-32,0,-15,100),(-35,0,-13,100),(-38,0,-13,100),(-21,0,9,100),
                  (-22,0,5.0,100),(-16,0,2.5,100),(17,0,-6.0,100),(17,0,-1.0,100),(-22,0,-16,100),
                  (-22,0,-14,100),(0,0,-23.0,100),(-2,0,-23.0,100),(1,0,-23.0,100),(15,0,20,100),
                  (18,0,20.0,150),(13,0,19.0,150),(3.6,0,11.0,150),(2,0.0,9.7,150),(24,0,7.0,300)]
class UserInformation:
    def __init__(self):
        self.socket = None
        self.user = User()


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.exp = 0
        self.nextExp = 0
        self.hp = 0
        self.maxhp = 0
        self.lv = 0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.request = None;
        self.hero = None;
class Zombie:
    def __init__(self):
        self.id = 0
        self.hp = 0
        self.type = ""
        self.x = 0
        self.y = 0
        self.z = 0
        self.deadtime = 0
        self.command = None

class ConnectionInformation:
    def __init__(self):
        self.state = CONNECTED
        self.username = None
        self.password = None
        self.message = None


class GameServer:
    def __init__(self):
        # Database
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        # Address
        HOST = "127.0.0.1"
        PORT = 7777
        # Listen Socket initialize
        self.listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listen_socket.bind( (HOST,PORT) )
        self.listen_socket.listen(5)
        # Information
        self.clients = {}                   #<socket>:ConnectionInformation
        self.users = {}                     #<username>:UserInformation
        self.inputs = [self.listen_socket]  #select read set
        self.tuser = None
        self.zombielist = []
        item = self.cursor.execute('select * from zombie ' )
        results = item.fetchall()
        if results!=None:
            for result in results:
                zom = Zombie()
                zom.id = result[0]
                zom.hp = result[1]
                zom.type = result[2]
                zom.x = ZombiePosition[zom.id][0]
                zom.y = ZombiePosition[zom.id][1]
                zom.z = ZombiePosition[zom.id][2]
                zom.deadtime = 0.0
                self.zombielist.append(zom)

	# Main loop
    def process(self):
        pre_time = time.time()
        while True:
            print 'Waiting for request...'
            current_time = time.time()
            print time.time()-current_time
            if current_time - pre_time > 3.0:
                pre_time = current_time
                print "Storing......."
                self.user_information_store()
            print time.time()-current_time
            rs,ws,es = select.select(self.inputs,[],[],2)
            for r_socket in rs:
                if r_socket is self.listen_socket:     #listen socket
                    connect_socket,addr = self.listen_socket.accept()
                    print 'Connected from :', addr
                    self.inputs.append(connect_socket)
                    self.clients[connect_socket] = ConnectionInformation()
                else:                           #client socket
                    try:
                        message = self.readline(r_socket)
                        print '----------------------------service----------------------------'
                        self.command_handle(r_socket,message)
                        #print "Message :" + message
                        disconnected = False
                    except Exception, e: 
                    	print e.message                  
                        self.user_offline(r_socket)
        self.listen_socket.close()

    #message handle
    def command_handle(self,c_socket,message):
        messages = message.split('#')
        #print "FromClient:"
        #print messages
        self.user_handle(c_socket,messages[0])
        self.user_weapon_update(c_socket,messages[1])
        self.zombie_update(c_socket,messages[2])
        c_socket.sendall(self.clients[c_socket].message)
        
        #print "ToClient:"
        #print self.clients[c_socket].message
        

    def user_weapon_update(self,c_socket,message):
        if message==None or message =='':
            return
        username = self.clients[c_socket].username
        weapons = message.split('$')
        for weapon in weapons:
            if weapon != '':
                #print weapon
                w = json.loads(weapon)
                query = '''select * from weapon where name = '%s' and weapon = '%s' ''' %(username,w['weaponName'])
                if self.is_exist(query):
                    query = '''update weapon set bullets = '%d' where name = '%s' and weapon = '%s' '''%(w['bullets'],username,w['weaponName'])
                    self.store(query)
                else:
                    query = '''insert into weapon (name,weapon,bullets) values ('%s','%s','%d') '''%(username,w['weaponName'],w['bullets'])
                    self.store(query)

    def user_weapon_acquire(self,username):
        item = self.cursor.execute('''select * from weapon where name = '%s' ''' %(username) )
        results = item.fetchall()
        if results!=None:
            for result in results:
                d = {}
                d['weaponName'] = result[1]
                d['bullets'] = int(result[2])
                weapon = json.dumps(d) + "$"
                #print weapon
                self.clients[self.users[username].socket].message += weapon

    def zombie_update(self,c_socket,message):
        self.clients[c_socket].message += '#'
        if message==None or message =='':
            return
        username = self.clients[c_socket].username
        zombies = message.split('$')
        index = 0
        for zom in zombies:
            if zom != '':
                #print zom
                zombie = json.loads(zom)
                self.zombielist[index].id = zombie['id']
                self.zombielist[index].hp = zombie['hp']
                self.zombielist[index].type = zombie['type']
                self.zombielist[index].x = zombie['x']
                self.zombielist[index].y = zombie['y']
                self.zombielist[index].z = zombie['z']
                #self.zombielist[index].deadtime = zombie['deadtime']
                self.zombielist[index].command = None
                x2 = math.pow(self.zombielist[index].x-self.users[username].user.x,2)
                y2 = math.pow(self.zombielist[index].y-self.users[username].user.y,2)
                z2 = math.pow(self.zombielist[index].z-self.users[username].user.z,2)
                distance = math.sqrt(x2+y2+z2)
                if self.zombielist[index].hp <= 0 :
                    self.zombielist[index].command = "Dead"
                    if self.zombielist[index].deadtime > 0.001:#already dead
                        if time.time()-self.zombielist[index].deadtime >30:
                            self.zombielist[index].hp = ZombiePosition[index][3]
                            self.zombielist[index].x = ZombiePosition[index][0]
                            self.zombielist[index].y = ZombiePosition[index][1]
                            self.zombielist[index].z = ZombiePosition[index][2]
                            self.zombielist[index].deadtime = 0
                            self.zombielist[index].command = "Alive"
                    else:
                        self.zombielist[index].deadtime = time.time()
                        
                else:
                    if distance <= AttackDistance[self.zombielist[index].type]:
                        self.zombielist[index].command = "Attack"
                    elif distance <= 15:
                        self.zombielist[index].command = "Move"
            index = index+1
        zombies = ""
        for zom in self.zombielist:
            zombies += json.dumps(self.get_dict(zom)) + "$"
        #print zombies
        self.clients[self.users[username].socket].message += zombies

    def zombie_acquire(self,username):
        zombies = ""
        for zom in self.zombielist:
            zombies += json.dumps(self.get_dict(zom)) + "$"
        self.clients[self.users[username].socket].message += '#'+zombies

    def zombie_store(self):
        index = 0
        for zombie in self.zombielist:
            query = '''update zombie set hp = '%d', x = '%f',y= '%f',z='%f',deadtime = '%f' where id = '%d' '''%(zombie.hp,zombie.x,zombie.y,zombie.z,zombie.deadtime,zombie.id)
            self.store(query)
            index += 1

    #get attribute of dicct from obj
    def get_dict(self,obj):  
        d = {}  
        for name in dir(obj):  
            value = getattr(obj, name)  
            if not name.startswith('__') and not callable(value):  
                d[name] = value  
        return d 

    #user information synchronize and handle
    def user_handle(self,c_socket,message):
        user = json.loads(message)
        self.clients[c_socket].username = user['username']
        self.tuser = user
        if user['request'] == None:#Information update
            self.user_information_update(c_socket,user)
        elif user['request'] == 'Login':
            self.user_login_handle(c_socket,user)
        elif user['request'] == 'Register':
            self.user_register_handle(c_socket,user)

    #user login 
    def user_login_handle(self,c_socket,user):
        username = user['username']
        password = user['password']
        tempuser = User()
        query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
        if not self.is_exist(query):
            tempuser.request = "LoginFail"
            self.clients[c_socket].message = json.dumps(self.get_dict(tempuser)) + "#"
        else:
            # someone has login,offline first!
            if self.users.has_key(username):
                self.user_offline(self.users[username].socket)
                self.clients[c_socket] = ConnectionInformation()
            #user information load
            self.clients[c_socket].name = username
            self.clients[c_socket].password = password
            self.users[username] = UserInformation()
            self.users[username].socket = c_socket
            self.print_status()
            self.user_logined(username, password)
            tempuser = self.users[username].user
            tempuser.request = "LoginSuccess"
            self.clients[c_socket].message = json.dumps(self.get_dict(tempuser))+"#"
            self.user_weapon_acquire(username)
            self.zombie_acquire(username)
            self.users[username].user.request = None #After login set None

    #user register
    def user_register_handle(self,c_socket,user):           
        username = user['username']
        password = user['password']
        tempuser = User()
        query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
        if self.is_exist(query):
            self.clients[c_socket].state = REGISTER
            tempuser.request = "RegisterFail"
            self.clients[c_socket].message = json.dumps(self.get_dict(tempuser)) + "#"
        else :
            #Database
            storage = '''insert into user (name,password,exp,nextExp,hp,maxhp,lv,x,y,z) values ('%s','%s',0,100,100,100,0,0.0,0.0,0.0)''' % (username,password)
            self.store(storage)
            tempuser.request = "RegisterSuccess"
            self.clients[c_socket].message = json.dumps(self.get_dict(tempuser)) + "#"

    #user information
    def user_information_update(self,c_socket,user):
        username = user['username']
        #self.users[username].username = username
        self.users[username].user.exp = user['exp']
        self.users[username].user.nextExp = user['nextExp']
        self.users[username].user.hp = user['hp']
        self.users[username].user.maxhp = user['maxhp']
        self.users[username].user.lv = user['lv']
        self.users[username].user.x = user['x']
        self.users[username].user.y = user['y']
        self.users[username].user.z = user['z']
        self.users[username].user.hero = user['hero']
        self.clients[c_socket].message = '#';

    #user information store interval
    def user_information_store(self):
        for name in self.users:
            user = self.users[name].user
            #print "Store Hero------------------"
            query = ''' update user set exp = '%d',nextExp = '%d',hp = '%d',maxhp = '%d',lv = '%d',x = '%f',y = '%f',z = '%f',hero = '%s' where name = '%s' ''' % (user.exp,user.nextExp,user.hp,user.maxhp,user.lv,user.x,user.y,user.z,user.hero,name)
            self.store(query)



    def user_offline(self,c_socket):
    	self.user_information_store()
        username = self.clients[c_socket].username
        #inputs remove
        self.inputs.remove(c_socket)
        print '***********************************************\n'
        print self.clients[c_socket].username,' offline'
        print '***********************************************\n'
        del self.users[username] 
        del self.clients[c_socket]     
        c_socket.close()
        self.print_status()
    
    def user_logined(self,username,password):
        query = ''' select * from user where name = '%s' and password = '%s' ''' % (username,password)
        item = self.cursor.execute(query)
        result = item.fetchone()
        self.users[username].user.username = result[0]
        self.users[username].user.password = result[1]
        self.users[username].user.exp = int(result[2])
        self.users[username].user.nextExp = int(result[3])
        self.users[username].user.hp = int(result[4])
        self.users[username].user.maxhp = int(result[5])
        self.users[username].user.lv = int(result[6])
        self.users[username].user.x = float(result[7])
        self.users[username].user.y = float(result[8])
        self.users[username].user.z = float(result[9])
        self.users[username].user.hero = result[10]
        

    def readline(self,c_socket):
        result = ''
        while True:
            c = c_socket.recv(1024)
            result += c
            if c.endswith('\n'):
                break
            elif c == '':
                message = self.clients[c_socket].username+' offline'
                raise Exception(message)
        return result.strip() 
         
    #Judge weither the record is exist       
    def is_exist(self, query):
        exist = False
        #Database
        item = self.cursor.execute(query)
        if item.fetchone() != None:
            exist = True
        return exist

    #Store the record
    def store(self,query):
        #print query
        self.cursor.execute(query)
        self.conn.commit()

    def quit(self):
        self.cursor.close()
        self.conn.close()
    
    def print_status(self):
        print '------------------------------------------------------------'
        print 'clients:',self.clients
        print 'users:',self.users
        print '------------------------------------------------------------'

    def fun(self):
        #Database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        #cursor.execute('create table user(name varchar(20) primary key, password varchar(20), exp INT ,hp INT,lv INT)')
        #cursor.execute('insert into user (name,password,exp,hp,lv) values (\'zhanghuanzj\',\'12345678\',0,100,1)')
        #cursor.execute('create table zombie(id INT primary key,hp INT,type varchar(20),x REAL,y REAL,z REAL)')
        cursor.execute('create table weapon(name varchar(20) , weapon varchar(20), bullets INT )')
        item = cursor.execute('select * from user where name = "zhanghuanzj" and password = "12345678"')
        result = item.fetchone()
        cursor.execute('update user set hp = 100 where name = "gujiao"')
        cursor.close()
        conn.commit()
        conn.close()

server = GameServer()  
#server.fun()
try:
    server.process()
finally:
    server.quit()

