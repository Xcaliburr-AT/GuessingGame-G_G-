import socket
import random

host = ""
port = 1111
banner = """
============================
==== Guessing Game v1.0 ====
============================
\nEnter your guess: """

#dictionary to store scores
leaderboard = {
    "easy": [],
    "medium": [],
    "hard": []
}

def rand_number(low, high):
    return random.randint(low, high)

def update_leaderboard(username, score, difficulty):
    leaderboard[difficulty].append({"username": username, "score": score})

def display_leaderboard():
    print("Leaderboard:")
    for difficulty, scores in leaderboard.items():
        print(f"\nDifficulty: {difficulty}")
        sorted_scores = sorted(scores, key=lambda x: x['score'])
        for idx, entry in enumerate(sorted_scores, 1):
            print(f"{idx}. {entry['username']} - {entry['score']} tries")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")
print("Waiting for connection...")

username = None
difficulty = None
while True:
    conn, addr = s.accept()
    print(f"New client: {addr[0]}")

    
    
    while True:

        #get username
        if username is None:
            conn.sendall(b"===Enter your username: ===")
            username = conn.recv(1024).decode().strip()

        while True:
            conn.sendall(b"Choose difficulty level:\n1. Easy Range-(1,50)\n2. Medium Range-(1,100)\n3. Hard (1,500)\nEnter your choice (1, 2, or 3): ")
            choice = conn.recv(1024).decode().strip()
            if choice in ["1", "2", "3"]:
                break
            else:
                conn.sendall(b"Invalid choice. Please press Enter to select again and choose 1, 2, or 3.")

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

        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            attempts += 1
            print(f"{username} guess attempt: {guess}")

            if guess == guessme:
                update_leaderboard(username, attempts, difficulty)
                conn.sendall(f"Guessed Correctly in {attempts} tries!".encode())
                display_leaderboard()
                username = None
                difficulty = None
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!: \nEnter Guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!: \nEnter Guess: ")

s.close()
