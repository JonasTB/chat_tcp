import threading
import socket

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
    
def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('utf-8').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('utf-8')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('utf-8'))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} deixou o chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break
        
def receive():
    while True:
        client, address = server.accept()
        print(f'Connection is established: {str(address)}')
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
            
        if nickname+'\n' in bans:
            client.send('BAN'.encode('utf-8'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASS'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8')
            
            if password != 'adminpass':
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue
    
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Connected with name {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected in the server!').encode('utf-8')
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by admin!'.encode('utf-8'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by admin!'.encode('utf-8'))

if __name__ == "__main__":
    print('Server is listen...')
    receive()