import tkinter as tk
from tkinter import ttk, filedialog
import socket
import RC4
import RSA
import sDES
import TDES
import threading
import hashlib
import subprocess
import verification
import random
import re  # Added for regex
client_socket = None


# Function to validate IP address
def is_valid_ip(ip):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return re.match(pattern, ip)


def received_Messages(ciphertext):
    hash_and_message = ciphertext.split('|')
    received_hash = hash_and_message[0]
    received_key_hash = hash_and_message[1]
    encrypted_message = hash_and_message[2]

    print(f"Encrypted text: {encrypted_message}")

    # Calculate MD5 hashes for each algorithm
    hash_rc4 = hashlib.md5(b'RC4').hexdigest()
    hash_RSA = hashlib.md5(b'RSA').hexdigest()
    hash_sDES = hashlib.md5(b'sDES').hexdigest()
    hash_TDES = hashlib.md5(b'TDES').hexdigest()
    hash_AES = hashlib.md5(b'AES').hexdigest()

    # Compare received hash with computed hashes to identify the algorithm
    if received_hash == hash_rc4:
        identified_algorithm = 'RC4'
    elif received_hash == hash_RSA:
        identified_algorithm = 'RSA'
    elif received_hash == hash_sDES:
        identified_algorithm = 'sDES'
    elif received_hash == hash_TDES:
        identified_algorithm = 'TDES'
    elif received_hash == hash_AES:
        identified_algorithm = 'AES'
    else:
        identified_algorithm = 'Unknown'

    print(f"Identified Algorithm: {identified_algorithm}")
    print(f"Received Key Hash: {received_key_hash}")
    print(f"Received Key Hash: {hash_RSA}")
    key = "123456789012345678901234"
    md5_key_hash = hashlib.md5(key.encode()).hexdigest()

    plaintext = ""

    if md5_key_hash == received_key_hash:
        key = "123456789012345678901234"
    private_key = (10609, 14017)

    if identified_algorithm == "RC4":
        plaintext = RC4.RC4(encrypted_message, key)
    if identified_algorithm == "sDES":
        plaintext = sDES.sdes_decrypt(encrypted_message, key)
    if identified_algorithm == "TDES":
        plaintext = TDES.tdes_decrypt(encrypted_message, key)
    if identified_algorithm == "RSA":
        plaintext = RSA.rsa_decrypt(encrypted_message, private_key)
    if identified_algorithm == "AES":
        plaintext = TDES.tdes_decrypt(encrypted_message, key)
    print(f"key: {key} plaintext: {plaintext}")
    return plaintext


def receive_messages():
    while True:
        try:
            message_received = client_socket.recv(1024).decode('utf-8')
            plaintext = received_Messages(message_received)
            if plaintext:
                print(f"Server: {plaintext}")  # Print the message to the console
                received_textarea.config(state=tk.NORMAL)
                received_textarea.insert(tk.END, f"{plaintext}\n")
                received_textarea.config(state=tk.DISABLED)
                received_textarea.yview(tk.END)
            else:
                break
        except:
            break
        
import os


def on_button_click_connect():
    
    # Client setup
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = ip_address_server_entry.get() # Replace with the actual server IP address

    if not is_valid_ip(server_ip):
        print("Invalid IP address. Please enter a valid one.")
        return

    port = 8080
    client_socket.connect((server_ip, port))

    accept_thread1 = threading.Thread(target=receive_messages)
    accept_thread1.daemon = True
    accept_thread1.start()

def select_file():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select a File")
    if file_path:
        file_path_var.set(file_path)  # Update the label or entry with the selected file path


def verify_sign():
    text_get_path = file_path_var.get()
    # subprocess.Popen(['python3', 'verification.py', text_get_path])
    is_it_valid=verification.verification(text_get_path)
    print(is_it_valid)
    if(is_it_valid):
        file_path_var1.set("Valid Signature")
    else:
        file_path_var1.set("InValid Signature")



# Create the main window
root = tk.Tk()
root.title(f"Cyber Security Receiver")
screen_width = 780
screen_height = 780
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

# Create a frame for layout purposes
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

##connect to server
connect_label = ttk.Label(frame, text="Connect to server: ")
connect_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

## entrybox for ip address
ip_address_server_entry = ttk.Entry(frame)
ip_address_server_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

## button for starting connection

# Create a Button
button = ttk.Button(frame, text="Connect", command=on_button_click_connect)
button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

# Create a TextArea for received messages
received_label = ttk.Label(frame, text="Received messages from server:")
received_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

received_textarea = tk.Text(frame, height=10, width=40)
received_textarea.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
received_textarea.config(state=tk.DISABLED)

# Create a button that opens the file selector
file_button = tk.Button(frame, text="Select File", command=select_file)
file_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

# Create a label to show the selected file path
file_path_var = tk.StringVar()
file_path_label = ttk.Label(frame, textvariable=file_path_var, anchor='w', relief='sunken', width=50)
file_path_label.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

# Create a button that Signs the file selector
sign_btn = tk.Button(frame, text="Verify Signature", command=verify_sign)
sign_btn.grid(row=3, column=0, padx=5, pady=5,sticky=tk.W)

# Create a label to show the verified file 
file_path_var1 = tk.StringVar()
file_path_label1 = ttk.Label(frame, textvariable=file_path_var1, anchor='w', relief='sunken', width=50)
file_path_label1.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

# Run the main event loop
root.mainloop()
