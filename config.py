"""Provides config variables to server"""
from os.path import realpath, join, dirname

BIND_ADDRESS="127.0.0.1"
BIND_PORT=1337

STORE_PATH=realpath(join(dirname(__file__), '../store'))
DB_PATH=realpath(join(dirname(__file__), '../database.json'))
