
# --------------------------------------------------------------------------------------------------------------------------------------- #

import threading
import socket
nickname = input('Choose an nickname >>> ')

if nickname == 'admin':
    password = input("Enter your pass for admin: ")
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))

stop_thread = False

def client_receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "nickname?":
                client.send(nickname.encode('utf-8'))
                next_message = client.recv(1024).decode('utf-8')
                
                if next_message == 'PASS':
                    client.send(password.encode('utf-8'))
                    
                    if client.recv(1024).decode('utf-8') == 'REFUSE':
                        print("Connection was refused! Wrong password")
                        stop_thread = True
                    
            else:
                print(message)
                
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        if stop_thread:
            break
        
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))
        
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('utf-8'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('utf-8'))
            else:
                print("Commands can only be executed by the admin")
        else:
            client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()