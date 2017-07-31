# -*- coding: GBK -*-
import sys

sys.path.append('..')
sys.path.append('../common_server')

import conf
from player import Player
from events import *
from dispatcher import Service, Dispatcher
from timer import TimerManager

class GameService(Service):
	def __init__(self, manager, sid = 0):
		super(GameService, self).__init__(sid)
		commands = {
			conf.MSG_CS_LOGIN 	: self._login,
			conf.MSG_CS_MOVETO 	: self._moveto,
			conf.MSG_CS_REGISTER : self._register,
			conf.MSG_CS_ROTATE 	: self._rotateto,
			conf.MSG_CS_FIREL 	: self._fireLeft,
			conf.MSG_CS_FIRER	: self._fireRight,
			conf.MSG_CS_ROOMS	: self._rooms,
			conf.MSG_CS_CREATEROOM : self._createRoom,
			conf.MSG_CS_ENTERROOM : self._enterRoom,
			conf.MSG_CS_PLAYERS	: self._players,
			conf.MSG_CS_QUIT 	: self._quit,
			conf.MSG_CS_QUITROOM: self._quitRoom,
			conf.MSG_CS_BEGIN	: self._begin,
			conf.MSG_CS_AIMED	: self._enemyAimed,
			conf.MSG_CS_AIMEDLEFT : self._enemyAimedLeft,
			conf.MSG_CS_TRAPCREATE : self._trapCreate,
			conf.MSG_CS_TRAPATTACK : self._trapAttack,
			conf.MSG_CS_TRAPBUY	: self._trapBuy,
		}
		self.manager = manager
		self.registers(commands)

	
	def _login(self, msg, host):
		confirm = MsgSCConfirm(msg.hid, conf.LOGIN_FAILED);
		userInfo = MsgCSLogin().unmarshal(msg.data)

		if msg.db.login(userInfo.name, userInfo.password) and not userInfo.name in self.manager.usernames:
			confirm.result = conf.LOGIN_SUCCESS
			player = Player(msg.hid)
			msg.db.getPlayer(userInfo.name, userInfo.password, player)
			self.manager.hidtoPlayer[msg.hid] = player
			self.manager.usernames.add(userInfo.name)
		host.sendClient(msg.hid,confirm.marshal())

	def _register(self, msg, host):
		rconfirm = MsgSCRConfirm(msg.hid, conf.REGISTER_FAILED)
		userInfo = MsgCSRegister().unmarshal(msg.data)
		if msg.db.register(userInfo.name, userInfo.password):
			rconfirm.result = conf.REGISTER_SUCCESS
		host.sendClient(msg.hid,rconfirm.marshal())

	def _moveto(self, msg, host):
		move = MsgCSMoveto().unmarshal(msg.data)
		move = MsgSCCMoveto(msg.hid, move.x, move.z)
		self.manager.hidtoPlayer[msg.hid].x = conf.DeAmplify(move.x)
		self.manager.hidtoPlayer[msg.hid].z = conf.DeAmplify(move.z)
		if not self.manager.hidtoPlayer[msg.hid].room:#not in room
			host.sendClient(msg.hid, move.marshal())#only self
		else:
			for hid in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:
				host.sendClient(hid, move.marshal())#room members

	def _rotateto(self, msg, host):
		rotate = MsgCSRotateto().unmarshal(msg.data)
		rotate = MsgSCRotateto(msg.hid, rotate.y)
		if not self.manager.hidtoPlayer[msg.hid].room:#not in room
			host.sendClient(msg.hid, rotate.marshal())#only self
		else:
			for hid in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:
				host.sendClient(hid, rotate.marshal())#room members
		

	def _fireLeft(self, msg, host):
		fire = MsgCSFireL().unmarshal(msg.data)
		fire = MsgSCFireL(msg.hid, fire.x, fire.y, fire.z)
		if not self.manager.hidtoPlayer[msg.hid].room:#not in room
			host.sendClient(msg.hid, fire.marshal())#only self
		else:
			self.sendMessageRoom(self.manager.hidtoPlayer[msg.hid].room, host, fire)	

	def _fireRight(self, msg, host):
		fire = MsgCSFireR().unmarshal(msg.data)
		fire = MsgSCFireR(msg.hid, fire.x, fire.y, fire.z)
		if not self.manager.hidtoPlayer[msg.hid].room:#not in room
			host.sendClient(msg.hid, fire.marshal())#only self
		else:
			self.sendMessageRoom(self.manager.hidtoPlayer[msg.hid].room, host, fire)

	def _rooms(self, msg, host):
		rooms = '#'.join(self.manager.roomtoHid.keys())
		room = MsgSCRooms(msg.hid, rooms)
		host.sendClient(msg.hid, room.marshal())

	def _createRoom(self, msg, host):
		room = MsgCSCreateRoom().unmarshal(msg.data)
		confirm = MsgSCCreateRoom(msg.hid, conf.CREATEROOM_FAILED)
		if not room.name in self.manager.roomtoHid.keys():
			confirm.result = conf.CREATEROOM_SUCCESS
			self.manager.roomtoHid[room.name] = [msg.hid]
			self.manager.roomtoState[room.name] = conf.ROOM_STATE_WAITING
			self.manager.hidtoPlayer[msg.hid].room = room.name

		host.sendClient(msg.hid, confirm.marshal())

	def _quitRoom(self, msg, host):
		hid = msg.hid
		if hid in self.manager.hidtoPlayer and self.manager.hidtoPlayer[hid].room:
			roomid = self.manager.hidtoPlayer[hid].room
			if roomid in self.manager.roomtoHid:
				if hid in self.manager.roomtoHid[roomid]:	#delete hid in room
					self.manager.roomtoHid[roomid].remove(hid)
				if len(self.manager.roomtoHid[roomid]) == 0:	#room empty
					del self.manager.roomtoHid[roomid]
					del self.manager.roomtoEnemy[roomid]
					del self.manager.roomtoScore[roomid]
					for t in self.manager.roomtoTimer[roomid]:
						print "cancel-------------------------"
						TimerManager.cancel(t)
					del self.manager.roomtoTimer[roomid]
			self.manager.hidtoPlayer[hid].room = None		#delete hid-roomid


	def _quit(self, msg, host):
		self._quitRoom(msg, host)
		if msg.hid in self.manager.hidtoPlayer:
			msg.db.userInformationStore(self.manager.hidtoPlayer[msg.hid])
			msg.db.commit()
			self.manager.usernames.remove(self.manager.hidtoPlayer[msg.hid].name)
			del self.manager.hidtoPlayer[msg.hid]					#delete hid-player
		if msg.hid in self.manager.hidtoEnemy:
			del self.manager.hidtoEnemy[msg.hid]
		if msg.hid in self.manager.hidtoScore:
			del self.manager.hidtoScore[msg.hid]
		if msg.hid in self.manager.hidtoTimer:
			for t in self.manager.hidtoTimer[msg.hid]:
				TimerManager.cancel(t)
			del self.manager.hidtoTimer[msg.hid]

	def _enterRoom(self, msg, host):
		room = MsgCSEnterRoom().unmarshal(msg.data)
		confirm = MsgSCEnterRoom(msg.hid, conf.ENTERROOM_SUCCESS)
		if (not room.name in self.manager.roomtoHid.keys()) or (self.manager.roomtoState[room.name] != conf.ROOM_STATE_WAITING):
			confirm.result = conf.ENTERROOM_FAILED
		else:#enter room
			self.manager.hidtoPlayer[msg.hid].room = room.name
			self.manager.roomtoHid[room.name].append(msg.hid)
		host.sendClient(msg.hid, confirm.marshal())

	def _players(self, msg, host):
		players = ''
		if msg.hid in self.manager.hidtoPlayer.keys() and self.manager.hidtoPlayer[msg.hid].room:
			for hid in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:
				players = players + self.manager.hidtoPlayer[hid].name + '#'
		confirm = MsgSCPlayers(msg.hid, players)
		host.sendClient(msg.hid, confirm.marshal())

	def _begin(self, msg, host):
		self.playersReload(msg)
		if msg.hid in self.manager.hidtoPlayer.keys() and self.manager.hidtoPlayer[msg.hid].room:
			self.manager.roomtoState[self.manager.hidtoPlayer[msg.hid].room] = conf.ROOM_STATE_GAMING #Gaming now
			self.manager.roomtoEnemy[self.manager.hidtoPlayer[msg.hid].room] = []
			self.manager.roomtoScore[self.manager.hidtoPlayer[msg.hid].room] = 0
			self.manager.roomtoNum[self.manager.hidtoPlayer[msg.hid].room] = 0
			for hid in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:
				for hid2 in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:#send hid2 info to hid
					message = MsgSCBegin(hid, self.manager.hidtoPlayer[hid2])
					host.sendClient(hid, message.marshal())
					print "d% to %d",(hid2, hid,)
		else:
			self.manager.hidtoEnemy[msg.hid] = []
			self.manager.hidtoNum[msg.hid] = 0
			self.manager.hidtoScore[msg.hid] = 0
			message = MsgSCBegin(msg.hid, self.manager.hidtoPlayer[msg.hid])
			host.sendClient(msg.hid, message.marshal())
			print msg.hid, self.manager.hidtoPlayer[msg.hid].name
	
	def playersReload(self, msg):
		if msg.hid in self.manager.hidtoPlayer.keys() and self.manager.hidtoPlayer[msg.hid].room:
			for hid in self.manager.roomtoHid[self.manager.hidtoPlayer[msg.hid].room]:
				username = self.manager.hidtoPlayer[hid].name
				password = self.manager.hidtoPlayer[hid].password
				msg.db.getPlayer(username, password, self.manager.hidtoPlayer[hid])
		else:
			username = self.manager.hidtoPlayer[msg.hid].name
			password = self.manager.hidtoPlayer[msg.hid].password
			msg.db.getPlayer(username, password, self.manager.hidtoPlayer[msg.hid])				

	def sendMessageRoom(self, roomid, host, message):
		for hid in self.manager.roomtoHid[roomid]:
			host.sendClient(hid, message.marshal())

	def getEnemy(self, hid, eid):
		if not self.manager.hidtoPlayer[hid].room :#single
			for en in self.manager.hidtoEnemy[hid]:
				if en.eid == eid:
					return en
		else:#room
			for en in self.manager.roomtoEnemy[self.manager.hidtoPlayer[hid].room]:
				if en.eid == eid:
					return en
		return None

	def sendUserMessage(self, msg, host, message):
		if not self.manager.hidtoPlayer[msg.hid].room :#single
			host.sendClient(msg.hid, message.marshal())
		else:#room
			self.sendMessageRoom(self.manager.hidtoPlayer[msg.hid].room, host, message)

	def _enemyAimed(self, msg, host):
		aimed = MsgCSAimed().unmarshal(msg.data)
		en = self.getEnemy(msg.hid, aimed.eid)
		if en:
			en.attacked(self.manager.hidtoPlayer[msg.hid], self.manager.hidtoPlayer[msg.hid].magicDamage)
			message = MsgSCAimed(en)
			self.sendUserMessage(msg, host, message)

	def _enemyAimedLeft(self, msg, host):
		aimed = MsgCSAimedLeft().unmarshal(msg.data)
		en = self.getEnemy(msg.hid, aimed.eid)
		if en:
			en.attacked(self.manager.hidtoPlayer[msg.hid], self.manager.hidtoPlayer[msg.hid].fireDamage)
			message = MsgSCAimedLeft(en, aimed.x, aimed.y, aimed.z)
			self.sendUserMessage(msg, host, message)

	def _trapBuy(self, msg, host):
		trap = MsgCSTrapBuy().unmarshal(msg.data)
		self.manager.hidtoPlayer[msg.hid].buyTrap(trap)
		message = MsgSCTrapBuy(self.manager.hidtoPlayer[msg.hid])
		self.sendUserMessage(msg, host, message)

	def _trapCreate(self, msg, host):
		trap = MsgCSTrapCreate().unmarshal(msg.data)
		self.manager.hidtoPlayer[msg.hid].getTrap(trap)
		message = MsgSCTrapCreate(self.manager.hidtoPlayer[msg.hid], trap)
		self.sendUserMessage(msg, host, message)

	def _trapAttack(self, msg, host):
		trap = MsgCSTrapAttack().unmarshal(msg.data)
		en = self.getEnemy(msg.hid, trap.eid)
		if en:
			en.trapAttack(trap, msg.hid)
			message = MsgSCTrapAttack(en)
			self.sendUserMessage(msg, host, message)
