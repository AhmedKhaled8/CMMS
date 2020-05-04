# to get environment variables
# and to generate random hash
import os
# for decoration functions
from functools import wraps
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
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

from helpers import admin_required, apology, check_admins, check_admin_cookies


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

# Global control variables
departments = ('IC', 'cardiac', 'operations')

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
        sel_command = users_tech.select().where(users_tech.c.username == session.get("username")).where(users_tech.c.token == session.get("token")).limit(1)
        sel_command = db.execute(sel_command)
        cookie = sel_command.fetchone()
        if cookie is None:
            return render_template("control/banned.html")
        return True

def login_man_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        check_cookies("man")
        return f(*args, **kwargs)
    return decorated_function

def login_tech_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        check_cookies("tech")
        return f(*args, **kwargs)
    return decorated_function

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
    if session.get("admin") is None and session.get("token_tech") is None and session.get("token_man") is None:
        return render_template("control/index.html")
    elif session.get("admin"):
        check_admin_cookies()
        return render_template("control/main.html")
    elif session.get("token_tech"):
        check_cookies("tech")
        return render_template("control/main.html")
    elif session.get("token_man"):
        check_cookies("man")
        return render_template("control/main.html")

@app.route("/set_log_man", methods = ["POST"])
def set_log_man():
    if request.method == "POST":
        session.clear()
        session['log_man'] = True
        return redirect("/login")

@app.route("/set_log_tech", methods = ["POST"])
def set_log_tech():
    if request.method == "POST":
        session.clear()
        session['log_tech'] = True
        return redirect("/login")
    
@app.route("/set_log_hr", methods = ["POST"])
def set_log_hr():
    if request.method == "POST":
        session.clear()
        session['log_hr'] = True
        return redirect("/login")

@app.route("/login", methods=["GET"])
def login():
    """Log user in"""
    if request.method == "GET":
        return render_template("control/login.html")


@app.route("/login_hr", methods=["POST"])
def login_hr():
    """Log user in"""

    # Forget any cookies set
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = request.form.get("username")
        passer = request.form.get("password")

        # Ensure username was submitted
        if not user:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not passer:
            return apology("must provide password", 403)
            
        
        #check if the admin is the one who signed in
        chck_admin1 = os.environ.get("admin1_user") == user and os.environ.get("admin1_pass") == passer
        chck_admin2 = os.environ.get("admin2_user") == user and os.environ.get("admin2_pass") == passer 
        chck_admin3 = os.environ.get("admin3_user") == user and os.environ.get("admin3_pass") == passer
        if chck_admin1 or chck_admin2 or chck_admin3:
            #set admin cookies
            session["admin"] = user
            session["password"] = passer
            return redirect("/")
        
        return apology("invalid username and/or password", 403)


@app.route("/login_man", methods=["POST"])
def login_man():
    """Log user in"""

    # Forget any cookies set
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = request.form.get("username")
        passer = request.form.get("password")
        
        # Ensure username was submitted
        if not user:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not passer:
            return apology("must provide password", 403)


        # Query database for username
        sel_command = users_man.select().with_only_columns([users_man.c.username, users_man.c.token, users_man.c.hash]).where(users_man.c.username == user).limit(1)
        sel_command = db.execute(sel_command)
        rows = sel_command.fetchone()
        
        
        # Ensure username exists and password is correct
        if rows is None:
            return apology("invalid username", 403)
        
        print(passer)
        print(rows[2])
        
        # compare hash
        pass_chk = check_password_hash("pbkdf2:sha256:50000$" + rows[2], passer)
        if not pass_chk:
            return apology("invalid password", 403)
        # Remember which user has logged in
        session["token_man"] = rows[1]
        session["username"] = rows[0]

        # Redirect user to home page
        return redirect("/")

@app.route("/login_tech", methods=["POST"])
def login_tech():
    """Log user in"""

    # Forget any cookies set
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = request.form.get("username")
        passer = request.form.get("password")

        # Ensure username was submitted
        if not user:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not passer:
            return apology("must provide password", 403)


        # Query database for username
        sel_command = users_tech.select().with_only_columns([users_tech.c.username, users_tech.c.token, users_tech.c.hash]).where(users_tech.c.username == session.get("username")).limit(1)
        sel_command = db.execute(sel_command)
        rows = sel_command.fetchone()
        

        # Ensure username exists and password is correct
        if rows is None:
            return apology("invalid username and/or password", 403)
        

        # compare hash
        pass_chk = check_password_hash("pbkdf2:sha256:50000$" + rows[2], passer)
        if not pass_chk:
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["token_tech"] = rows[1]
        session["username"] = rows[0]

        # Redirect user to home page
        return redirect("/")


