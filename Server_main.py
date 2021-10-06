import socket
import select

'''setting header length'''
HEADER_LENGTH = 10

'''Initializing the server on localhost witrh port number 9999'''
Host = "127.0.0.1"
PORT = 9999
'''for TCP connection'''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''To maintain the same addr '''
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

'''Binding and listening(waiting) for the message from the clients'''
server_socket.bind((Host, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}
print(f'Listening for connections on {Host}:{PORT}...')

'''if the message is received then decoding the message as it contain both message size and the message'''
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False    
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}


    except:
        return False 

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    '''checks and appends the new clients'''

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            '''prints the data of in the server '''
            user = clients[notified_socket]
            print(f'{user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            '''This sends data to the other clients'''  
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]           