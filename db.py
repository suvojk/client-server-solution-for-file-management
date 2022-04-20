"""This module is responsible for handling database functions for application"""

import os
import json
from json.decoder import JSONDecodeError

from config import DB_PATH

class Database():
    """This class provides a minimal database functionality using json file
    methods:
        commit
        dump
        close
    """
    db_path = DB_PATH

    def __init__(self):
        """Constructor class to initialise the instance
        Reads database form old file if exists
        """
        if os.path.isfile(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as old_file:
                try:
                    self.data = json.load(old_file)
                except JSONDecodeError:
                    self.data = {'users': {}, 'user_ids': {}}
        else:
            self.data = {'users': {}, 'user_ids': {}}

        self.commit()

    def commit(self):
        """Commits all the changes made to db object to the database file"""
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.data))

    def dump(self):
        """Dumps all the data in database"""
        return self.data

db = Database()
