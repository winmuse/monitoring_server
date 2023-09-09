import socket
import time
import struct
import os
import interface
import tkinter      #for Linux you must install tkinter and scrot
from threading import Thread
import psutil
from win10toast import ToastNotifier
import sys
import tkinter as tk
from tkinter import messagebox
import datetime  

logfp = None
status = ""
server_thread = None
def exit_interface():
    interface.root.destroy()
def remove_file(root_directory):
    # while True:
    if os.path.exists(root_directory):
        directories = os.listdir(root_directory)
        for each_directory in directories:
            each_directory_files = root_directory + '\\' + each_directory
            files = os.listdir( each_directory_files )
            if files:
                for file in files:
                    current_file = each_directory_files + '\\' + file 
                    created_file_time = file.split(' ')[1].split('.')[0]
                    current_time = datetime.datetime.now()
                    change_time_dt = datetime.datetime.strptime(created_file_time, "%d-%m-%Y-%H-%M-%S")
                    diff = (current_time - change_time_dt).total_seconds() / 60
                    if diff >= 60 * 24 * 2:
                        os.remove( current_file )
                    else :
                        pass
            else:
                pass
    else :
        pass
def check_memory():
    global check_memory_status
    check_memory_status = True
    global root_directory
    root_directory ="Client_data"
    mem = psutil.virtual_memory()
    remaining_memory = mem.available / (1024 ** 3)  # Convert bytes to GB

    if remaining_memory < 10:
        response = messagebox.askquestion("Insufficient system memory capacity", "Would you like to automatically delete record files older than 48 hours?")
        print(response)
        if response == 'yes':
            remove_file(root_directory)
            # check_memory_status = False               
        else :
            print('faild')
            pass
check_memory()
def recvall(sock, msgsize):
    result = bytearray()
    while msgsize > 0:
        buff = sock.recv(msgsize)
        if not buff:
            break
        result.extend(buff)
        msgsize -= len(buff)
    return result

def work(sock, addr):
    ts = int(time.time() * 1000)
    sock.settimeout(60)
    buf = sock.recv(struct.calcsize("<QQ64s64sI"))
    if len(buf) != struct.calcsize("<QQ64s64sI"):
        logfp.write('len(buf) != struct.calcsize()\n')
        return
    currtime, idletime, filename, username, imglen = struct.unpack("<QQ64s64sI", buf)
    filename = filename.decode("utf-8").split('\0', 1)[0]
    username = username.decode("utf-8").split('\0', 1)[0].replace(" ", "")
    buf = recvall(sock, imglen)
    if len(buf) != imglen:
        logfp.write('{} {}'.format(len(buf), imglen))
        logfp.write('len(buf) != imglen\n')
        return
    if os.path.isdir(root_directory + str(addr)+" "+username) == False:
        os.mkdir(root_directory + str(addr)+" "+username)
    with open(time.strftime(str(addr)+" "+username+'/' + filename, time.localtime()), 'wb') as imgfp:
        imgfp.write(buf)
    logfp.write('{}\t{}\t{}\t{}\t{}\n'.format(ts, currtime, idletime, filename, username))
# Report what's happening
def status_playing(yeter):
    global status
    status = yeter
    if status == "stopped":
        interface.start["state"] = "normal"
        interface.canvas.itemconfig(interface.info, text="")
    elif status == "playing":
        interface.end["state"] = "normal"
        interface.start["state"] = "disabled"
        interface.canvas.itemconfig(interface.info, text="Frame Recorder Server is started")
    elif status == "end":
        interface.canvas.itemconfig(interface.info, text="Frame Recorder Server")
        interface.end["state"] = "disabled"
        interface.start["state"] = "normal"

def start_server(arg1, arg2):
    print("start_threads")

    global logfp
    logfp = open('screen_monitor_server.log', mode='a', buffering=1)
    logfp.write('Start {}\n'.format(time.strftime("%y:%m:%d %H:%M:%S", time.localtime())))
    global sock
    sock = socket.socket()
    sock.bind(('', 56230))
    sock.listen()

    while True:
        connection, client_address = sock.accept()
        logfp.write('Connected from {}\n'.format(str(client_address)))
        work(connection, client_address[0])
        connection.close()

def main():
    global server_thread
    print(status)
    server_thread = Thread(target=start_server, args=("start", "destination_config"))
    server_thread.start()
    status_playing("playing")
    # time.sleep(20)
    
    # status = "end"
    
def stop():
    sock.close()
    status_playing("end")
    server_thread.join()
    print("stop thread")

# if __name__ == '__main__':
#     main()
interface.start.config(command=lambda: main())
interface.end.config(command=lambda: stop())
  
#interface.root.protocol("WM_DELETE_WINDOW", on_closing)
interface.running = True
while interface.running:
    interface.root.update()
    interface.start.place(x=118, y=230, width=172, height=58)
    # interface.pause.place(x=118, y=230, width=172, height=58)
    interface.end.place(x=518, y=230, width=172, height=58)
