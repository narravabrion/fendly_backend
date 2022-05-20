
from flask import current_app,g
from flask.cli import with_appcontext
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db():
    sql = psycopg2.connect(user="xmetbafaylxgso",
                                  password="dd70034b30be181c4262a8ed872f0becfdd6c1c7f187a8abcc3e62b85b71528b",
                                  host="ec2-3-231-82-226.compute-1.amazonaws.com",
                                  port="5432",
                                  database="de170uk9i89kkn",
                                  cursor_factory=RealDictCursor)
    # curr = sql.cursor()
    return sql
