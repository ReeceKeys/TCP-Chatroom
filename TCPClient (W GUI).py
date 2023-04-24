import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import cv2
import time
from datetime import datetime

date = datetime.now()
date = str(date)
date = date[0: (len(date) - 10)]


HOST = 'localhost'
PORT = 18000
global count
global clients
global names
global pass_bank
pass_bank = ["success"]
global name_flag
name_flag = False



class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create socket
        self.sock.connect((host, port))  #connect!
        self.gui_done = False  #flag
        self.running = True  #flag
        self.main_menu_done = False
        self.select_room_done = False
        global room 
        room = -1
        
        gui_thread = threading.Thread(target = self.name_sel)  #create thread for client
        receive_thread = threading.Thread(target= self.receive) #thread for client to recieve data 

        gui_thread.start()  #start gui thread
        receive_thread.start()  #start thread
        
        
        
        


    def name_sel(self):
        global name_flag
        name_flag = False
        print("[Sending name for verification...]")
        while name_flag == False:
            msg_name = tkinter.Tk()  #create window
            msg_name.withdraw()  #withdraw window box
            
            self.name = simpledialog.askstring("name","[ENTER NAME]", parent  = msg_name)  #text box open
            self.sock.send(self.name.encode())  #send name
            time.sleep(4)

        self.main_menu()
            
            
                
                
                 
        
    
    
    def server_report(self):
        self.win = tkinter.Tk()
        self.win.title("Server Report")
        self.win.configure(bg = '#4C4E52')

        self.clients_title = tkinter.Label(self.win, text = ("SERVER REPORT"), bg = '#4C4E52', fg = '#F2F79E')
        self.clients_title.config(font = ("Helvetica 15 underline"))
        self.clients_title.pack(padx = 20, pady = 20)

        self.clients_title = tkinter.Label(self.win, text = (str(user_count) + " Current Users: "), bg = '#4C4E52', fg = '#A8D4AD')
        self.clients_title.config(font = ("Helvetica 14 italic"))
        self.clients_title.pack(padx = 20, pady = (20, 5))
        
        self.clients_label = tkinter.Label(self.win, text = str(client_report), bg = "white")
        self.clients_label.config(font = ("Helvetica 12"))
        self.clients_label.pack(padx = 20, pady = 5)

        self.win.protocol("WM_DELETE_WINDOW", self.stop) 
        self.win.mainloop()
    



    def main_menu(self):  #main_menu
        self.win = tkinter.Tk()
        self.win.title("ChatterBox")
        self.win.configure(bg='#4C4E52')

        self.menu_label = tkinter.Label(self.win, text = ("Welcome to ChatterBox!"), bg = "#4C4E52", fg = '#F2F79E')
        self.menu_label.config(font = ("Helvetica 15 underline"))
        self.menu_label.pack(padx = 20, pady = 5)

        self.name_label = tkinter.Label(self.win, text = ("Logged in as " + self.name), bg = "#4C4E52", fg = '#F2F79E')
        self.name_label.config(font = ("Helvetica 12"))
        self.name_label.pack(padx = 20, pady = 5)

        self.menu_label = tkinter.Label(self.win, text = ("(Version: 1.0)"), bg = "#4C4E52", fg = '#F2F79E')
        self.menu_label.config(font = ("Helvetica 10 italic"))
        self.menu_label.pack(padx = 20, pady = (5,50))

        self.chatroom_button = tkinter.Button(self.win, text = "Server Report", command = self.close_open_0, fg = 'black', bg = "#A8D4AD")
        self.chatroom_button.config(font = ("Birch", 16))
        self.chatroom_button.pack(padx = 20, pady = 10)

        self.chatroom_button = tkinter.Button(self.win, text = "Join Chatroom", command = self.close_open_1, fg = 'black', bg = "#A8D4AD")
        self.chatroom_button.config(font = ("Birch", 16))
        self.chatroom_button.pack(padx = 20, pady = 10)

        self.name_sel_button = tkinter.Button(self.win, text = "Rename", command = self.close_open_2, fg = 'black', bg = "#92B9BD")
        self.name_sel_button.config(font = ("Birch", 12))
        self.name_sel_button.pack(padx = 20, pady = 10)

        self.password_button = tkinter.Button(self.win, text = "Password Manager (coming soon!)", fg = 'black', bg = "#92B9BD")  #Button for Send function 
        self.password_button.config(font = ("Birch", 12))
        self.password_button.pack(padx = 20, pady = 10)

        self.exit_button = tkinter.Button(self.win, text = "Exit", command = self.stop, fg = 'black', bg = "#92B9BD")
        self.exit_button.config(font = ("Birch", 12))
        self.exit_button.pack(padx = 20, pady = 10)

        self.main_menu_done = True  #close window
        self.win.protocol("WM_DELETE_WINDOW", self.stop) 
        self.win.mainloop()
    
    
    def select_room(self): 
        self.win = tkinter.Tk()
        self.win.configure(bg = '#4C4E52')

        self.room_sel = tkinter.Label(self.win, text = ("Select A Room To Join!"), bg = '#4C4E52', fg = '#F2F79E')
        self.room_sel.config(font = ('Helvetica 15 underline'))
        self.room_sel.pack(padx = 20, pady = 5)

        self.room_1_button = tkinter.Button(self.win, text = "Room 1", command = self.join_room_1, fg = 'black', bg = "#A8D4AD")
        self.room_1_button.config(font = ("Noto Sans", 12))
        self.room_1_button.pack(padx = 20, pady = 5, side = "left")


        self.room_2_button = tkinter.Button(self.win, text = "Room 2", command = self.join_room_2, fg = 'black', bg = "#92B9BD")  #Button for Send function 
        self.room_2_button.config(font = ("Noto Sans", 12))
        self.room_2_button.pack(padx = 20, pady = 5, side = "left")


        self.room_3_button = tkinter.Button(self.win, text = "Room 3", command = self.join_room_3, fg = 'black', bg = "#A8D4AD")  #Button for Send function 
        self.room_3_button.config(font = ("Noto Sans", 12))
        self.room_3_button.pack(padx = 20, pady = 5, side = "left")

        self.room_4_button = tkinter.Button(self.win, text = "Room 4", command = self.join_room_4, fg = 'black', bg = "#92B9BD")  #Button for Send function 
        self.room_4_button.config(font = ("Noto Sans", 12))
        self.room_4_button.pack(padx = 20, pady = 5, side = "left")

        self.select_room_done = True  #close window
        self.win.protocol("WM_DELETE_WINDOW", self.stop) 
        self.win.mainloop()
    


       


    def gui_loop(self, room):  #chatroom - need to implement room_number
        self.win = tkinter.Tk()
        self.win.configure(bg="#4C4E52")  #background color
    

        self.chat_label = tkinter.Label(self.win, text=("ChatterBox"), bg="#4C4E52", fg = '#F2F79E')  #use same as bg color
        self.chat_label.config(font = ('Helvetica 15 underline'))
        self.chat_label.pack(padx = 20, pady = 5)
        
        self.chat_label = tkinter.Label(self.win, text=("(Room " + str(room) + ")"), bg="#4C4E52", fg = '#92B9BD')  #use same as bg color
        self.chat_label.config(font = ('Helvetica 12'))
        self.chat_label.pack(padx = 20, pady = 5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg = "#E6E6E6")  #text history box
        self.text_area.pack(padx = 20, pady = 5)
        self.text_area.config(state = 'disabled')  #turn off editing text history

        self.chat_label = tkinter.Label(self.win, text="Chat", bg="#4C4E52", fg = '#92B9BD')  #use same as bg color
        self.chat_label.config(font = ("Eccentric Std", 12))
        self.chat_label.pack(padx = 20, pady = 5)

        self.input_area = tkinter.Text(self.win, height = 3, bg = "#E6E6E6")
        self.input_area.pack(padx = 20, pady = 5)

        self.send_button = tkinter.Button(self.win, text = "Send", command = self.write, fg = 'black', bg = '#A8D4AD')  #Button for Send function 
        self.send_button.config(font = ("Arial", 12))
        self.send_button.pack(padx = 20, pady = 5)

        

        self.exit_button = tkinter.Button(self.win, text = "Exit", command = self.stop_btn, fg = 'black', bg = '#A8D4AD')  #Button for Send function 
        self.exit_button.config(font = ("Arial", 12))
        self.exit_button.pack(padx = 20, pady = 5)

        
        self.gui_done = True  #allow messages to show
        self.win.protocol("WM_DELETE_WINDOW", self.stop)  #call stop function to terminate program

        self.win.mainloop()


    

    def write(self):
        
        message = f"({date}) {self.name}: {self.input_area.get('1.0', 'end')}"
        print("Sending message: ", message)
        self.sock.send(message.encode())
        self.input_area.delete('1.0', 'end')

    def stop_btn(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def stop(self):
        self.running = False
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                global join_flag
                message = self.sock.recv(1024).decode()
                if message == 'name':
                    self.sock.send(self.name.encode())
                elif message == 'txt':
                    msg = tkinter.Tk()  #text box to enter txt file name
                    msg.withdraw()  #withdraw text box
                    self.txt_name = simpledialog.askstring("txt","[ENTER .TXT FILE NAME]", parent  = msg)  #text box open
                    self.sock.send(self.txt_name.encode())
                    time.sleep(1)
                    message = self.sock.recv(1024).decode()  #print txt file
                    self.text_area.config(state = 'normal')
                    self.text_area.insert('end', message + '\n')
                    self.text_area.yview('end')
                    self.text_area.config(state = 'disabled')
                elif message == 'png':
                    msg = tkinter.Tk()  #text box to enter img file name
                    msg.withdraw()  #withdraw text box
                    self.png_name = simpledialog.askstring("png","[ENTER .PNG FILE NAME]", parent  = msg)  #text box open
                    self.sock.send(self.png_name.encode())
                    image = self.sock.recv(1024).decode()
                    
                    self.text_area.config(state = 'normal')
                    self.text_area.insert('end', image)
                    self.text_area.yview('end')
                    self.text_area.config(state = 'disabled')
                elif message == 'exit':
                    self.running = False
                    print("Exiting room")
                    self.sock.close()
                    break
                elif message == 'name_valid':
                    print("Requested name is valid!")
                    global name_flag
                    name_flag = True
                elif message == 'name_invalid':
                    print("Requested name is in use. Enter a new one.")
                    name_flag = False
                elif message == 'server_report':
                    global client_report
                    global user_count
                    print("Accessing Server Info...")
                    client_report = self.sock.recv(1024).decode()
                    time.sleep(1)
                    user_count = self.sock.recv(1024).decode()
                elif message == 'history':
                    time.sleep(1)
                    global prev_mess
                    prev_mess = self.sock.recv(1024).decode()
                    self.text_area.config(state = 'normal')
                    self.text_area.insert('end', prev_mess)
                    self.text_area.yview('end')
                    self.text_area.config(state = 'disabled')
                elif message == 'enough space':
                    join_flag = 1
                elif message == 'too many':
                    join_flag = 0
                    
                else:
                    if self.gui_done:  #print normal message
                        self.text_area.config(state = 'normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')
            
            except ConnectionAbortedError:
                break
            except:
                print("[Error. Closing Down]")
                self.sock.close()
                break


    def close_open_0(self):
        self.win.destroy()
        self.sock.send('0'.encode())
        time.sleep(5)
        self.server_report()


    def cannot_join(self):
        no_join = tkinter.Tk()  #create window
        no_join.configure(bg="#4C4E52")

        no_join_label = tkinter.Label(no_join, text=("Too many users!"), bg="#4C4E52", fg = '#F2F79E')  #use same as bg color
        no_join_label.config(font = ('Helvetica 15 underline'))
        no_join_label.pack(padx = 20, pady = 5)

        no_join.protocol("WM_DELETE_WINDOW", self.stop)  #call stop function to terminate program

        no_join.mainloop()


    def close_open_1(self):  #for closing windows and opening new ones 
        self.sock.send('1'.encode())  #send option
        self.win.destroy()
        self.select_room()
            
    def close_open_2(self):
        self.sock.send('2'.encode())
        self.win.destroy()
        self.name_sel()


    


    def join_room_1(self):  #join room functions
        global join_flag
        self.win.destroy()
        self.sock.send('1'.encode())
        time.sleep(1)
        if join_flag == 1:
            print("Entering Room : 1")  #send room number
            self.gui_loop(1)
        else:
            self.cannot_join()
        global room 
        room = 1

           
        
        
    
    def join_room_2(self):
        global join_flag
        self.win.destroy()
        self.sock.send('2'.encode())
        time.sleep(1)
        if join_flag == 1:
            print("Entering Room : 2")  #send room number
            self.gui_loop(2)
        else:
            self.cannot_join()
        global room 
        room = 2

    def join_room_3(self):
        global join_flag
        self.win.destroy()
        self.sock.send('3'.encode())
        time.sleep(1)
        if join_flag == 1:
            print("Entering Room : 3")  #send room number
            self.gui_loop(3)
        else:
            self.cannot_join()
        global room 
        room = 3

    def join_room_4(self):
        global join_flag
        self.win.destroy()
        self.sock.send('4'.encode())
        time.sleep(1)
        if join_flag == 1:
            print("Entering Room : 4")  #send room number
            self.gui_loop(4)
        else:
            self.cannot_join()
        global room 
        room = 4


    def close_open_room1(self):
        self.win.destroy()
        self.join_room_1()
    def close_open_room2(self):
        self.win.destroy()
        self.join_room_2()
    def close_open_room3(self):
        self.win.destroy()
        self.join_room_3()
    def close_open_room4(self):
        self.win.destroy()
        self.join_room_4()



client = Client(HOST,PORT)

#main menu -> name select -> room select -> exit
#implement commands (a, i , 0)