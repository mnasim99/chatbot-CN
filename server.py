# code is implemented in linux
# IMPORT MODULES
from socket import socket,AF_INET,SOCK_STREAM
import select
import sys
from _thread import *
import threading
import os
#import new server_function_definitions


#FUNCTION DEFINITION FOR SENDING OF FILES
def file_send(_file,client): 
    print('All the clients are going to recieve a new file') 
    #file_client=list(client) 
    file_client=array_clients[client]
    #file_client.destroy(client) 
    file_size = os.path.getsize(_file)
    
    count=0 
    for client_socket in file_client: 
        client.send(bytes("FILE-BROADCASTING", "utf8")) 
        client.send(str(_file).encode('utf-8')) 
       
        client.send(str(file_size).encode('utf-8')) 
        fileopen = open(_file,"r") 
        read = fileopen.read() 
        while True: 
            for every_line in read: 
                client.send(bytes(every_line,"utf8"))  
            break
        fileopen.close() 
        count+1
   

#FUNCTION DEFINITION FOR WELCOMING THE NEW CLIENT,
#STORING THE DETAILS(NAME AND IP ADDRESS) OF THE CLIENT 
#AND BROADCASTING EVERY MESSAGE  
     
def clientsthread(client):
   
    name=client.recv(buffer_size).decode("utf-8")
    welcome="%s if you ever want to quit,simply type 'QUIT' and you can exit" % name
    client.send(bytes(welcome,"utf8"))
    message="\n\n\n            '%s has joined the chat'\n" % name
    array_clients[client]=name
    
    broadcast(bytes(message,"utf8"))
    #broadcast(name,client)
    


    while True:
            message=client.recv(buffer_size)
            if message != bytes("QUIT","utf8"):
             
                 broadcast(message,name+':')
      
    # IMPLEMENTING FUNCTIONALITY FOR CHANGE OF NAME BY CLIENT

                 if message[0:6]==bytes("|name|","utf-8"):
                    array_clients[client]=message[6:]
                    inform=array_clients[client] + "has changed name to" + message[6:]
                    broadcast(bytes(inform,"utf-8"))
                    continue

    #IMPLEMENTING TRANSFER OF FILES
                 if message==bytes("send","utf8"):
                  
                     flag=1 
                     name2 = client.recv(1024)
                     f_size=client.recv(1024)
                     serverside=str(name2.decode('utf-8')) 
                     print (serverside)
                     final_name=serverside+"_new"+".txt"
                     print(message)
                     fsize=len(f_size)

                     #fsize = int(f_size.decode('utf-8'))
                     try:
                        with open(final_name, 'wb') as fr:
                             print(f_size)
                             rsize = 0
                             while True:
                                   filedata = client.recv(1024)
                                   rsize = rsize + len(filedata)
                                   fr.write(filedata)
                                   if rsize >= fsize:
                                       print('Breaking from file write')
                                       break
                     finally:
                         fr.close()
                         print("Complete recieving", "utf8")
                         file_send(final_name,client)
 
     #IMPLEMENTING SERVERSIDE CODE FOR THE QUITING CLIENT
            else:
                client.send(bytes("QUIT","utf8"))
                destroy(array_clients[client])
                broadcast(bytes("%s has quit the chat" %name, "utf8"))
                client.close()
                continue
              
             
                     
 #FUNCTION DEFINITION FOR BROADCASTING MESSAGES TO ALL THE CLIENTS            

def broadcast(message,Prefix=''):
    for sock in array_clients:
                sock.send(bytes(Prefix,"utf8")+message)
                #sock.send(message)
           

#FUNCTION IMPLEMENTATION FOR THE REMOVAL OF CLIENTS THAT HAVE LEFT
def destroy(client):
    if client in array_clients:
       array_clients.destroy(connection)


                
            
            

#MAIN METHOD

array_clients={}
array_addresses={}
host='10.0.2.15'
port_no=32000
buffer_size=1024
address=(host,port_no)
server=socket(AF_INET,SOCK_STREAM)   #CREATION OF SOCKET
server.bind(address)
server.listen(50)  # LISTENS FOR 50 STUDENTS IN A CLASS
print("Waiting for connection to be established...")


while True:
          client,client_addr=server.accept()
          print("%s:%s has connected" % client_addr )
          client.send(bytes("\n\n             BENVENUTO!!! \n \n \n" + "Please enter your name:","utf8"))
          array_addresses[client]=client_addr
                  
          ACCEPT_THREAD = threading.Thread(target=clientsthread,args=(client,))
           
          ACCEPT_THREAD.start()



