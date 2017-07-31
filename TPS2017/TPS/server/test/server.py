# -*- coding: GBK -*-

import unittest
import sys
import cPickle
import time
import struct
import math
import random

sys.path.append('..')
sys.path.append('../common')
sys.path.append('../network')
sys.path.append('../common_server')

import conf
import enemy
import player
import gameService
from gameService import GameService
from enemy import Ellephant, Bear, Bunny
from events import *
from dispatcher import Service, Dispatcher
from netStream import NetStream
from simpleHost import SimpleHost
from timer import TimerManager
from dataBase import DataBase
from pathFinding import PathFinding

BNumber = 1
ENumber = 1
interTime = 10


class Manager(object):	#Manage game dataing
	def __init__(self):
		super(Manager, self).__init__()
		self.usernames = set()

		self.hidtoScore = {}
		self.hidtoEnemy = {}
		self.hidtoTimer = {}
		self.hidtoPlayer = {}
		self.hidtoNum	= {}
		self.roomtoHid = {}
		self.roomtoEnemy = {}
		self.roomtoTimer = {}
		self.roomtoScore = {}
		self.roomtoState = {}
		self.roomtoNum	 = {}

class MsgService(object):
	def __init__(self, sid, cid, hid, data, db):
		super(MsgService, self).__init__()
		self.sid = sid
		self.cid = cid
		self.hid = hid
		self.data = data
		self.db = db

