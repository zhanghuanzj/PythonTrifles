# -*- coding: GBK -*-
import sqlite3

#query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
#query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
class DataBase(object):
	def __init__(self):
		self.conn = sqlite3.connect('../test.db')
		self.cursor = self.conn.cursor()

	def fun(self):
		self.cursor.execute('create table user(name varchar(20) primary key, password varchar(20), exp INT , nextExp INT,hp INT,maxhp INT,lv INT, money INT, fire INT, needle INT)')

	#Judge weither the item is exist	  
	def isExist(self, query):
		exist = False
		item = self.cursor.execute(query)
		if item.fetchone():
			exist = True
		return exist

	#Store the item
	def store(self,query):
		self.cursor.execute(query)

	def login(self, username, password):
		print username,password
		query = '''SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
		print query
		return self.isExist(query)

	def register(self, username, password):
		query = '''SELECT * FROM user WHERE name = '%s' ''' % (username,)
		if self.isExist(query):
			return False
		else:
			storage = '''insert into user (name, password, exp, nextExp, hp, maxhp, lv, money, fire, needle) values ('%s', '%s', 0, 100, 200, 200, 0, 100, 1, 1)''' % (username,password)
			self.store(storage)
			return True

	def getPlayer(self, username, password, player):
		query = ''' SELECT * FROM user WHERE name = '%s' AND password = '%s' ''' % (username,password)
		item = self.cursor.execute(query)
		result = item.fetchone()
		player.name = username
		player.password = password
		player.exp = int(result[2])
		player.nextExp = int(result[3])
		player.hp = int(result[4])
		player.maxhp = int(result[5])
		player.lv = int(result[6])
		player.money = int(result[7])
		player.fire = int(result[8])
		player.needle = int(result[9])
		player.x = 0
		player.z = -18
		player.fireDamage = 20 + 2 * player.lv
		player.magicDamage =  30 + 5 * player.lv
		player.isDead = False
		player.isOver = False

	    #user information store interval
	def userInformationStore(self, player):
		query = ''' update user set exp = '%d',nextExp = '%d',hp = '%d',maxhp = '%d',lv = '%d',money = '%d',fire = '%d',needle = '%d' where name = '%s' ''' % (player.exp, player.nextExp, player.maxhp, player.maxhp, player.lv, player.money, player.fire, player.needle, player.name)
		self.store(query)

	def commit(self):
		self.conn.commit()
		
	def close(self):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()
#db = DataBase()
# db.fun()
# db.close()
