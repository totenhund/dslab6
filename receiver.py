import socket
import tqdm
import os
from threading import Thread
import time

# server IP address
SERVER_HOST = "xx.xx.xx.xx"
SERVER_PORT = 8080
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


saved_files = []


def receive_file(client_socket, address):
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    num_copy = 0
    was = False
    name = filename.split('.')
    for i in saved_files:
        if name[0] in i:
            was = True
            num_copy += 1

    # if file was send before add copy_num
    if was:
        if len(name) > 1:
            cont = ''
            for i in range(1, len(name)):
                cont += name[i]
            filename = name[0] + '_copy{}'.format(num_copy) + '.' + cont
        else:
            filename = name[0] + '_copy{}'.format(num_copy)

    saved_files.append(filename)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(1)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


# create the server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to our address
s.bind(('', SERVER_PORT))

# enabling our server to accept connections
s.listen()
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
while True:
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    thread = Thread(target=receive_file, args=(client_socket, address))
    thread.start()
