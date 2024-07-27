import socket
import threading


clients = []


def handle_client(conn, addr):
    print(f'New connection: {addr}')
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f'{addr}: {message}')
                broadcast(message, conn)
            else:
                remove(conn)
                break
        except:
            continue


def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Server is listening on port 12345")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()