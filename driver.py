"""This module is responsible to handle user interaction and message passing to server"""

import doctest

from client import client
from config import *

def register(tokens):
    """Sends a registration request to server
    
    Input: Takes username and password
    Return: Prints the server response

    >>> login(['login', 'random', 'random'])
    User not found

    >>> register(['register', 'test', 'test'])
    Registration successfull

    >>> register(['register', 'test', 'test'])
    User already exists

    """
    try:
        username = tokens[1]
        password = tokens[2]
    except IndexError:
        print("Invalid arguments")
        return

    data = {
        "action": "register",
        "body": {
            "username": username,
            "password": password
        }
    }
    res = client.send(data)
    print(res['message'])

def login(tokens):
    """Sends a login request to server
    
    Input: Takes username and password
    Return: Prints the server response

    >>> login(['login', 'test', 'test'])
    Already Logged in

    """
    try:
        username = tokens[1]
        password = tokens[2]
    except IndexError:
        print("Invalid arguments")
        return

    data = {
        "action": "login",
        "body": {
            "username": username,
            "password": password
        }
    }
    res = client.send(data)
    print(res['message'])

def change_folder(tokens):
    """Sends a request to change the folder
    
    Input: Takes folder name
    Return: Prints the server response

    >>> change_folder(['change_folder', 'unexisting'])
    Directory not exists

    >>> create_folder(['create_folder', 'new_dir'])
    Created Directory

    >>> change_folder(['change_folder', 'new_dir'])
    Changed Directory

    """
    try:
        folder = tokens[1]
    except IndexError:
        print("Invalid arguments")
        return

    data = {
        "action": "change_folder",
        "body": {
            "folder": folder
        }
    }
    res = client.send(data)
    print(res['message'])

def list_cwd():
    """Sends a request to list files in current directory

    Return: Prints the server response
    """
    data = {
        "action": "list",
    }
    res = client.send(data)
    if 'data' in res:
        for file in res['data']:
            print(f"%s\t%s\t%s" % (file['name'], file['size'],  file['ctime']))
    else:
        print(res['message'])

def read_file(tokens):
    """Sends a request to read 100 bytes of given file 
    
    Input: Takes name of file
    Return: Prints the server response
    """
    try:
        filename = tokens[1]
    except IndexError:
        filename = ""

    data = {
        "action": "read_file",
        "body": {
            "filename": filename
        }
    }
    res = client.send(data)
    if 'data' in res:
        print(res['data'])
    else:
        print(res['message'])

def write_file(tokens):
    """Sends a request to write to file
    
    >>> write_file(['write_file', 'testfile', 'Hello world'])
    Written to file

    Input: Takes file name
    Return: Prints the server response
    """
    try:
        filename = tokens[1]
        content = " ".join(tokens[2:])
    except IndexError:
        print("Invalid arguments")
        return

    data = {
        "action": "write_file",
        "body": {
            "filename": filename,
            "content": content
        }
    }
    res = client.send(data)
    print(res['message'])


def create_folder(tokens):
    """Sends a request to create the folder

    >>> create_folder(['create_folder', 'test_folder'])
    Created Directory

    >>> create_folder(['create_folder', 'test_folder'])
    Directory already exists
    
    Input: Takes folder name
    Return: Prints the server response
    """
    try:
        folder = tokens[1]
    except IndexError:
        print("Invalid arguments")
        return

    data = {
        "action": "create_folder",
        "body": {
            "folder": folder
        }
    }
    res = client.send(data)
    print(res['message'])

def quit():
    """User get logged out
    Closes the socketconnection and program exits
    """
    client.token = ""
    client.close()
    exit()

def info_server():
    """prints server commands list"""
    print("\ncommands available: ")
    print("$ register <username> <password>")
    print("$ login <username> <password>")
    print("$ change_folder <name>")
    print("$ list")
    print("$ read_file <name>")
    print("$ write_file <name> <input>")
    print("$ create_folder <name>")
    print("$ quit \n")

def main():
    """The driver function"""
    print("Client application\n")
    print("commands available: ")
    print("$ commands")
    print("$ quit")

    while True:
        
        tokens = input("\n$ ").split(' ')
        if not len(tokens):
            print("Enter any command")
            continue

        cmd = tokens[0]

        if cmd == 'register':
            register(tokens)
        elif cmd == 'login':
            login(tokens)
        elif cmd == 'create_folder':
            create_folder(tokens)
        elif cmd == 'write_file':
            write_file(tokens)
        elif cmd == 'read_file':
            read_file(tokens)
        elif cmd == 'list':
            list_cwd()
        elif cmd == 'change_folder':
            change_folder(tokens)
        elif cmd == 'commands':
            info_server()
        elif cmd == 'quit':
            quit()
        else:
            print("Invalid command")
            continue

def run_docktest():
    doctest.run_docstring_examples(register, globals())
    doctest.run_docstring_examples(login, globals())
    doctest.run_docstring_examples(change_folder, globals())
    doctest.run_docstring_examples(create_folder, globals())
    doctest.run_docstring_examples(read_file, globals())
    doctest.run_docstring_examples(write_file, globals())

if __name__=='__main__':
    # run_docktest()
    main()