class GameServer(object):
	def __init__(self):
		self.host = SimpleHost()
		self.host.startup(7777)
		self.db = DataBase()
		self.dispatcher = Dispatcher()
		self.sid = 0
		self.pfinding = PathFinding()
		self.pfinding.readMap('../MainScene.obj')
		self.manager = Manager()

	def sendMessageRoom(self, roomid, message):
		if not roomid in self.manager.roomtoHid.keys():
			return
		for hid in self.manager.roomtoHid[roomid]:
			self.host.sendClient(hid, message.marshal())

	def countDown(self, hid, room = None):
		message = MsgSCCountDown(hid, interTime)
		if hid == -1 : 	
			self.sendMessageRoom(room, message)
		else:
			self.host.sendClient(hid, message.marshal())

	def enemyGenerate(self, turn, hid, room = None):
		#pass
		if turn == 0:
			t1 = TimerManager.addRepeatNumTimer(4, self.enemyCreate, 5, enemy.ENEMY_BUNNY, turn, hid, room)
			t2 = TimerManager.addRepeatNumTimer(6.6, self.enemyCreate, 3, enemy.ENEMY_BEAR, turn, hid, room)
			t3 = TimerManager.addRepeatNumTimer(7, self.enemyCreate, 2, enemy.ENEMY_ELEPHANT, turn, hid, room)
			if hid == -1 : 
				self.manager.roomtoTimer[room] = self.manager.roomtoTimer[room] + [t1, t2, t3]
			else:
				self.manager.hidtoTimer[hid] = self.manager.hidtoTimer[hid] + [t1, t2, t3]

		elif turn == 1:
			t1 = TimerManager.addRepeatNumTimer(4, self.enemyCreate, 6, enemy.ENEMY_BUNNY, turn, hid, room)
			t2 = TimerManager.addRepeatNumTimer(6.6, self.enemyCreate, 4, enemy.ENEMY_BEAR, turn, hid, room)
			t3 = TimerManager.addRepeatNumTimer(7, self.enemyCreate, 3, enemy.ENEMY_ELEPHANT, turn, hid, room)
			if hid == -1 :
				self.manager.roomtoTimer[room] = self.manager.roomtoTimer[room] + [t1, t2, t3]
			else:
				self.manager.hidtoTimer[hid] = self.manager.hidtoTimer[hid] + [t1, t2, t3]

		elif turn == 2:
			t1 = TimerManager.addRepeatNumTimer(4, self.enemyCreate, 7, enemy.ENEMY_BUNNY, turn, hid, room)
			t2 = TimerManager.addRepeatNumTimer(6.6, self.enemyCreate, 5, enemy.ENEMY_BEAR, turn, hid, room)
			t3 = TimerManager.addRepeatNumTimer(7, self.enemyCreate, 4, enemy.ENEMY_ELEPHANT, turn, hid, room)
			if hid == -1 : 
				self.manager.roomtoTimer[room] = self.manager.roomtoTimer[room] + [t1, t2, t3]
			else:
				self.manager.hidtoTimer[hid] = self.manager.hidtoTimer[hid] + [t1, t2, t3]
		elif turn == 3:
			print "Win============================================================"
			if hid == -1 : 
				message = MsgSCGameWin(hid)
				self.sendMessageRoom(room, message)
				self.manager.roomtoState[room] = conf.ROOM_STATE_OVER
			else:
				message = MsgSCGameWin(hid)
				self.host.sendClient(hid, message.marshal())
				self.manager.hidtoPlayer[hid].isOver = True

	def enemyCreate(self, etype, turn, hid , room = None):
		en = None
		if etype == enemy.ENEMY_BEAR:
			en = Bear(random.randint(0, 1))
		elif etype == enemy.ENEMY_BUNNY:
			en = Bunny(random.randint(0, 1))
		else:
			en = Ellephant(random.randint(0, 1))
		en.lvUp(turn)
		print "Create...........................",en.eid
		message = MsgSCEnemyCreate(hid, en)
		if hid != -1: #single
			if hid in self.manager.hidtoEnemy.keys():#still gaming
				self.host.sendClient(hid, message.marshal())
				self.manager.hidtoEnemy[hid].append(en)
				self.manager.hidtoNum[hid] += 1
		else:
			if room in self.manager.roomtoEnemy.keys():
				self.sendMessageRoom(room, message)
				self.manager.roomtoEnemy[room].append(en)
				self.manager.roomtoNum[room] += 1

	def enemyStep(self, en, nx, nz):
		x = nx - en.x
		z = nz - en.z
		t = max(math.sqrt(x*x + z*z), 0.0001)#avoid divide zero
		en.x += x * min(1, 0.03 * en.speed/t)
		en.z += z * min(1, 0.03 * en.speed/t)

	def enemyMove(self, en, hid, room = None):
		#print "x,",en.x,"z,",en.z
		nextMove = self.pfinding.pathByPosition(en.x ,en.z)
		self.enemyStep(en, nextMove[0], nextMove[1])
		message = MsgSCEMoveto(en)
		if not room:
			self.host.sendClient(hid, message.marshal())
		elif room in self.manager.roomtoHid:
			self.sendMessageRoom(room, message )

	def enemyArrive(self, en, hid, room = None):
		if not room:
			self.manager.hidtoScore[hid] += 1
			message = MsgSCEnemyArrive(en, self.manager.hidtoScore[hid])
			self.host.sendClient(hid, message.marshal())
			self.manager.hidtoEnemy[hid].remove(en)
		elif room in self.manager.roomtoHid:
			self.manager.roomtoScore[room] += 1
			message = MsgSCEnemyArrive(en, self.manager.roomtoScore[room])
			self.sendMessageRoom(room, message )
			self.manager.roomtoEnemy[room].remove(en)
			
	def enemyAttack(self, en, hid, room = None):
		if not room:
			if en.isClose(self.manager.hidtoPlayer[hid]):
				message = MsgSCEnemyAttack(en, self.manager.hidtoPlayer[hid])
				self.host.sendClient(hid, message.marshal())
				message = MsgSCAttacked(hid, self.manager.hidtoPlayer[hid])
				self.host.sendClient(hid, message.marshal())
				return True
		elif room in self.manager.roomtoHid:
			for h in self.manager.roomtoHid[room]:
				if en.isClose(self.manager.hidtoPlayer[h]):
					message = MsgSCEnemyAttack(en, self.manager.hidtoPlayer[h])
					self.sendMessageRoom(room, message)
					message = MsgSCAttacked(h, self.manager.hidtoPlayer[h])
					self.sendMessageRoom(room, message)
					return True
		return False

	def enemySeek(self, en, hid, room = None):
		if not room:
			if en.isNear(self.manager.hidtoPlayer[hid]):
				self.enemyStep(en , self.manager.hidtoPlayer[hid].x, self.manager.hidtoPlayer[hid].z)
				message = MsgSCEMoveto(en)
				self.host.sendClient(hid, message.marshal())
				return True
		elif room in self.manager.roomtoHid:
			for h in self.manager.roomtoHid[room]:
				if en.isNear(self.manager.hidtoPlayer[h]):
					self.enemyStep(en , self.manager.hidtoPlayer[h].x, self.manager.hidtoPlayer[h].z)
					message = MsgSCEMoveto(en)
					self.sendMessageRoom(room, message)
					return True
		return False

	def enemyHandle(self, en, hid, room = None):
		if self.pfinding.isArriveDest(en.x, en.z):#Enemy arrived dest
			self.enemyArrive(en, hid, room)
		elif self.enemyAttack(en, hid, room):
			pass
			#print "closing.............................................."
		elif self.enemySeek(en, hid, room):
			pass
			#print "seeking.............................................."
		else:
			self.enemyMove(en, hid, room)

	def enemyManager(self, hid, room = None):
		if not room:
			if self.manager.hidtoNum[hid] == 0:
				self.manager.hidtoNum[hid] += 1
				self.countDown(hid, room)
				self.manager.hidtoTimer[hid] = [TimerManager.addTimer(interTime, self.enemyGenerate, 0, hid, room)]
			elif self.manager.hidtoNum[hid] == 11:
				self.manager.hidtoNum[hid] += 1
				self.countDown(hid, room)
				self.manager.hidtoTimer[hid] = [TimerManager.addTimer(interTime, self.enemyGenerate, 1, hid, room)]
			elif self.manager.hidtoNum[hid] == 25:
				self.manager.hidtoNum[hid] += 1
				self.countDown(hid, room)
				self.manager.hidtoTimer[hid] = [TimerManager.addTimer(interTime, self.enemyGenerate, 2, hid, room)]
			elif self.manager.hidtoNum[hid] == 42:
				self.enemyGenerate(3, hid, room)#win
		elif room in self.manager.roomtoHid:
			if self.manager.roomtoNum[room] == 0:
				self.manager.roomtoNum[room] += 1
				self.countDown(hid, room)
				self.manager.roomtoTimer[room] = [TimerManager.addTimer(interTime, self.enemyGenerate, 0, hid, room)]
			elif self.manager.roomtoNum[room] == 11:
				self.manager.roomtoNum[room] += 1
				self.countDown(hid, room)
				self.manager.roomtoTimer[room] = [TimerManager.addTimer(interTime, self.enemyGenerate, 1, hid, room)]
			elif self.manager.roomtoNum[room] == 25:	
				self.manager.roomtoNum[room] += 1
				self.countDown(hid, room)
				self.manager.roomtoTimer[room] = [TimerManager.addTimer(interTime, self.enemyGenerate, 2, hid, room)]
			elif self.manager.roomtoNum[room] == 42:
				self.enemyGenerate(3, hid, room)#win

	def enemyUpdate(self):
		#print "++++++++++++++++++++++++++++++++"
		for hid in self.manager.hidtoEnemy.keys(): #for every single player
			if self.manager.hidtoPlayer[hid].isOver:
				continue
			if self.manager.hidtoPlayer[hid].isDead or self.manager.hidtoScore[hid] >= 10: #Game Over
				print "GameOver---------------------------------------------------------------------",hid
				self.manager.hidtoPlayer[hid].isOver = True
				message = MsgSCGameOver(hid)
				self.manager.hidtoEnemy[hid] = []
				for t in self.manager.hidtoTimer[hid]:
					TimerManager.cancel(t)
				self.host.sendClient(hid, message.marshal())
			else:
				if len(self.manager.hidtoEnemy[hid]) == 0:
					self.enemyManager(hid)
				else:
					for en in self.manager.hidtoEnemy[hid]:
						if en.hp <= 0:
							self.manager.hidtoEnemy[hid].remove(en)
							en.getMoney(self.manager.hidtoPlayer[hid])
							message = MsgSCMoney(self.manager.hidtoPlayer[hid])
							self.host.sendClient(hid, message.marshal())
						else:
							self.enemyHandle(en, hid)
		for room in self.manager.roomtoEnemy.keys() :	#for every room
			if self.manager.roomtoState[room] == conf.ROOM_STATE_OVER:
				continue
			isAllDead = True
			for hid in self.manager.roomtoHid[room]:
				if not self.manager.hidtoPlayer[hid].isDead:
					isAllDead = False
					break
			if isAllDead or self.manager.roomtoScore[room] >= 10:#Game Over
				self.manager.roomtoState[room] = conf.ROOM_STATE_OVER
				message = MsgSCGameOver(hid)
				self.manager.roomtoEnemy[room] = []
				for t in self.manager.roomtoTimer[room]:
					TimerManager.cancel(t)
				self.sendMessageRoom(room, message)
			else:
				if len(self.manager.roomtoEnemy[room]) == 0:
					self.enemyManager(-1, room)
				else:
					for en in self.manager.roomtoEnemy[room]:
						if en.hp <= 0:
							self.manager.roomtoEnemy[room].remove(en)
							en.getMoney(self.manager.hidtoPlayer[en.lastHid])
							message = MsgSCMoney(self.manager.hidtoPlayer[en.lastHid])
							self.host.sendClient(en.lastHid, message.marshal())
						else:
							self.enemyHandle(en, -1, room)

	def userInfoStore(self):
		for player in self.manager.hidtoPlayer.values():
			self.db.userInformationStore(player)

	def getCommand(self,data):
		return struct.unpack('=H', data[:2])[0]

	def process(self):#Main loop to handle request
		print "process"
		pre_time = time.time()
		TimerManager.addRepeatTimer(0.03, self.enemyUpdate)#Repeat handle Enemy
		TimerManager.addRepeatTimer(3, self.userInfoStore)#Repeat store users' data
		while 1:
			TimerManager.scheduler()
			self.host.process()
			event, hid, data = self.host.read() #read event from queue
			if event < 0:
				continue
			
			if event == conf.NET_CONNECTION_DATA:
				command = self.getCommand(data)
				if command != conf.MSG_CS_LOGIN and command != conf.MSG_CS_REGISTER and not hid in self.manager.hidtoPlayer.keys():
					continue
				else:
					msg = MsgService(self.sid, command, hid, data, self.db)
					self.dispatcher.dispatch(msg, self.host)	

			elif event == conf.NET_CONNECTION_NEW:
				self.dispatcher.register(self.sid, GameService(self.manager))

			elif event == conf.NET_CONNECTION_LEAVE:
				print "client %d leave" % (hid,)
				msg = MsgService(self.sid, conf.MSG_CS_QUIT, hid, None, self.db)
				self.dispatcher.dispatch(msg, self.host)

			current_time = time.time()
			print "FPS:%d" % (1/(current_time-pre_time+0.0001),)
			pre_time = current_time


server = GameServer()
server.process()
