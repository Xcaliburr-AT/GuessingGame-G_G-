import socket


host = "localhost"
port = 1111



s = socket.socket()
s.connect((host, port))


#receiving
data = s.recv(1024)

#print
print(data.decode().strip())



while True:
    #getting input
    user_input = input("").strip()

    s.sendall(user_input.encode())
    reply = s.recv(1024).decode().strip()
    if "Correct" in reply:
        print(reply)
        break
    print(reply)
    continue
s.close
