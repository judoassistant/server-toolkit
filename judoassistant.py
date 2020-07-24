#!/bin/python3

import argparse
import bcrypt
import configparser
import sys
import os
from sqlalchemy import Table, MetaData, create_engine, text

def user_remove(db, args):
    sql = text('delete from users WHERE id = :identifier')
    result = db.execute(sql, identifier=args.identifier)
    print("Removed {} user(s) from the database".format(result.rowcount))

def user_add(db, args):
    password_hash = str(bcrypt.hashpw(args.password.encode('utf-8'), bcrypt.gensalt()), encoding="utf-8")
    # password_hash = "$2a$12$1rHate3ZkEnXS89xkCb5leW.bmvefC4Zj9JfZNnwe45GjZj7Cu7na"
    # print(len(password_hash))
    sql = text('insert into users (email, password_hash) values (:email, :password_hash)')
    result = db.execute(sql, email = args.email, password_hash = password_hash)

    if result.rowcount == 0:
        print("Failed to add users to database")

def user_list(db, args):
    result = db.execute('select * from users')
    print("Database contains {} user(s)".format(result.rowcount))
    for r in result:
        print("id={}, email={}, password_hash={}".format(r[0], r[1], r[2]))

def tournament_remove(db, args):
    sql = text('delete from tournaments WHERE id=:identifier')
    result = db.execute(sql, identifier=args.identifier)
    print("Removed {} tournament(s) from the database".format(result.rowcount))

def tournament_list(db, args):
    result = db.execute('select * from tournaments')
    print("Database contains {} tournament(s)".format(result.rowcount))
    for r in result:
        print("id={}, owner={}, web_name={}, name={}, location={}, date={}".format(r[0], r[1], r[3], r[6], r[7], r[8]))

# config = configparser.ConfigParser()
# config.read('config.ini')

# module = sys.argv[1]
# command = sys.argv[2]

def __handle(db, args):
    pass

parser = argparse.ArgumentParser(prog="judoassistant.py")
parser.set_defaults(func=__handle)

subparsers = parser.add_subparsers()

# User Parser
user_parser = subparsers.add_parser("user", help="manage users")
user_subparsers = user_parser.add_subparsers()

user_add_parser = user_subparsers.add_parser("add", help="add a user")
user_add_parser.add_argument("email")
user_add_parser.add_argument("password")
user_add_parser.set_defaults(func=user_add)

user_remove_parser = user_subparsers.add_parser("remove", aliases=["rm"], help="remove a user")
user_remove_parser.add_argument("email")
user_remove_parser.set_defaults(func=user_remove)

user_list_parser = user_subparsers.add_parser("list", aliases=["ls"], help="list users")
user_list_parser.set_defaults(func=user_list)

# Tournament parser
tournament_parser = subparsers.add_parser("tournament", help="manage tournaments")
tournament_subparsers = tournament_parser.add_subparsers()

tournament_remove_parser = tournament_subparsers.add_parser("remove", aliases=["rm"], help="remove a tournament")
tournament_remove_parser.add_argument("identifier")
tournament_remove_parser.set_defaults(func=tournament_remove)

tournament_list_parser = tournament_subparsers.add_parser("list", aliases=["ls"], help="list tournaments")
tournament_list_parser.set_defaults(func=tournament_list)

# Parse args, connect to db and run commands
args = parser.parse_args()

database_url = os.environ.get('DATABASE_URL')
if database_url is None:
    print("Please set the DATABASE_URL environment variable")
    sys.exit()

db = create_engine(database_url)

args.func(db, args)
