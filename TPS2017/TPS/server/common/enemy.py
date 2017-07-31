# -*- coding: GBK -*-
import math
import time
import conf
ENEMY_LEFT = 0
ENEMY_RIGHT = 1
ENEMY_BEAR = 1
ENEMY_BUNNY = 2
ENEMY_ELEPHANT = 3
class Enemy(object):
	ID = 0
	def __init__(self, direction):
		super(Enemy, self).__init__()
		self.eid = Enemy.ID + 1
		self.hp = 100
		self.scoreValue = 20
		Enemy.ID = Enemy.ID + 1
		if direction == ENEMY_LEFT:
			self.x, self.z = 4.3, 23.5
		else:
			self.x, self.z = 7.5, 19.9
		self.closeDistance = 1.5
		self.nearDistance = 5
		self.currentTime = time.time()
		self.isSlowdown = False
		print "Create success"

	def lvUp(self, lv):
		self.damage += lv*5
		self.hp	+= lv*10
		self.scoreValue += lv*5

	def isNear(self, player):
		if player.isDead:
			return False
		if self.distance(self.x, self.z, player.x, player.z) < self.nearDistance:
			return True
		return False

	def isClose(self, player):
		if player.isDead:
			return False
		now = time.time()
		if now - self.currentTime <= self.timeBetweenAttack: #Between Attack Time 
			return False
		if self.distance(self.x, self.z, player.x, player.z) < self.closeDistance:#Attack
			player.hp -= self.damage
			if player.hp <= 0:
				player.isDead = True
			self.currentTime = now
			return True
		return False

	def distance(self, x1, z1, x2, z2):
		#print [x1,z1,x2,z2]
		return math.sqrt(math.pow(x1 - x2, 2) + math.pow(z1 - z2, 2))

	def attacked(self, player, damage):
		if self.hp > 0:
			self.lastHid = player.hid
			self.hp -= damage

	def getMoney(self, player):
		pass

	def trapAttack(self, trap, hid):
		if self.hp > 0:
			self.lastHid = hid
			self.hp -= trap.damage
			if not self.isSlowdown:
				print trap.slowdown
				print conf.DeAmplify(trap.slowdown)
				self.speed = self.speed * conf.DeAmplify(trap.slowdown)
				self.isSlowdown = True


class Bear(Enemy):
	def __init__(self, direction):
		super(Bear, self).__init__(direction)
		self.etype = 1
		self.speed = 2.5
		self.damage = 10
		self.scoreValue = 30
		self.timeBetweenAttack = 1
		self.closeDistance = 5
		self.nearDistance = 8

	def getMoney(self, player):
		player.money += self.scoreValue
		player.exp += self.scoreValue
		player.lvUp()



class Bunny(Enemy):
	def __init__(self, direction):
		super(Bunny, self).__init__(direction)
		self.etype = 2
		self.speed = 2.5
		self.damage = 10
		self.scoreValue = 20
		self.timeBetweenAttack = 1

	def getMoney(self, player):
		player.money += self.scoreValue
		player.exp += self.scoreValue
		player.lvUp()

class Ellephant(Enemy):
	def __init__(self, direction):
		super(Ellephant, self).__init__(direction)
		self.etype = 3
		self.speed = 2
		self.damage = 30
		self.hp = 300
		self.scoreValue = 50
		self.timeBetweenAttack = 0.5

	def getMoney(self, player):
		player.money += self.scoreValue
		player.exp += self.scoreValue
		player.lvUp()



