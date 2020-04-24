# to get environment variables
# and to generate random hash
import os

# for token storage
import binascii

#flask functionality
from flask import Flask, redirect, render_template, request, session
#for cookies setting
from flask_session import Session
#to set cookies in a temp file not in browser
from tempfile import mkdtemp
#for exception handling
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
#for password hashing and checking
from werkzeug.security import check_password_hash, generate_password_hash

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

from helpers import login_required,admin_required, apology, check_admins, check_admin_cookies


# Make sure admins are set
check_admins()

# connect engine to database
engine = create_engine("mysql+pymysql://root:sqldata@localhost/CMMS",echo = None)
# make a metadata object for DB handling
meta = MetaData()
# make a DB_cursor object for commiting
db = engine.connect()

# function to load tables used for exception handling
def reflect_table(table_name,meta_object, engine_object):
    try:
        table = Table(table_name, meta_object, autoload = True, autoload_with = engine_object)
        return table
    except SQLAlchemyError as err:
        if type(err) == sqlalchemy.exc.NoSuchTableError:
            print("ERROR: table does not exists")
            return None
        elif err.orig.args[0] == 1103:
            print("ERROR: Invalid table name")
        else:
            print("Unknown error occured")
            return None
            

# Load tables into variables
device_description = reflect_table("device_description", meta, engine)
device_essentials = reflect_table("device_essentials", meta, engine)
device_extras = reflect_table("device_extras", meta, engine)
manager_essentials = reflect_table("manager_essentials", meta, engine)
manager_extras = reflect_table("manager_extras", meta, engine)
users_man = reflect_table("users_man", meta, engine)
order_essentials = reflect_table("order_essentials", meta, engine)
order_extras = reflect_table("order_extras", meta, engine)
tech_essentials = reflect_table("tech_essentials", meta, engine)
tech_extras = reflect_table("tech_extras", meta, engine)
users_tech = reflect_table("users_tech", meta, engine)

#check for cookies
def check_cookies(user_type = "man"):
    if user_type == "man" or user_type == "manager":
        sel_command = users_man.select().where(users_man.c.username == session.get("username")).where(users_man.c.token == session.get("token"))
        sel_command = db.execute(sel_command)
        cookie = sel_command.fetchone()
        if cookie is None:
            return render_template("control/banned.html")
        return True
    if user_type == "tech" or user_type == "technician":
        sel_command = users_tech.select().where(users_tech.c.username == session.get("username")).where(users_tech.c.token == session.get("token"))
        sel_command = db.execute(sel_command)
        cookie = sel_command.fetchone()
        if cookie is None:
            return render_template("control/banned.html")
        return True


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies) (more security)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if session.get("admin") is None and session.get("token") is None:
        return render_template("control/index.html")
    elif session.get("admin"):
        check_admin_cookies()
        return render_template("control/main.html")
    elif session.get("token_tech"):
        check_cookies()
        return render_template("control/main.html")
    elif session.get("token_man"):
        check_cookies()
        return render_template("control/main.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("control/error.html",name=e.name, code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
