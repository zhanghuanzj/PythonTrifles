# -*- coding: GBK -*-
import conf
from header import SimpleHeader


class MsgCSLogin(SimpleHeader):
	def __init__(self, name = '', password = ''):
		super(MsgCSLogin, self).__init__(conf.MSG_CS_LOGIN)
		self.appendParam('name', name, 's')
		self.appendParam('password', password, 's')

class MsgSCConfirm(SimpleHeader):
	def __init__(self, uid, result ):
		super (MsgSCConfirm, self).__init__(conf.MSG_SC_CONFIRM)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 'i')

class MsgCSRegister(SimpleHeader):
	def __init__(self, name = '', password = ''):
		super(MsgCSRegister, self).__init__(conf.MSG_CS_REGISTER)
		self.appendParam('name', name, 's')
		self.appendParam('password', password, 's')

class MsgSCRConfirm(SimpleHeader):
	def __init__(self, uid, result = 0):
		super (MsgSCRConfirm, self).__init__(conf.MSG_SC_RCONFIRM)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 'i')

class MsgCSMoveto(SimpleHeader):
	def __init__ (self, x = 0, z = 0):
		super (MsgCSMoveto, self).__init__ (conf.MSG_CS_MOVETO)
		self.appendParam('x', x, 'i')
		self.appendParam('z', z, 'i')

class MsgSCCMoveto(SimpleHeader):
	def __init__ (self, uid, x = 0, z = 0): 
		super (MsgSCCMoveto, self).__init__ (conf.MSG_SC_MOVETO)
		self.appendParam('uid', uid, 'i')
		self.appendParam('x', x, 'i')
		self.appendParam('z', z, 'i')

class MsgCSRotateto(SimpleHeader):
	def __init__ (self, y = 0):
		super (MsgCSRotateto, self).__init__ (conf.MSG_CS_ROTATE)
		self.appendParam('y', y, 'i')

class MsgSCRotateto(SimpleHeader):
	def __init__ (self, uid, y = 0): 
		super (MsgSCRotateto, self).__init__ (conf.MSG_SC_ROTATE)
		self.appendParam('uid', uid, 'i')
		self.appendParam('y', y, 'i')

class MsgCSFireL(SimpleHeader):
	def __init__ (self, x = 0, y = 0, z = 0):
		super (MsgCSFireL, self).__init__ (conf.MSG_CS_FIREL)
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgSCFireL(SimpleHeader):
	def __init__ (self, uid, x, y, z): 
		super (MsgSCFireL, self).__init__ (conf.MSG_SC_FIREL)
		self.appendParam('uid', uid, 'i')
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgCSFireR(SimpleHeader):
	def __init__ (self, x = 0, y = 0, z = 0):
		super (MsgCSFireR, self).__init__ (conf.MSG_CS_FIRER)
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgSCFireR(SimpleHeader):
	def __init__ (self, uid, x, y, z): 
		super (MsgSCFireR, self).__init__ (conf.MSG_SC_FIRER)
		self.appendParam('uid', uid, 'i')
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgCSQuit(SimpleHeader):
	def __init__(self,):
		super(MsgCSQuit, self).__init__(conf.MSG_CS_QUIT)

class MsgCSRooms(SimpleHeader):
	def __init__(self,):
		super(MsgCSRooms, self).__init__(conf.MSG_CS_ROOMS)

class MsgSCRooms(SimpleHeader):
	def __init__(self, uid, result):
		super (MsgSCRooms, self).__init__(conf.MSG_SC_ROOMS)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 's')

class MsgCSCreateRoom(SimpleHeader):
	def __init__(self, name = ''):
		super(MsgCSCreateRoom, self).__init__(conf.MSG_CS_CREATEROOM)
		self.appendParam('name', name, 's')

class MsgSCCreateRoom(SimpleHeader):
	def __init__(self, uid, result = 0):
		super (MsgSCCreateRoom, self).__init__(conf.MSG_SC_CREATEROOM)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 'i')

