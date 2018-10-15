#! /usr/bin/env python3
import sys, os, socket, params, time
from threading import Thread
from framedSock import FramedStreamSock
from threading import Lock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
        print("new thread handling connection from", addr)
        lock.acquire()
        try:
            with open('FileRequest'+str(ServerThread.requestCount)+'.txt', "wb") as f:
                while True:
                    msg = self.fsock.receivemsg()
                    if not msg:
                        if self.debug: print(self.fsock, "server thread done")
                        return
                    requestNum = ServerThread.requestCount
                    # time.sleep(0.001)
                    ServerThread.requestCount = requestNum + 1
                    f.write(msg+bytes('\n','utf-8'))
                    msg = ("%s! (%d)" % (msg, requestNum)).encode()
                    self.fsock.sendmsg(msg)
                f.close()
        finally:
            lock.release()

while True:
    sock, addr = lsock.accept()
    lock = Lock()
    ServerThread(sock, debug)
