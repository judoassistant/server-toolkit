#!/bin/python3

import sys
import configparser
from sqlalchemy import Table, MetaData, create_engine

# users ls
# users rm
# users add
def user_ls(db):
    result = db.execute("select * from users")
    print("Database contains {} user(s)".format(result.rowcount))
    for r in result:
        print("id={}, email={}".format(r[0], r[1]))

def user_rm(db, identifier):
    result = db.execute("delete from users WHERE id={}".format(identifier))
    print("Removed {} user(s) from the database".format(result.rowcount))

def user_add(db, email, password):
    pass
    # has
    # result = db.execute("delete from users WHERE id={}".format(identifier))
    # if result.rowcount == 0:
    #     print("Failed to add users to database")

def tournament_ls(db):
    result = db.execute("select * from tournaments")
    print("Database contains {} tournament(s)".format(result.rowcount))
    for r in result:
        print("id={}, owner={}, web_name={}".format(r[0], r[1], r[3]))

def tournament_rm(db, identifier):
    result = db.execute("delete from tournaments WHERE id={}".format(identifier))
    print("Removed {} tournament(s) from the database".format(result.rowcount))

config = configparser.ConfigParser()
config.read('config.ini')
db = create_engine(config["judoassistant"]["connect_string"])

module = sys.argv[1]
command = sys.argv[2]

if module == "users" and command == "ls":
    user_ls(db)
elif module == "users" and command == "rm":
    identifier = int(sys.argv[3])
    user_rm(db, identifier)
elif module == "users" and command == "add":
    email = sys.argv[3]
    password = sys.argv[4]
    user_add(db, email, password)
if module == "tournaments" and command == "ls":
    tournament_ls(db)
elif module == "tournaments" and command == "rm":
    identifier = int(sys.argv[3])
    tournament_rm(db, identifier)

