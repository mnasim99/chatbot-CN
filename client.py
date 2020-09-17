#code is implemted in linux
#IMPORTING MODULES

from socket import socket,AF_INET,SOCK_STREAM
import select
import sys
import threading
import os
import time

#FUNTION IMPLEMENTAION FOR SENDING OF MESSAGES FROM CLIENT TO SERVER

def send_msgs(mine_msg):
  
        client_socket.send(bytes(mine_msg,"utf8"))
  
   #IMPLEMENTAION OF CASE1: CLIENT QUIT
        if mine_msg=="QUIT":
            
            client_socket.close()
            sys.exit()

   #CASE2: CLIENT WANTS TO SLEEP THE CONNECTION FOR SOME TIME
        if mine_msg[0:7]=="|sleep|":
           time.sleep(int(mine_msg[7:]))
           

   #CASE3 : CLIENT WANTS TO BLOCK ANOTHER CLIENT
        if mine_msg[0:7]=="|block|":
           block_clients.append(mine_msg[7:])
         
           
   #CASE4: CLIENT WANTS TO UNBLOCK ANOTHER CLIENT
        if mine_msg[0:9]=="|unblock|":
           block_clients.remove(mine_msg[9:])
          
   #CASE5:CLIENT WANTS TO TRANSFER A FILE
        if mine_msg=="send":
                fname=input("Please Enter filename:")
                file_name=fname+".txt"
                print(file_name)
                fsize = os.path.getsize(file_name)
                client_socket.send(str(file_name).encode('utf-8'))
                client_socket.send(str(fsize).encode('utf-8'))
                print(fsize)
                print( "Data sending in progess ...." )
                fileopen = open(file_name,"r")
                read = fileopen.read()
                while True:
                     for line in read:
                         client_socket.send(bytes(line,"utf8"))
                     break
                fileopen.close()

'''def on_closure(event=None):
    mine_msg.set("QUIT")
    send_msgs()'''

#FUNTION IMPLEMENTATION FOR RECIEVING OF MESSAGES ON CLIENT SIDE
def recieve_msgs():
    while True:
        try:
            msg=client_socket.recv(buffer_size).decode("utf-8")
            print(msg)
            messages_list.append(msg)

     #IF RECIEVED MSG IS OF BROADCASTING FILE
            if msg=="FILE-BROADCASTING":
               name1 = client_socket.recv(1024)
               print(name1)
               file_size = client_socket.recv(1024)
               print(file_size)
               server_side=str(name1.decode('utf-8'))
               f_size = len(file_size)
               server_side=server_side+"recieved from server"
               try:
                  with open(name1, 'wb') as fr:
                       print(f_size)
                       rsize = 0
                       while True:
                            file_data = client_socket.recv(1024)
                            rsize = rsize + len(file_data)
                            fr.write(file_data)
                            if rsize >= f_size:
                               print('Going to break file write')
                               break
               finally:
                  fr.close()
               print( "File Data recieved from server...." )
        except OSError:
            break
 

#MAIN METHOD       
messages_list=[]
block_clients=[]
host = input('Please Enter host IP : ')
port_no = input('Please Enter port number: ')

if not port_no:
    port_no = 30000  # DEFAULT VALUE.IN CASE USER FAILS TO GIVE A PORT NUMBER EXCEPTION WILL BE HANDLED
else:
    port_no = int(port_no)

buffer_size = 1024
address = (host, port_no)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

receive_thread = threading.Thread(target=recieve_msgs,args=[])
receive_thread.start()
while True: 
    mine_msg = input()
    send_msgs(mine_msg)
  
server.close()

        
