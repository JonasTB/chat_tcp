import threading
import socket

host = '127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break
        
def receive():
    while True:
        client, address = server.accept()
        print(f'Connect on address: {str(address)}')
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
    
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Connected with {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connect on server!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by admin!'.encode('ascii'))
        
print('Servidor est?? no ar...')
receive()