import socket
import tqdm
import os
import sys

args = sys.argv

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

filename = args[1]
host = args[2]
port = int(args[3])

filesize = os.path.getsize(filename)

# client socket

print(host, port)


def send_file():
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(1)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()


send_file()
