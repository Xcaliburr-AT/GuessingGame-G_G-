import socket

host = "localhost"
port = 1111

s = socket.socket()
s.connect((host, port))

while True:
    #receiving
    data = s.recv(1024)
    print(data.decode().strip())

    while True:
        #get input
        user_input = input("").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()

        if "Correct" in reply:
            print(reply)
            break
        else:
            print(reply)

    #play again
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again != "yes":
        break

s.close()
