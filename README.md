# TCP-Chatroom
Allows user to host and connect to a TCP chatroom throuigh multiple instances of Python. Run server first, then run client. 

TCP Chatroom (With GUI)

Project Description
Simple TCP chat room that utilizes multiple rooms and keeps track of clients to make sure client messages are sent only to 
clients in the same room. Allows for .txt file uploads, which are then displayed in the respective chat room. Includes a rename 
button that renames the user and allows previous name to be used by a new client. 

Project Future
I enjoyed this project since it allowed me to learn how to use threading, how TCP connections are handled, and how to implement 
a tkinter GUI. As the main menu shows, I would like to implement a password manager for this application to further secure the rooms. 
I have a file of a password implementation that I’ve yet to complete, which is why the button is not operable. I would also like to 
implement GUI themes to allow the client to choose the color of the interface. Also, there is still some debugging to be done. Some of 
the buttons do not lead back into previous menus. I believe that this may have to do with arrangements of the threads. I would also 
like to add more GUI labels, such as user counters for each of the rooms so that a connecting user knows if a room is already full. 
