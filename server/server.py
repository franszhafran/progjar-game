import socket
import time
import sys
import asyncore
import logging
import threading
import random
import queue
import json

rcv = ""

game = {
	"data": [],
	"player_data": [],
	"state": "roll",
	"player_data_queue": [queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()]
}
command_queue = queue.Queue()
game_lock = threading.Lock()

class ProcessTheClient(asyncore.dispatcher_with_send):
	def handle_read(self):
		global rcv
		data = self.recv(1024)
		if data:
			d = data.decode()
			rcv = rcv + d
			if rcv[-2:] == '\r\n':
				# end of command, proses string
				# logging.warning("data dari client: {}".format(rcv))
				hasil = self.proses(rcv.replace("\r\n", ""), self.ip)
				#hasil sudah dalam bentuk bytes
				hasil = hasil + "\r\n\r\n".encode()
				#agar bisa dioperasikan dengan string \r\n\r\n maka harus diencode dulu => bytes
				# logging.warning("balas ke  client: {}".format(hasil))
				self.send(hasil) #hasil sudah dalam bentuk bytes, kirimkan balik ke client
				rcv = ""
				self.close()

		#self.send('HTTP/1.1 200 OK \r\n\r\n'.encode())
			#self.send("{}" . format(httpserver.proses(d)))
		self.close()

	def proses(self, rcv, ip):
		global game_lock
		game_lock.acquire()
		global game
		print(rcv, ip)
		index = game["player_data"].index(ip)
		if rcv == "ask":
			data = []
			while not game["player_data_queue"][index].empty():
				data.append(game["player_data_queue"][index].get())
			res = json.dumps({"status": "OK", "player_number": int(index), "data": data})
		else:
			command_queue.put(rcv)
			res = json.dumps({"status": "OK", "data": ""})
		game_lock.release()
		return res.encode()

def game_loop():
	global dice
	global command_queue
	player_now = 0

	while True:
		game_lock.acquire()
		print(game["state"])
		if game["state"] == "roll":
			dice = random.randint(1, 6)
			print("appending atas {}".format("dice_{}_{}".format(player_now, dice)))
			game["data"].append({
				"ip": "server",
				"action": "dice_{}_{}".format(player_now, dice)
			})
			for i in range(4):
				game["player_data_queue"][i].put({
					"ip": "server",
					"action": "dice_{}_{}".format(player_now, dice)
				})
			player_now += 1
			if player_now == 2:
				player_now = 0
			game["state"] = "play"
		elif game["state"] == "play":
			game_lock.release()
			cmd = command_queue.get()
			game_lock.acquire()
			print("cmd", cmd)
			print("appending bawah {}".format("dice_{}_{}".format(player_now, dice)))
			game["data"].append({
				"action": cmd
			})
			for i in range(4):
				game["player_data_queue"][i].put({
					"action": cmd
				})
			game["state"] = "roll"
		game_lock.release()
		time.sleep(5)

class Server(asyncore.dispatcher):
	def __init__(self,portnumber):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('',portnumber))
		self.listen(5)
		logging.warning("running on port {}" . format(portnumber))

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			# logging.warning("connection from {}" . format(repr(addr)))
			game_lock.acquire()
			if addr[0] not in game["player_data"]:
				game["player_data"].append(addr[0])
			game_lock.release()
			handler = ProcessTheClient(sock)
			handler.ip = addr[0]

def main():
	t = threading.Thread(target=game_loop)
	t.start()
	portnumber=8888
	try:
		portnumber=int(sys.argv[1])
	except:
		pass
	svr = Server(portnumber)
	asyncore.loop()

if __name__=="__main__":
	main()

