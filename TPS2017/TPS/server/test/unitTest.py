# -*- coding: GBK -*-

import unittest
import sys
import cPickle
import time

sys.path.append('..')
sys.path.append('../common')
sys.path.append('../network')
sys.path.append('../common_server')

import conf
from events import MsgCSLogin, MsgCSMoveto
from dispatcher import Service, Dispatcher
from netStream import NetStream
from simpleHost import SimpleHost
from timer import TimerManager

class TestService(Service):
	def __init__(self, sid = 0):
		super(TestService, self).__init__(sid)
		commands = {
			10 : self.f,
			20 : self.f,
		}
		self.registers(commands)
	
	def f(self, msg, owner):
		return owner

class MsgService(object):
	pass

class ServerTest(unittest.TestCase):
	def setUp(self):
		self._head1 = MsgCSLogin('test', '163')
		self._head2 = MsgCSMoveto(3, 5)

		self._dispatcher = Dispatcher()
		self._dispatcher.register(100, TestService())

		self.count = 0

	def tearDown(self):
		self._head1 = None
		self._head2 = None

		self._dispatcher = None

		self.count = 0

	def addCount(self):
		self.count += 1

	def test_Parser(self):
		# test header
		data = self._head1.marshal()
		head = MsgCSLogin().unmarshal(data)
		self.assertEqual(self._head1.name, head.name)
		self.assertEqual(self._head1.password, head.password)
		print head.name
		print head.password

		data = self._head2.marshal()
		head = MsgCSMoveto().unmarshal(data)
		self.assertEqual(self._head2.x, head.x)
		self.assertEqual(self._head2.y, head.y)
		print head.x
		print head.y

		# test dispatcher
		msg = MsgService()
		msg.sid = 100
		msg.cid = 10
		self.assertEqual(self._dispatcher.dispatch(msg, 'client1'), 'client1')
		print self._dispatcher.dispatch(msg, 'client1')
		msg.cid = 20
		self.assertEqual(self._dispatcher.dispatch(msg, 'client2'), 'client2')

		# test network
		host = SimpleHost()
		host.startup(2000)
		sock = NetStream()
		last = time.time()
		sock.connect('127.0.0.1', 2000)

		stat = 0
		last = time.time()
		sock.nodelay(1)

		while 1:
			time.sleep(0.1)
			host.process()
			sock.process()
			
			if stat == 0:
				if sock.status() == conf.NET_STATE_ESTABLISHED:
					stat = 1
					data = cPickle.dumps((stat, 'Hello, world !!'), -1)
					sock.send(data)
					last = time.time()
			elif stat == 1:
				if time.time() - last >= 2.0:
					stat = 2
					data = cPickle.dumps((stat, 'exit'), -1)
					sock.send(data)
		
			event, wparam, data = host.read()
			if event < 0:
				continue
			
			if event == conf.NET_CONNECTION_DATA:
				client_stat, message = cPickle.loads(data)
				host.sendClient(wparam, 'RE: ' + message)
				print wparam
				print message
				if client_stat == 1:
					self.assertEqual(message, 'Hello, world !!')
				elif client_stat == 2:
					self.assertEqual(message, 'exit')
					host.closeClient(wparam)

					host.shutdown()
					break

		# test timer
		TimerManager.addRepeatNumTimer(0.15, self.addCount, 7)
		last = time.time()
		while 1:
			time.sleep(0.01)
			TimerManager.scheduler()
			print self.count
			if time.time() - last > 3.0:
				break

		#self.assertEqual(self.count, 8)

		return

if __name__ == '__main__':
	unittest.main()
