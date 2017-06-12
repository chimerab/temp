#!/usr/bin/python

import sys
import socket
import getopt
import threading
import subprocess

listen  = False
command = False
upload  = False
execute = ""
target  = ""
upload_dest = ""
port    = 0

def usage():
    print "BHP Tools"
    print
    print "Usage: %s -t target target_host -p port"%__file__
    print "-l --listen          -listen on [host]:[port] for" \
          "incoming connections"
    sys.exit(0)


def main():
    global listen
    global target
    global command
    global upload
    global execute
    global upload_dest
    global port

    if not len(sys.argv[1:]):
        usage()


    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command",
                                                              "upload"])

    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","-execute"):
            execute = a
        elif o in ("-u","--upload"):
            upload_dest = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        elif o in ("-c","--commandshell"):
            command = True
        else:
            assert False,"Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print target, port
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if not data:
                    client.close()
                    return
                if recv_len < 4096:
                    break


            print response

            buffer = raw_input("Input:")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()


def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket,addr = server.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()

#    try:
    output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)

#    except:
#output = "Failed to execute command .\r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_dest):
        print "upload file:%s" % upload_dest
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if not data or data.strip() == "END":
                print "receive data complete."
                break
            else:
                print "received data:%s" % data
                file_buffer += data
                client_socket.send("data received.")

        try:
            file_descriptor = open(upload_dest,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved file to %s\r\n" % upload_dest)
            client_socket.close()
        except:
            client_socket.send("Failed to save file")
            client_socket.close

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send("BHP:#>")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                response = run_command(cmd_buffer)
                client_socket.send(response)




main()
