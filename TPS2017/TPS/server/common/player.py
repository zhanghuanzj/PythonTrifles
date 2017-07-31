# -*- coding: GBK -*-
import conf
class Player(object):
	FireMoney = 60
	NeedleMoney = 80
	def __init__(self, hid):
		super(Player, self).__init__()
		self.room = None
		self.hid = hid
		self.isOver = False

	def getDamage(self, fireType):
		if fireType == conf.FIRE_LEFT:
			return self.fireDamage
		else:
			return self.magicDamage

	def buyTrap(self, trap):
		if trap.ttype == conf.FIRE_TRAP:
			if self.money >= Player.FireMoney:
				self.money -= Player.FireMoney
				self.fire += 1
		else:
			if self.money >= Player.NeedleMoney:
				self.money -= Player.NeedleMoney
				self.needle += 1

	def getTrap(self, trap):#Trap damage and slowdown
		if trap.ttype == conf.FIRE_TRAP:
			if self.fire > 0:
				self.fire -= 1
				trap.damage = self.lv * 5 + 30
				trap.slowdown = 1
				return
		else:
			if self.needle > 0:
				self.needle -= 1
				trap.damage = self.lv * 3 + 20
				trap.slowdown = max(0.3, 0.8 - self.lv*0.03)
				return
		trap.damage = 0
		trap.slowdown = 1

	def lvUp(self):
		if self.exp >= self.nextExp:
			self.lv += 1
			self.exp -= self.nextExp
			self.nextExp = self.nextExp * 1.5
			self.maxhp += 30
			self.hp += 30