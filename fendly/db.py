import sqlite3
import os
from flask import current_app,g
from flask.cli import with_appcontext
import psycopg2

# def connect_to_db():
#     sql = sqlite3.connect(os.path.join(os.path.dirname(__file__),'fendly.db'))
#     sql.row_factory = sqlite3.Row
#     return sql

# def get_db():
#     if 'fendly' not in g:
#         g.fendly=connect_to_db()
#     return g.fendly


def get_db():
    sql = psycopg2.connect(user="xmetbafaylxgso",
                                  password="dd70034b30be181c4262a8ed872f0becfdd6c1c7f187a8abcc3e62b85b71528b",
                                  host="ec2-3-231-82-226.compute-1.amazonaws.com",
                                  port="5432",
                                  database="de170uk9i89kkn")
    # curr = sql.cursor()
    return sql