def register(user_table, essentials_table, extras_table, reference_name):
    """Register user"""
    user = request.form.get("username")
    # Ensure username was submitted
    if not user:
        return apology("must provide username", 400)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confirmation was submitted
    elif not request.form.get("confirmation"):
        return apology("must provide confirmation", 400)

    # Check whether the password and confirmation match
    elif request.form.get("password") != request.form.get("confirmation"):
        return apology("password and confirmation do not match", 400)

    sel_command = user_table.select().with_only_columns([user_table.c.username]).where(user_table.c.username == session.get("username")).limit(1)
    sel_command = db.execute(sel_command)
    rows = sel_command.fetchone()
    
    if rows:
        return apology("Username already exists", 400)

    hasher = generate_password_hash(request.form.get("password"),  method = 'pbkdf2:sha256:50000', salt_length=8)
    
    
    # Strip hash from extra characters
    # Extra characters are "pbkdf2:sha256:50000$"
    hasher = hasher[20:]
    
    # Make a random number for token
    token = binascii.hexlify(os.urandom(16))
    token = token.decode("utf-8")
    
    
    if not request.form.get("insurance") or request.form.get("insurance")== '':
        print("\n No insurance Entered")
        insurance = 0
    else:
        insurance = request.form.get("insurance")
    # Insert essentials in table
    insert1 = essentials_table.insert().values(name = request.form.get("name"), insurance = insurance)
    db.execute(insert1)
    # Get the unique code of the current user
    sel_command = essentials_table.select().with_only_columns([func.max(essentials_table.c.code)]).where(essentials_table.c.name == request.form.get("name")).limit(1)
    sel_command = db.execute(sel_command)
    code = sel_command.fetchone()[0]
    
    dictionary = {reference_name : code}
    
    # Insert extras in table
    insert2 = extras_table.insert().values(**dictionary, SSN = request.form.get("SSN"),
    sex = request.form.get("sex"), phone = request.form.get("phone"), bdate = request.form.get("bdate"),
    street = request.form.get("street"), province = request.form.get("province"))
    
    # Insert new user credentials
    insert3 = user_table.insert().values(username = user, hash = hasher, token = token, email = request.form.get("email"), **dictionary)
    
    # commit changes in database
    db.execute(insert2)
    db.execute(insert3)
    
    return token, user
    


@app.route("/add_man", methods=["GET", "POST"])
@admin_required
def add_man():
    if request.method == "GET":
        return render_template("control/register.html", reg_type = "man")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        token, user = register(users_man, manager_essentials, manager_extras, "m_code")
        # automatically login
        session["token_man"] = token
        session["username"] = user
        return redirect("/")
        
@app.route("/add_tech", methods=["GET", "POST"])
@admin_required
def add_tech():
    if request.method == "GET":
        return render_template("control/register.html", reg_type = "tech")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        token, user = register(users_tech, tech_essentials, tech_extras, "t_code")
        # automatically login
        session["token_tech"] = token
        session["username"] = user
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


@app.route("/remove_man", methods=["GET", "POST"])
@admin_required
def rem_man():
    if request.method == "GET":
        return render_template("control/remove.html", rem_type = "man")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        up_command = manager_essentials.update().where(manager_essentials.c.code == request.form.get("code")).values(status = request.form.get("status"))
        db.execute(up_command)
        return redirect("/")
        
@app.route("/remove_tech", methods=["GET", "POST"])
@admin_required
def rem_tech():
    if request.method == "GET":
        return render_template("control/remove.html", rem_type = "tech")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        up_command = tech_essentials.update().where(tech_essentials.c.code == request.form.get("code")).values(status = request.form.get("status"))
        db.execute(up_command)
        return redirect("/")

def addDevice():
    serial = request.form.get("serial")
    deviceType = request.form.get("type")
    maintain_date = request.form.get("maint_date")
    description = request.form.get("description")
    name = request.form.get("name")
    model = request.form.get("model")
    manufacturer = request.form.get("manufacturer")
    country = request.form.get("country")
    recieve_date = request.form.get("recieve_date")
    cost = request.form.get("cost")
    department = request.form.get("department")
    
    print(maintain_date)
    
    # Create the Essential Data
    essentialDictionary = {
        'serial': serial,
        'type': deviceType,
        'maint_date': maintain_date
    }
    
    # Inserting Essential Data to device_essentials Table
    insertEssential = device_essentials.insert().values(**essentialDictionary)
    db.execute(insertEssential)

    # Get the Code of the Recently Registed Data
    selectEssential = device_essentials.select().where(device_essentials.c.serial == serial)
    selectedData = db.execute(selectEssential)
    code = selectedData.fetchone()[0]
    
    # Create Description Data
    descriptionDictionary = {
        'd_code': code,
        'description': description
    }

    # Inserting Description Data
    insertDescription = device_description.insert().values(**descriptionDictionary)
    db.execute(insertDescription)

    # Create Extra Data 
    extraDictionary = {
        'd_code': code,
        'name': name,
        'model': model,
        'manufacturer': manufacturer,
        'country': country,
        #'receive_date': datetime.datetime.strptime(recieve_date, dateFormat),
        'receive_date': recieve_date,
        'cost': cost,
        'department': department
    }
    
    # Insert Extra Data
    insertExtra = device_extras.insert().values(**extraDictionary)
    db.execute(insertExtra)


@app.route("/add_device", methods=["GET", "POST"])
@login_man_required
def add_device():
    if request.method == "GET":
        return render_template("device/add_device.html", departments = departments)
    elif request.method == "POST":
        addDevice()
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("control/error.html",name=e.name, code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
