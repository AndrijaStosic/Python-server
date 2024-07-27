import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')
                text_area.yview(tk.END)
                text_area.config(state=tk.DISABLED)
        except:
            print("An error occurred.")
            client_socket.close()
            break

def send_message(client_socket, entry_widget):
    message = entry_widget.get()
    entry_widget.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))


    root = tk.Tk()
    root.title("Chat Client")


    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

    entry_widget = tk.Entry(root, width=50)
    entry_widget.pack(padx=10, pady=10)
    

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client, entry_widget))
    send_button.pack(padx=10, pady=10)


    thread = threading.Thread(target=receive_messages, args=(client, text_area))
    thread.start()

    root.mainloop()


start_client()
