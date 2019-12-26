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

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.connect((HOST, PORT))

g = randint(0,100)
p = randint(0,100)
a = randint(0,100)
A = g ** a % p
sock.send(pickle.dumps((p, g, A)))
B = pickle.loads(sock.recv(1024))
key = B ** a % p
print('Enter your message:')
msg = input()

while msg != 'exit':
     print(f"Send to server:\n message {msg},\n key: {key}")
     send(sock,msg, key)
     print(de_shifr(sock,key))
     msg = input()

sock.close()
