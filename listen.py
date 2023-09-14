import socket
import classes


class MyServer:
	def __init__(self, host, port):  # create socket
		self.server_socket = socket.socket()
		self.server_socket.settimeout(300.0)
		self.server_socket.bind((host, port))
		self.server_socket.listen()
		print('Server running!')

	def server_program(self):
		while True:
			conn = None
			address = None
			try:
				conn, address = self.server_socket.accept()
				print("Connection from: " + str(address))
				conn.settimeout(300.0)
				while True:
					data = conn.recv(1024).decode()  # get command
					if data.lower() == 'remain_all':  # need get all remains
						data = classes.remains()

					elif data.lower() == 'list':  # need update material names
						data = classes.get_list_material()

					elif data.lower() == 'bye':  # closing client program
						print('Client ' + str(address) + ' disconnected\n')
						break

					elif data:  # create new object for actions with database
						print("Command: " + str(data))
						material_list = str(data).split(',')
						name, lot, action = material_list
						data = classes.Actions(name, lot, action).run_method()
					conn.send(data.encode())

			except socket.timeout:  # if there are no commands from the client
				if conn is not None:
					conn.close()
					print(f'Timeout. Client {str(address)} disconnected\n')

			except OSError:
				if conn is not None:
					conn.close()
					print('OSError. Client disconnected\n')
