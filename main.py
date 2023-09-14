import listen
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv('config.env')
    host = os.getenv('HOST_SOCKET')
    port = int(os.getenv('PORT_SOCKET'))
    listen.MyServer(host, port).server_program()
