#CHATAPP
#FILE :  SERVER
#AUTHOR: SAGAR MISHRA

import socket
import threading
import time

host = socket.gethostbyname(socket.gethostname())
port = 9999
FORMAT= 'utf-8'

# STARTING SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("[STARTING] Server is starting...")
print("[BINDING]    Binding with   | " +str(port)+ " | IP: "+host+" | ADMIN")

# CLIENT LIST
clients = []
names = []

# BROADCASTING MESSAGE TO ALL CLIENTS
def broadcast(message):
    for client in clients:
        client.send(message)

def manage_client(client):
    while True:
        try:
            # BROADCAST
            message = client.recv(1024)
            broadcast(message)
            
        except:
            # CLOSE CONNECTION
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(("{} left!".format(name).center(177,' ')).encode(FORMAT))
            print(f"Active Connections: {threading.activeCount()-2}")
            names.remove(name)
            break

# RECIEVE MESSAGE
def receive():
    while True:

        # ACCEPT CLIENT
        client, address = server.accept()
        x,y=address

        # TAKING NAME
        client.send('NICK'.encode(FORMAT))
        name = client.recv(1024).decode(FORMAT)
        names.append(name.upper())
        clients.append(client)

        # PRINTING DETAILS        
        print(f"[CONNECTING] Connected with | {y} | IP: {x} | {name}")
        
        broadcast((f"  {time.ctime()}  ".center(144,'-') + "\n").encode(FORMAT))
        
        broadcast(("{} joined!".format(name).center(177,' ') + "\n").encode(FORMAT))
        
         
        # STARTING CLIENT THREAD
        thread = threading.Thread(target=manage_client, args=(client,))
        thread.start()
        print(f"Active Connections: {threading.activeCount()-1}")
        
receive()
