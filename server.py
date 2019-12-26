import socket
import pickle
from random import randint


#шифрование
def shifr(cript, key): 
    c = [chr(ord(cript[i]) ^ key) for i in range(len(cript))]
    return ''.join(c)

#отправка
def send(conn, msg, key):
    msg = shifr(msg, key)
    conn.send(pickle.dumps(msg))

#дешифровка
def de_shifr(conn, key):
    msg = pickle.loads(conn.recv(1024))
    msg = shifr(msg, key)
    return msg

def check(key):

     with open('key.txt', 'r') as file:
         f = False
         for line in file:
             if int(line) == key:
                 f = True
                 break
     return f


HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
print(pickle.loads(msg))
p, g, A = pickle.loads(msg)
b = randint(0, 300)
B = g ** b % p
conn.send(pickle.dumps(B))
key = A ** b % p

while True:
    try:
        f = check(key)
        if f == False:
                print("incorrect key");
                send(conn, "incorrect key", key)
                break
        msg = de_shifr(conn, key)
        print(f"From client:\n{conn},\n{key}\n")
        print(f"To client:\n{msg}")
        send(conn, msg, key)

    except EOFError:
        break

conn.close()
