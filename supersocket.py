import socket

END = "\x00"


class SuperSocket:

	def __init__(self, sock):
		self.sock = sock
		#self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.inBuf = ""
		self.isAlive = True

	def send(self, msg):
		try:
			newmsg = msg + END
			self.sock.send(bytes(newmsg, 'UTF-8'))
		except Exception as e:
			print('Exception in supersock while sending:', e)
			self.isAlive = False
			return None

	def recv(self, chsize=1024):
		try:
			while not END in self.inBuf and self.isAlive:
				recvd = self.sock.recv(chsize)
				recvd = recvd.decode('UTF-8')
				#print('chunk:', recvd)
				if not recvd:
					raise Exception()
				self.inBuf += recvd
		except OSError:
			print('Connection Closed')
			return None
		except Exception as e:
			print(type(e))
			print('exception while Recieving', str(e))
			self.isAlive = False
			return None
		msg, _, self.inBuf = self.inBuf.partition("\0")
		return msg

	def close(self):
		self.isAlive = False
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
