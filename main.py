import socket
import io
from PIL import Image
import datetime
import threading
import os
import random
import json


def new_user(id_a, username):
    the_new_user = {
        str(id_a): str(username)
    }
    file_path = 'users.json'
    # בדיקה אם הקובץ קיים
    if os.path.isfile(file_path):
        with open(file_path, 'r') as infile:
            users = json.load(infile)
        users.update(the_new_user)
    else:
        users = the_new_user
    with open(file_path, 'w') as outfile:
        json.dump(users, outfile)
    print(f"Data added to {file_path}")


def get_username(id_a):
    with open("users.json", 'r') as infile:
        users = json.load(infile)
    username = users[str(id_a)]
    return username


def ensure_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def handle_client_connection(client_socket):
    try:
        char_value = client_socket.recv(1)
        have_id = char_value.decode() == '1'
        if not have_id:
            id_a = bytes([random.randint(0, 255) for _ in range(1024)])
            client_socket.send(id_a)
            username = client_socket.recv(1024).decode()
            new_user(str(id_a), username)
        id_a = bytes(client_socket.recv(1024))
        username = get_username(id_a)
        print("hi " + username)

        image_stream = io.BytesIO()
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            image_stream.write(data)

        image_stream.seek(0)
        image = Image.open(image_stream)

        now = datetime.datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        directory_name = f'images_{username}'
        ensure_directory(directory_name)  
        image_path = os.path.join(directory_name, f'image_{formatted_date_time}.png')
        image.save(image_path)
        image.show()
    except Exception as e:
        print(e)
        print("err")
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 5010))
    server_socket.listen(5)

    try:
        while True:
            client_sock, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_thread.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    get_username()
