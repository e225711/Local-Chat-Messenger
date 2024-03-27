import socket
import os
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/tmp/socket_file'

fake = Faker()


try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)

sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        while True:
            data = connection.recv(16)
            data_str =  data.decode('utf-8')
            print('Received ' + data_str)

            if data_str == 'name':
                response = 'Name: ' + fake.name()
            elif data_str == 'address':
                response = 'Address: ' + fake.address()
            elif data_str == 'text':
                response = 'Text: ' + fake.text()

            if data:
                connection.sendall(response.encode())

            else:
                print('no data from', client_address)
                break

    finally:
        connection.close()
