import socket
import select
import errno
import sys

'''Declaring Header length'''
HEADER_LENGTH = 10

'''Host, port and username declaration'''
Host = "127.0.0.1"
PORT = 9999
my_username = input("Username: ")

'''The socket is created based on TCP model'''
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, PORT))

'''In order to retain the clients the setblocking is set as false'''
client_socket.setblocking(False)

'''The length of username and username is encoded to send to the server'''
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


'''The continuous running loop'''
while True:
    message = input(f'{my_username} > ')

    '''This part send the data from the client to the server '''
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        '''This part receives the message and prints it'''
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

    
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')


        '''some error cases are handled here   '''            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()


