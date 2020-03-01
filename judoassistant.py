#!/bin/python3

import sys
import configparser
import bcrypt
from sqlalchemy import Table, MetaData, create_engine, text

# users ls
# users rm
# users add
def user_ls(db):
    result = db.execute('select * from users')
    print("Database contains {} user(s)".format(result.rowcount))
    for r in result:
        print("id={}, email={}, password_hash={}".format(r[0], r[1], r[2]))

def user_rm(db, identifier):
    sql = text('delete from users WHERE id = :identifier')
    result = db.execute(sql, identifier=identifier)
    print("Removed {} user(s) from the database".format(result.rowcount))

def user_add(db, email, password):
    password_hash = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    sql = text('insert into users (email, password_hash) values (:email, :password_hash)')
    result = db.execute(sql, email = email, password_hash = password_hash)

    if result.rowcount == 0:
        print("Failed to add users to database")

def tournament_ls(db):
    result = db.execute('select * from tournaments')
    print("Database contains {} tournament(s)".format(result.rowcount))
    for r in result:
        print("id={}, owner={}, web_name={}".format(r[0], r[1], r[3]))

def tournament_rm(db, identifier):
    sql = text('delete from tournaments WHERE id=:identifier')
    result = db.execute(sql, identifier=identifier)
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
    email = str(sys.argv[3])
    password = str(sys.argv[4])
    user_add(db, email, password)
if module == "tournaments" and command == "ls":
    tournament_ls(db)
elif module == "tournaments" and command == "rm":
    identifier = int(sys.argv[3])
    tournament_rm(db, identifier)

