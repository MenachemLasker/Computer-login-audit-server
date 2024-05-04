import os
import json
import socket


def has_file(name):
    return os.path.isfile(name)


def has_user(username):
    file = "usersPass.json"
    if has_file(file):
        with open(file, 'r') as infile:
            users_pass = json.load(infile)
            return users_pass.get(username)
    return False


def rcv_username(client_socket):
    username = client_socket.recv(1024).decode()
    while has_user(username):
        client_socket.send("0".encode())
        username = client_socket.recv(1024).decode()
    client_socket.send("1".encode())
    return username


def new_user(id_a, username, hashed_pass):
    the_new_user = {
        str(id_a): username
    }
    file = 'users.json'
    if has_file(file):
        with open(file, 'r') as infile:
            users = json.load(infile)
        users.update(the_new_user)
    else:
        users = the_new_user
    with open(file, 'w') as outfile:
        json.dump(users, outfile)
    new_user_and_pass = {
        username: hashed_pass
    }
    file = 'usersPass.json'
    if has_file(file):
        with open(file, 'r') as infile:
            users_and_pass = json.load(infile)
        users_and_pass.update(new_user_and_pass)
    else:
        users_and_pass = new_user_and_pass
    with open(file, 'w') as outfile:
        json.dump(users_and_pass, outfile)
    print(f"Data added")


def get_username(id_a):
    with open("users.json", 'r') as infile:
        users = json.load(infile)
    username = users[str(id_a)]
    return username


def ensure_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
