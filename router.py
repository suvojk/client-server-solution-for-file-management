"""This module is responsible for hadling client requests for every service provided by server"""

import json
import uuid
import os
import re

from db import db
from config import *

class Router():
    """Router class to handle all the commands requested by client
    methods:
        register
        login
        list
        create_folder
        read_file
        write_file
        change_folder
    """

    def __init__(self):
        """construcor method to initiate instance"""

        # create store if not exists
        if not os.path.isdir(STORE_PATH):
            os.mkdir(STORE_PATH)

        self.files = {}

    def register(self, data):
        """Adds a new user to database
        Input: Username and Password
        Returns a message accordingly
        """
        username = data['body']['username']
        password = data['body']['password']

        if username in db.data['user_ids']:
            return {
        "status": 500,
        "message": "User already exists"
            }

        user_id = str(uuid.uuid4())
        user_dir = os.path.join(STORE_PATH, username)

        if not os.path.isdir(user_dir):
            os.mkdir(user_dir)

        db.data['users'][user_id] = {
            'username': username,
            'password': password,
            'dir': user_dir,
            'cwd': user_dir + '/',
        }
        db.data['user_ids'][username] = user_id
        db.commit()

        return {
            "status": 200,
            "message": "Registration successfull",
            "token": user_id
        }

    def login(self, data):
        """Logs in a user
        Gives error if user credentials are incorect
        Input: Username and Password
        Returns a message accordingly
        """
        username = data['body']['username']
        password = data['body']['password']

        if 'token' in data and data['token'] in db.data['users']:
            return {
        "status": 500,
        "message": "Already Logged in"
            }

        if username not in db.data['user_ids']:
            return {
        "status": 500,
        "message": "User not found"
            }

        user_id = db.data['user_ids'][username]
        if db.data['users'][user_id]['password'] != password:
            return {
        "status": 500,
        "message": "Invalid credentials"
            }

        return {
            "status": 200,
            "message": "Login successfull",
            "token": user_id
        }


    def list(self, data):
        """Lists all files in current working directory
        It gets cwd from user data in database
        """
        user = db.data['users'][data['token']]
        array = os.listdir(user['cwd'])
        files = []
        for file in array:

            if os.path.isfile( user['cwd'] + file):
                stat = os.stat( user['cwd'] + file)
                files.append({
                "name": file,
                "size": stat.st_size,
                "ctime": stat.st_ctime
                })
        return {
            "status": 200,
            "data": files
        }

    def create_folder(self, data):
        """Creates a new folder under user's directory
        Input: folder name
        """
        user = db.data['users'][data['token']]

        if not re.match(r"^[a-zA-Z0-9_]+$", data['body']['folder']):
            return {
        "status": 500,
        "message": "Invalid folder name"
            }

        folder_path = user['cwd'] + data['body']['folder'] + '/'
        if os.path.isdir(folder_path):
            return {
        "status": 500,
        "message": "Directory already exists"
            }

        os.mkdir(folder_path)
        return {
            "status": 200,
            "message": "Created Directory"
        }

    def write_file(self, data):
        """Writes data to a file
        Opens a file if exists and creates a new one if file doesn't exist
        Input: takes filename
        """
        user = db.data['users'][data['token']]

        if not re.match(r"^[a-zA-Z0-9_.]+$", data['body']['filename']):
            return {
        "status": 500,
        "message": "Invalid file name"
            }

        file_name = user['cwd'] + data['body']['filename']
        file_content = data['body']['content']

        with open(file_name, 'a') as file:
            file.write('\n')
            file.write(file_content)

        return {
            "status": 200,
            "message": "Written to file"
        }

    def read_file(self, data):
        """Reads a file from users current directoty
        File will be read in chunks of size 100
        Takes a file name
        """
        user_id = data['token']
        user = db.data['users'][data['token']]

        if not data['body']['filename']:

            if user_id in self.files: del self.files[user_id]
            return {
        "status": 200,
        "message": "Current file closed"
            }

        if not re.match(r"^[a-zA-Z0-9_.]+$", data['body']['filename']):
            return {
        "status": 500,
        "message": "Invalid file name"
            }

        file_name = user['cwd'] + data['body']['filename']

        if not os.path.isfile(file_name):
            return {
        "status": 500,
        "message": "File doesn't exists"
            }

        content = ""

        if user_id in self.files:
            file = self.files[user_id]
            content = file.read(100)
        else:
            file = open(file_name, 'r')
            content = file.read(100)
            self.files[user_id] = file

        return {
            "status": 200,
            "data": content
        }

    def change_folder(self, data):
        """Changes the current working directory of user
        Cannot traverse out of the user's directory
        """
        user = db.data['users'][data['token']]
        temp_folder = data['body']['folder']

        if temp_folder != '..' and not re.match(r"^[a-zA-Z0-9_]+$", temp_folder):
            return {
        "status": 500,
        "message": "Invalid folder name"
            }


        cwd = user['cwd'].split('/')[-2]

        if temp_folder == '..' and cwd == user['username']:
            return {
        "status": 500,
        "message": "Invalid folder name"
            }

        folder_path = user['cwd'] + data['body']['folder'] + '/'
        if not os.path.isdir(folder_path):
            return {
        "status": 500,
        "message": "Directory not exists"
            }
        user['cwd'] = os.path.realpath(user['cwd'] + data['body']['folder']) + '/'
        return {
            "status": 200,
            "message": "Changed Directory"
        }



    def request(self, data):
        """This method servers as a proxy for above methods
        It loads and dumps data accordinly
        Also routes to a correct method using conditions
        """
        data = json.loads(data)
        action = data['action']

        response = {}

        if action in ['register', 'login']:
            if action == 'register':
                response = self.register(data)
            elif action == 'login':
                response = self.login(data)
            response = json.dumps(response)
            return response

        if data['token'] not in db.data['users']:
            response = {
        "status": 500,
        "message": "Not Authenticated! Please login",
            }
            response = json.dumps(response)
            return response

        if action == 'change_folder':
            response = self.change_folder(data)
        elif action == 'list':
            response = self.list(data)
        elif action == 'read_file':
            response = self.read_file(data)
        elif action == 'write_file':
            response = self.write_file(data)
        elif action == 'create_folder':
            response = self.create_folder(data)
        else:
            response = {
        "status": 500,
        "message": "Invalid action"
            }

        response = json.dumps(response)
        return response


router = Router()