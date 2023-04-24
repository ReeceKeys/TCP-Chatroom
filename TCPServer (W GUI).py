import socket 
import threading
import cv2
import time
import glob, os
from datetime import datetime

date = datetime.now()
date = str(date)
date = date[0: (len(date) - 10)]

HOST = 'localhost'
PORT = 18000




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
addresses = []
names = []
rooms = [[],[],[],[]]
room_add = [[],[],[],[]]
room_count = [0, 0, 0, 0]
name = ''
global addr
global history
history = ['','','','']
names_in_room = [[],[],[],[]]


class pw:
    def __init__(self, creator, pword, room_number):
        self.creator = creator
        self.pword = pword
        self.room_number = room_number

def name_checker(name):
    for i in range(0, len(names)):
          if name == names[i]:
               return False
    
    return True

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def closed_send(message, room_sel):   
    for client in rooms[room_sel]:
        client.send(message.encode())





def receive():
    while True:
        global addr
        global name
        client, addr = server.accept()
        conn_flag = False
        while conn_flag == False:
            name_req = client.recv(1024).decode()  #receive name
            print("Client [" + str(addr) + "] is trying to use [" + name_req + "]")
            check_name = name_checker(name_req)
            if check_name == False:
                client.send("name_invalid".encode())
                print("[Username in use]")
            else: 
                client.send("name_valid".encode())
                name = name_req
                clients.append(client)
                addresses.append(addr)
                names.append(name)
                conn_flag = True
                
                print(f"Name of the client " + str(addr) + " is " + name)
                    
                    
        
        print(f"Connected with {str(addr)}")
        print("[Active Users:] = [" + str(names) + "]")
        main_menu(client)
        
def main_menu(client):
            global history
            client_report = ''
            client_report += '\n'
            user_count = 0
            print("Accessing main menu...")
            global name
            option = client.recv(1024).decode()
            if option == '0':
                    print("Menu_Entry: 0")
                    for i in range(0, len(clients)):
                         client_report += names[i]
                         client_report += " - " 
                         client_report += str(addresses[i])
                         client_report += "\n\n"
                         user_count += 1
                    client.send('server_report'.encode())
                    client.send(client_report.encode())
                    time.sleep(1)
                    client.send(str(user_count).encode())
            if option == '1':  #select room function
                    print("Menu_Entry: 1")
                    room_sel = client.recv(1024).decode()
                    room_sel = int(room_sel)
                    room_key = int(room_sel) - 1
                    if (room_count[room_key] == 3):
                        client.send('too many'.encode())
                        index = clients.index(client)
                        print("[Removing:] ", addr[index], "(", names[index], ")")
                        clients.remove(client)
                        name_remove = names[index]
                        names.remove(name_remove)
                        print('-'*20)
                        print("Current Users: ", str(room_add))
                        print('-'*20)
                        client.close()
                                            
                    else:
                        client.send('enough space'.encode())
                        rooms[room_key].append(client)
                        room_add[room_key].append(addr)
                        room_count[room_key] += 1
                        names_in_room[room_key].append(name)
                        welcome = ('(' + date + ") Welcome to room " + str(room_sel) + ", " + name + "! Users: " + str(names_in_room[room_key]) +"\n")
                        closed_send(welcome, room_key)
                        print('-'*20)
                        print("Rooms: ", room_add)
                        print('-'*20)
                        history[room_key] += welcome
                        time.sleep(1)
                        client.send('history'.encode())
                        time.sleep(1)
                        client.send(history[room_key].encode())


                        #client.send("connected".encode())
                        thread = threading.Thread(target = handle, args = (client,room_key))
                        thread.start() 
                    
                    
                    

            elif option == '2':  #select name function
                    print("Menu_Entry: 2")
                    conn_flag = False
                    while conn_flag == False:
                        name_req = client.recv(1024).decode()  #receive name
                        print("Client [" + str(addr) + "] is trying to use [" + name_req + "]")
                        check_name = name_checker(name_req)
                        if check_name == False:
                            client.send("name_invalid".encode())
                            print("[Username in use]")
                        else: 
                            client.send("name_valid".encode())
                            index = clients.index(client)
                            names.remove(name)
                            name = name_req
                            clients.append(client)
                            addresses.append(addr)
                            names.append(name)
                            conn_flag = True
                            
                            print(f"Name of the client " + str(addr) + " is " + name)
                        main_menu(client)
        
                


def handle(client, room_sel):
    while True:
        try:
            global history 
            msg = client.recv(1024).decode()  #fetch msg
            print("Handling message: " + msg)  #fetch name of person sending msg
            if "/a" in msg:
                print(name, " is accessing txt file. ")
                client.send('txt'.encode())
                txt_name = client.recv(1024).decode()
                print(txt_name)
                if txt_name != '0':
                    if txt_name[len(txt_name) - 4:] != '.txt':
                        txt_name += '.txt'
                    with open(txt_name) as f:
                        lines = f.readlines()
                    print(lines)
                    index = clients.index(client)
                    name_txt = names[index]
                    file_mess = '(' + date + ') ' + name_txt + ': ' + str(lines)
                    history[room_sel] += file_mess + '\n'
                    closed_send(file_mess, room_sel)  
                    f.close()
            elif '/i' in msg:
                 client.send('png'.encode())
                 png_name = client.recv(1024).decode()
                 print(png_name)
                 if png_name != '0':
                      if png_name[len(png_name) - 4:] != '.png':
                            png_name += '.png'
                      png = open(png_name, 'wb')
                      image_chunk = client.recv(1024).decode()
                      while image_chunk:
                           png.write(image_chunk)
                           image_chunk = client.recv(1024).decode()
                      closed_send(png, room_sel)
                      png.close()
            else:
                history[room_sel] += msg
                print("Sending message ", msg)
                closed_send(msg, room_sel)  #broadcast msg to room
                
        except:
            index = clients.index(client)
            name_remove = names[index]
            names.remove(name_remove)
            names_in_room[room_sel].remove(name)
            rooms[room_sel].remove(client)
            closed_send(("(" + date + ") [" + name + " left.] Current Users: [" + str(names_in_room[room_sel])+ ']\n'), room_sel)
            break
    
    print("[Removing:] ", addr[index], "(", names[index], ")")
    clients.remove(client)
    addr_remove = room_add[room_sel][index]
    room_add[room_sel].remove(addr_remove)
    
    print('-'*20)
    print("Current Users: ", str(room_add))
    print('-'*20)
    client.close()



print('-' * 30, '\n')
print("Server running\n")
print('-' * 30)


receive()

