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

print(f"Server is listening on port {port}")

conn = None
username = None
difficulty = None

while True:
    if conn is None:
        print("Waiting for connection...")
        conn, addr = s.accept()
        print(f"New client: {addr[0]}")

        # Get username
        if username is None:
            conn.sendall(b"Enter your username: ")
            username = conn.recv(1024).decode().strip()

        # Get difficulty level
        if difficulty is None:
            conn.sendall(b"Choose difficulty level:\n1. Easy\n2. Medium\n3. Hard\nEnter your choice (1, 2, or 3): ")
            choice = conn.recv(1024).decode().strip()
            if choice not in ["1", "2", "3"]:
                conn.sendall(b"Invalid choice. Please enter 1, 2, or 3.")
                conn.close()
                conn = None
                username = None
                difficulty = None
                continue

            if choice == "1":
                difficulty = "easy"
                guessme = rand_number(1, 50)
            elif choice == "2":
                difficulty = "medium"
                guessme = rand_number(1, 100)
            elif choice == "3":
                difficulty = "hard"
                guessme = rand_number(1, 500)

            conn.sendall(banner.encode())
            attempts = 0
            continue

    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        attempts += 1
        print(f"{username} guess attempt: {guess}")

        if guess == guessme:
            conn.sendall(b"Guessed Correctly!")
            conn.close()
            conn = None
            username = None
            difficulty = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!: \nEnter Guess: ")
        elif guess < guessme:
            conn.sendall(b"Guess Higher!: \nEnter Guess: ")

s.close()