class MsgCSEnterRoom(SimpleHeader):
	def __init__(self, name = ''):
		super(MsgCSEnterRoom, self).__init__(conf.MSG_CS_ENTERROOM)
		self.appendParam('name', name, 's')

class MsgSCEnterRoom(SimpleHeader):
	def __init__(self, uid, result = 0):
		super (MsgSCEnterRoom, self).__init__(conf.MSG_SC_ENTERROOM)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 'i')

class MsgCSPlayers(SimpleHeader):
	def __init__(self,):
		super(MsgCSPlayers, self).__init__(conf.MSG_CS_PLAYERS)

class MsgSCPlayers(SimpleHeader):
	def __init__(self, uid, result):
		super (MsgSCPlayers, self).__init__(conf.MSG_SC_PLAYERS)
		self.appendParam('uid', uid, 'i')
		self.appendParam('result', result, 's')

class MsgCSQuitroom(SimpleHeader):
	def __init__(self,):
		super(MsgCSQuitroom, self).__init__(conf.MSG_CS_QUITROOM)

class MsgCSBegin(SimpleHeader):
	def __init__(self,):
		super(MsgCSBegin, self).__init__(conf.MSG_CS_BEGIN)

class MsgSCBegin(SimpleHeader):
	def __init__(self, hid, player):
		super(MsgSCBegin, self).__init__(conf.MSG_SC_BEGIN)
		self.appendParam('hid', hid, 'i')
		self.appendParam('uid', player.hid, 'i')
		self.appendParam('name', player.name, 's')
		self.appendParam('maxhp', player.maxhp, 'i')
		self.appendParam('hp', player.hp, 'i')
		self.appendParam('lv', player.lv, 'i')
		self.appendParam('nextExp', player.nextExp, 'i')
		self.appendParam('exp', player.exp, 'i')
		self.appendParam('money', player.money, 'i')
		self.appendParam('fire', player.fire, 'i')
		self.appendParam('needle', player.needle, 'i')

class MsgSCEnemyCreate(SimpleHeader):
	def __init__(self, hid, enemy):
		super(MsgSCEnemyCreate, self).__init__(conf.MSG_SC_ENEMYCREATE)
		self.appendParam('hid', hid, 'i')
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('etype', enemy.etype, 'i')
		self.appendParam('x', conf.Amplify(enemy.x), 'i')
		self.appendParam('z', conf.Amplify(enemy.z), 'i')
		self.appendParam('hp', enemy.hp, 'i')

class MsgSCEMoveto(SimpleHeader):
	def __init__ (self, enemy):
		super (MsgSCEMoveto, self).__init__ (conf.MSG_SC_EMOVETO)
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('x', conf.Amplify(enemy.x), 'i')
		self.appendParam('z', conf.Amplify(enemy.z), 'i')

class MsgSCEnemyArrive(SimpleHeader):
	def __init__ (self, enemy, num):
		super (MsgSCEnemyArrive, self).__init__ (conf.MSG_SC_ENEMYARRIVE)
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('num', num, 'i')

class MsgSCEnemyAttack(SimpleHeader):
	def __init__ (self, enemy, player):
		super (MsgSCEnemyAttack, self).__init__ (conf.MSG_SC_ENEMYATTACK)
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('x', conf.Amplify(player.x), 'i')
		self.appendParam('z', conf.Amplify(player.z), 'i')

class MsgSCAttacked(SimpleHeader):
	def __init__ (self, hid, player):
		super (MsgSCAttacked, self).__init__ (conf.MSG_SC_ATTACKED)
		self.appendParam('hid', hid, 'i')
		self.appendParam('hp', player.hp, 'i')

class MsgCSAimed(SimpleHeader):
	def __init__ (self, eid = -1):
		super (MsgCSAimed, self).__init__ (conf.MSG_CS_AIMED)
		self.appendParam('eid', eid, 'i')
		

class MsgSCAimed(SimpleHeader):
	def __init__ (self, enemy):
		super (MsgSCAimed, self).__init__ (conf.MSG_SC_AIMED)
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('hp', enemy.hp, 'i')

