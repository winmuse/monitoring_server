import socket
import time
import struct
import os
import interface
import tkinter      #for Linux you must install tkinter and scrot
from threading import Thread

logfp = None
status = ""

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
    if os.path.isdir(str(addr)+" "+username) == False:
        os.mkdir(str(addr)+" "+username)
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
    print("start_thread")

    global logfp
    logfp = open('screen_monitor_server.log', mode='a', buffering=1)
    logfp.write('Start {}\n'.format(time.strftime("%y:%m:%d %H:%M:%S", time.localtime())))
    sock = socket.socket()
    sock.bind(('', 56230))
    sock.listen()

    while True:
        connection, client_address = sock.accept()
        logfp.write('Connected from {}\n'.format(str(client_address)))
        work(connection, client_address[0])
        connection.close()
        if status == "end":
            sock.close()
            break

def main():
    global thread
    thread = Thread(target=start_server, args=("start", "destination_config"))
    thread.start()
    status_playing("playing")
def stop():
    # thread = Thread(target=start_server, args=("start", "destination_config"))
    # thread.join()
    status_playing("end")
    

# if __name__ == '__main__':
#     main()
interface.start.config(command=lambda: main())
interface.end.config(command=lambda: stop())
# interface.pause.config(command=lambda: status_playing("stopped"))

#interface.root.protocol("WM_DELETE_WINDOW", on_closing)
interface.running = True
while interface.running:
    interface.root.update()
    interface.start.place(x=118, y=230, width=172, height=58)
    # interface.pause.place(x=118, y=230, width=172, height=58)
    interface.end.place(x=518, y=230, width=172, height=58)
