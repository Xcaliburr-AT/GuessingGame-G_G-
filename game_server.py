import socket
import random

host = ""
port = 1111
banner = """
============================
==== Guessing Game v1.0 ====
============================
\nEnter your guess:"""


def rand_number(low, high):
    return random.randint(low, high)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)


print(f"server is listening in port {port}")
guessme = 0
conn = None
while True:
    if conn is None:
        print("waiting for connection...")
        conn, addr = s.accept()
        guessme = rand_number(1,50)
        print(f"new client: {addr[0]}")
        cheat_str = f" ==== number to guess is {guessme} \n" + banner
        conn.sendall(cheat_str.encode())

    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b" Guessed Correctly!")
            conn.close()
            conn = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!: \nEnter Guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!: \nEnter Guess: ")
            continue

s.close()