class MsgCSAimedLeft(SimpleHeader):
	def __init__ (self, eid = -1, x = 0, y = 0, z = 0):
		super (MsgCSAimedLeft, self).__init__ (conf.MSG_CS_AIMEDLEFT)
		self.appendParam('eid', eid, 'i')
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgSCAimedLeft(SimpleHeader):
	def __init__ (self, enemy, x, y, z):
		super (MsgSCAimedLeft, self).__init__ (conf.MSG_SC_AIMEDLEFT)
		self.appendParam('eid', enemy.eid, 'i')
		self.appendParam('hp', enemy.hp, 'i')
		self.appendParam('x', x, 'i')
		self.appendParam('y', y, 'i')
		self.appendParam('z', z, 'i')

class MsgSCGameOver(SimpleHeader):
	def __init__(self, uid ):
		super (MsgSCGameOver, self).__init__(conf.MSG_SC_GAMEOVER)
		self.appendParam('uid', uid, 'i')

class MsgSCGameWin(SimpleHeader):
	def __init__(self, uid ):
		super (MsgSCGameWin, self).__init__(conf.MSG_SC_GAMEWIN)
		self.appendParam('uid', uid, 'i')

class MsgSCMoney(SimpleHeader):
	def __init__(self, player ):
		super (MsgSCMoney, self).__init__(conf.MSG_SC_MONEY)
		self.appendParam('hid', player.hid, 'i')
		self.appendParam('money', player.money, 'i')
		self.appendParam('nextExp', player.nextExp, 'i')
		self.appendParam('exp', player.exp, 'i')
		self.appendParam('lv', player.lv, 'i')

class MsgSCCountDown(SimpleHeader):
	def __init__(self, hid, interTime ):
		super (MsgSCCountDown, self).__init__(conf.MSG_SC_COUNTDOWN)
		self.appendParam('hid', hid, 'i')
		self.appendParam('interTime', interTime, 'i')

class MsgCSTrapBuy(SimpleHeader):
	def __init__ (self, ttype = -1):
		super (MsgCSTrapBuy, self).__init__ (conf.MSG_CS_TRAPBUY)
		self.appendParam('ttype', ttype, 'i')

class MsgSCTrapBuy(SimpleHeader):
	def __init__ (self, player):
		super (MsgSCTrapBuy, self).__init__ (conf.MSG_SC_TRAPBUY)
		self.appendParam('hid', player.hid, 'i')
		self.appendParam('money', player.money, 'i')
		self.appendParam('fire', player.fire, 'i')
		self.appendParam('needle', player.needle, 'i')

class MsgCSTrapCreate(SimpleHeader):
	def __init__ (self, ttype = -1):
		super (MsgCSTrapCreate, self).__init__ (conf.MSG_CS_TRAPCREATE)
		self.appendParam('ttype', ttype, 'i')

class MsgSCTrapCreate(SimpleHeader):
	def __init__ (self, player, trap):
		super (MsgSCTrapCreate, self).__init__ (conf.MSG_SC_TRAPCREATE)
		self.appendParam('hid', player.hid, 'i')
		self.appendParam('ttype', trap.ttype, 'i')
		self.appendParam('damage', trap.damage, 'i')
		self.appendParam('slowdown', conf.Amplify(trap.slowdown), 'i')
		self.appendParam('fire', player.fire, 'i')
		self.appendParam('needle', player.needle, 'i')

class MsgCSTrapAttack(SimpleHeader):
	def __init__ (self, eid = -1, damage = 1, slowdown = 1):
		super (MsgCSTrapAttack, self).__init__ (conf.MSG_CS_TRAPATTACK)
		self.appendParam('eid', eid, 'i')
		self.appendParam('damage', damage, 'i')
		self.appendParam('slowdown', slowdown, 'i')

class MsgSCTrapAttack(SimpleHeader):
	def __init__ (self, en):
		super (MsgSCTrapAttack, self).__init__ (conf.MSG_SC_TRAPATTACK)
		self.appendParam('eid', en.eid, 'i')
		self.appendParam('hp', en.hp, 'i')

		
		