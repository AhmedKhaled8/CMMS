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

from helpers import login_required,admin_required, apology, check_admins, check_admin_cookies,logger


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Make sure admins are set
check_admins()

# connect engine to database
engine = create_engine("mysql+pymysql://root:sqldata@localhost/CMMS",echo = None)
# make a metadata object for DB handling
meta = MetaData()
# make a DB_cursor object for commiting
db = engine.connect()

# Load tables into variables
device_description = Table("device_description", meta, autoload = True, autoload_with = engine)
device_essentials = Table("device_essentials", meta, autoload = True, autoload_with = engine)
device_extras = Table("device_extras", meta, autoload = True, autoload_with = engine)
manager_essentials = Table("manager_essentials", meta, autoload = True, autoload_with = engine)
manager_extras = Table("manager_extras", meta, autoload = True, autoload_with = engine)
order_essentials = Table("order_essentials", meta, autoload = True, autoload_with = engine)
order_extras = Table("order_extras", meta, autoload = True, autoload_with = engine)
tech_essentials = Table("tech_essentials", meta, autoload = True, autoload_with = engine)
tech_extras = Table("tech_extras", meta, autoload = True, autoload_with = engine)

