# to get environment variables
# and to generate random hash
import os
# for date and time manipulations
# for decoration functions
from functools import wraps
# for token storage
import binascii
# for datetime manipulations
import datetime
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
from sqlalchemy.types import DATE,Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_


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
            print("ERROR: table" + table_name + " does not exists")
            return None
        elif err.orig.args[0] == 1103:
            print("ERROR: Invalid table name")
        else:
            print("Unknown error occured")
            return None
            

# Load tables into variables
manager_essentials = reflect_table("manager_essentials", meta, engine)
manager_extras = reflect_table("manager_extras", meta, engine)
users_man = reflect_table("users_man", meta, engine)

tech_essentials = reflect_table("tech_essentials", meta, engine)
tech_extras = reflect_table("tech_extras", meta, engine)
users_tech = reflect_table("users_tech", meta, engine)

device_essentials = reflect_table("device_essentials", meta, engine)
device_extras = reflect_table("device_extras", meta, engine)
device_description = reflect_table("device_description", meta, engine)

order_essentials = reflect_table("order_essentials", meta, engine)
order_extras_defib = reflect_table("order_extras_defib", meta, engine)
order_extras_ECG = reflect_table("order_extras_ECG", meta, engine)
order_extras_monitor = reflect_table("order_extras_monitor", meta, engine)
order_extras_syringe_pump = reflect_table("order_extras_syringe_pump", meta, engine)
order_extras_infusion_pump = reflect_table("order_extras_infusion_pump", meta, engine)
order_extras_blood_gas = reflect_table("order_extras_blood_gas", meta, engine)

report_install = reflect_table("report_install", meta, engine)
report_move = reflect_table("report_move", meta, engine)
report_scrap = reflect_table("report_scrap", meta, engine)

maintain_dates = reflect_table("maintain_dates", meta, engine)


# TODO remove this after debugging
"""
order_extras_defib.drop(engine)
order_extras_ECG.drop(engine)
order_extras_monitor.drop(engine)
order_extras_syringe_pump.drop(engine)
order_extras_infusion_pump.drop(engine)
order_extras_blood_gas.drop(engine)
order_essentials.drop(engine)
"""


# Global control variables
departments = ('Admissions', 'Open Cardiology', 'Radiology')
device_types = {
    "Admissions" : ["Defibrillator","ECG","Monitor","Syringe Pump", "Infusion Pump"],
    "Open Cardiology" : ["Monitor", "Defibrillator", "Syringe Pump", "Mobile Ventilator", "Blood Gas Analyzer", "Ventilator", "X-Ray"],
    "Radiology" : ["Ultrasonic", "X-Ray", "MRI", "CT", "Gamma Camera"]
    }

ppm_map = {
    "Defibrillator" : order_extras_defib,
    "ECG" : order_extras_ECG,
    "Monitor" : order_extras_monitor,
    "Syringe Pump" : order_extras_syringe_pump,
    "Infusion Pump" : order_extras_infusion_pump,
    # TODO mobile ventilator here
    "Blood Gas Analyzer" : order_extras_blood_gas    
    }

#check for cookies
def check_cookies(user_type = "man"):
    if user_type == "man" or user_type == "manager":
        sel_command = users_man.select().where(users_man.c.username
           == session.get("username")).where(users_man.c.token == session.get("token_man"))
        sel_command = db.execute(sel_command)
        cookie = sel_command.fetchone()
        if cookie is None:
            return render_template("control/banned.html")
        return 1
    if user_type == "tech" or user_type == "technician":
        sel_command = users_tech.select().where(users_tech.c.username ==
            session.get("username")).where(users_tech.c.token == session.get("token_tech")).limit(1)
        sel_command = db.execute(sel_command)
        cookie = sel_command.fetchone()
        if cookie is None:
            return render_template("control/banned.html")
        return 1

def check_department(device_code: int):
    department = session.get("department")
    
    selDevice = device_essentials.select().with_only_columns([device_essentials.c.status]
             ).where(device_essentials.c.code == device_code).limit(1)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchone()
    if rows is None:
        return apology("Invalid device code", 400)
    if rows[0] == "obselete":
        return apology("Can't control a scrapped device", 400)
    
    sel_command = device_extras.select().where(device_extras.c.d_code ==
            device_code).where(device_extras.c.department == department)
    sel_command = db.execute(sel_command)
    department = sel_command.fetchone()
    if department is None:
        return apology("Forbidden, you can't control a device not in your department", 403)
    return None

def login_man_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cookie = check_cookies("man")
        try:
            length = len(cookie)
        except:
            length = len(str(cookie))
        if length > 1:
            return cookie

        return f(*args, **kwargs)
    return decorated_function

def login_tech_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cookie = check_cookies("tech")
        try:
            length = len(cookie)
        except:
            length = len(str(cookie))
        if length > 1:
            return cookie
        
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
        return redirect('/due_orders')
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

    

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = request.form.get("username")
        passer = request.form.get("password")
        

        # Ensure username was submitted
        if not user:
            #return apology("must provide username", 403)
            print("POST login_hr")
            return render_template("control/login.html", err_user="Please provide a username.")

        # Ensure password was submitted
        elif not passer:
            #return apology("must provide password", 403)
            return render_template("control/login.html", err_pwd="Please provide a password.")
            
        
        #check if the admin is the one who signed in
        chck_admin1 = os.environ.get("admin1_user") == user and os.environ.get("admin1_pass") == passer
        chck_admin2 = os.environ.get("admin2_user") == user and os.environ.get("admin2_pass") == passer 
        chck_admin3 = os.environ.get("admin3_user") == user and os.environ.get("admin3_pass") == passer
        if chck_admin1 or chck_admin2 or chck_admin3:
            #set admin cookies
            # Forget any cookies set
            session.clear()
            session["admin"] = user
            session["password"] = passer
            return redirect("/")
        
        #return apology("invalid username and/or password", 403)
        return render_template("control/login.html", err_user_pwd="Invalid username and/or password. Please try again.")

def loginFunction(users_table,essential_table = None, user = None):
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not user:
            user = request.form.get("username")
        passer = request.form.get("password")
        
        # Ensure username was submitted
        if not user:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not passer:
            return apology("must provide password", 403)


        # Query database for username
        sel_command = users_table.select().with_only_columns([users_table.c.username,
              users_table.c.token, users_table.c.hash, users_table.c.r_code]).where(users_table.c.username == user).limit(1)
        sel_command = db.execute(sel_command)
        rows = sel_command.fetchone()
        
        # Ensure username exists and password is correct
        if rows is None:
            return apology("invalid username", 403)
        
        # compare hash
        pass_chk = check_password_hash("pbkdf2:sha256:50000$" + rows[2], passer)
        if not pass_chk:
            return apology("invalid password", 403)
        
        if not essential_table is None:
            sel_command = essential_table.select().with_only_columns(
                [essential_table.c.department]).where(essential_table.c.code == rows[3]).where(essential_table.c.status == "hired").limit(1)
            sel_command = db.execute(sel_command)
            department = sel_command.fetchone()
            if department is None:
                return apology("Your account is disabled", 403)
            department = department[0]
            
            # rows[0] is the user and rows[1] is the token
            return (rows[0],rows[1], department)
            
        # rows[0] is the user and rows[1] is the token
        return (rows[0],rows[1])

@app.route("/login_man", methods=["POST"])
def login_man():
    """Log user in"""
    
    if request.method == "POST":
       
        
        out = loginFunction(users_man,manager_essentials)
        if(len(out) > 3):
            if (out == apology("must provide username", 403)):
                return render_template("control/login.html", err_user="Please provide a username")
            elif out == apology("must provide password", 403):
                return render_template("control/login.html", err_pwd="Please provide a password")
            elif out == apology("invalid username", 403):
                return render_template("control/login.html", err_inv_user="Invalid Username")
            elif out == apology("invalid password", 403):
                return render_template("control/login.html", err_inv_pwd="Invalid Password")
            elif out == apology("Your account is disabled", 403):
                return render_template("control/login.html", disabled_acc="Your account is disabled")
            else:
                return out

        user, token, department = out
        # Forget any cookies set
        session.clear()
        # Remember which user has logged in
        session["username"] = user
        session["token_man"] = token
        session["department"] = department
        
        sel_command = maintain_dates.select()
        sel_command = db.execute(sel_command)
        rows = sel_command.fetchall()
        
        due_week = datetime.date.today() + datetime.timedelta(days = 8)
        due_serials = []
        for row in rows:
            if (due_week > row[2]):
                sel_command = device_essentials.select().where(device_essentials.c.code 
                        == row[0]).where(device_essentials.c.status == "operational").limit(1)
                sel_command = db.execute(sel_command)
                row = sel_command.fetchone()
                if row is not None:
                    due_serials.append(["Device with serial " + str(sel_command.fetchone()[1]) + " have a maintainance date " +str(row[2])])
                
    
        # Redirect user to home page
        return render_template("control/main.html", warning_msg = due_serials)

@app.route("/login_tech", methods=["POST"])
def login_tech():
    """Log user in"""
    
    if request.method == "POST":    
        
        
        out = loginFunction(users_tech,tech_essentials)
        if(len(out) > 3):
            if (out == apology("must provide username", 403)):
                return render_template("control/login.html", err_user="Please provide a username")
            elif out == apology("must provide password", 403):
                return render_template("control/login.html", err_pwd="Please provide a password")
            elif out == apology("invalid username", 403):
                return render_template("control/login.html", err_inv_user="Invalid Username")
            elif out == apology("invalid password", 403):
                return render_template("control/login.html", err_inv_pwd="Invalid Password")
            elif out == apology("Your account is disabled", 403):
                return render_template("control/login.html", disabled_acc="Your account is disabled")
            else:
                return out


        user, token, department = out
        # Forget any cookies set
        session.clear()
        # Remember which user has logged in
        session["username"] = user
        session["token_tech"] = token
        session["department"] = department
    
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

    sel_command = user_table.select().with_only_columns([user_table.c.username]
        ).where(user_table.c.username == session.get("username")).limit(1)
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
    
    department = request.form.get("department")
    
    if not request.form.get("insurance") or request.form.get("insurance")== '':
        print("\n No insurance Entered")
        insurance = 0
    else:
        insurance = request.form.get("insurance")
    # Insert essentials in table
    insert1 = essentials_table.insert().values(name = request.form.get("name"),
        department = department, insurance = insurance)
    db.execute(insert1)
    # Get the unique code of the current user
    sel_command = essentials_table.select().with_only_columns([func.max(essentials_table.c.code)]
          ).where(essentials_table.c.name == request.form.get("name")).limit(1)
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
    
    return token, user, department
    


@app.route("/add_man", methods=["GET", "POST"])
@admin_required
def add_man():
    if request.method == "GET":
        return render_template("control/register.html", departments = departments, reg_type = "man")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        out = register(users_man, manager_essentials, manager_extras, "r_code")
        if(len(out) > 3):
            return out
        return render_template("control/main.html", message = "Manager added successfully")
    
        
@app.route("/add_tech", methods=["GET", "POST"])
@admin_required
def add_tech():
    if request.method == "GET":
        return render_template("control/register.html", departments = departments, reg_type = "tech")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        out = register(users_tech, tech_essentials, tech_extras, "r_code")
        if(len(out) > 3):
            return out
        return render_template("control/main.html", message = "Technician added successfully")

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
        up_command = manager_essentials.update().where(manager_essentials.c.code 
               == request.form.get("code")).values(status = request.form.get("status"))
        db.execute(up_command)
        return render_template("control/main.html", message = "Manager removed successfully")
        
@app.route("/remove_tech", methods=["GET", "POST"])
@admin_required
def rem_tech():
    if request.method == "GET":
        return render_template("control/remove.html", rem_type = "tech")
    
    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":
        up_command = tech_essentials.update().where(tech_essentials.c.code 
            == request.form.get("code")).values(status = request.form.get("status"))
        db.execute(up_command)
        return render_template("control/main.html", message = "Technician removed successfully")

def addDevice():
    serial = request.form.get("serial")
    deviceType = request.form.get("type")
    maintain_date = request.form.get("maint_date")
    description = request.form.get("description")
    name = request.form.get("name")
    model = request.form.get("model")
    manufacturer = request.form.get("manufacturer")
    country = request.form.get("country")
    receive_date = request.form.get("receive_date")
    cost = request.form.get("cost")
    department = session.get("department")
    
    
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
    

    # Create Extra Data 
    extraDictionary = {
        'd_code': code,
        'name': name,
        'model': model,
        'manufacturer': manufacturer,
        'country': country,
        'receive_date': receive_date,
        'cost': cost,
        'department': department
    }
    
    # Insert Extra Data
    insertExtra = device_extras.insert().values(**extraDictionary)
    
    
    installDictionary = {
        'code': code,
        'receive_date': receive_date,
        'device_name': name,
        'device_type': deviceType,
        'device_serial': serial,
        'device_manufacturer': manufacturer,
        'cost': cost, 
        'department': department
    }

    insertInstall = report_install.insert().values(**installDictionary)
    
    
    maintainDictionary = {
        'device_code': code,
        'maint_date': maintain_date
        }
    
    insertMaintain = maintain_dates.insert().values(**maintainDictionary)
    
    db.execute(insertExtra)
    db.execute(insertDescription)
    db.execute(insertInstall)
    db.execute(insertMaintain)
    
    return None


@app.route("/add_device", methods=["GET", "POST"])
@login_man_required
def add_device():
    if request.method == "GET":
        return render_template("device/add_device.html", device_types = device_types[session.get("department")])
    elif request.method == "POST":
        addDevice()
        return render_template("control/main.html", message = "Device added successfully")

def removeDevice():
    reportDictionary = {}
    
    code = request.form.get("code")
    reportDictionary.update({"code" : code})
    cause = request.form.get("cause")
    reportDictionary.update({"cause" : cause})
    
    reportDictionary.update({"date" : func.cast(func.now(), DATE)})
    
    updateDevice1 = device_essentials.update().where(device_essentials.c.code == code).values(status = "obselete")
    updateDevice2 = device_extras.update().where(device_extras.c.d_code == code).values(remove_date = func.cast(func.now(), DATE))
    
    selDevice = device_essentials.select().with_only_columns([device_essentials.c.serial,
        device_essentials.c.type]).where(device_essentials.c.code == code).limit(1)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchone()
    reportDictionary.update({"device_serial" : rows[0]})
    reportDictionary.update({"device_type" : rows[1]})
    
    selDevice = device_extras.select().with_only_columns([device_extras.c.name,
          device_extras.c.manufacturer]).where(device_extras.c.d_code == code).limit(1)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchone()
    reportDictionary.update({"device_name" : rows[0]})
    reportDictionary.update({"device_manufacturer" : rows[1]})
    
    insertReport = report_scrap.insert().values(**reportDictionary)
    
    delete_maint = maintain_dates.delete().where(maintain_dates.c.device_code == code)
    
    db.execute(updateDevice1)
    db.execute(updateDevice2)
    db.execute(insertReport)
    db.execute(delete_maint)
    
    return None


@app.route("/remove_device", methods=["GET", "POST"])
@login_man_required
def remove_device():
    if request.method == "GET":
        return render_template("device/remove_device.html")
    elif request.method == "POST":
        user = session.get("username")
        code = request.form.get("code")

        out = check_department(code)
        if out is not None:
            return out
        
        out = loginFunction(users_man, user = user)
        if(len(out) > 2):
            return out
        
        removeDevice()
        return render_template("control/main.html", message = "Device removed successfully")

def moveDevice():
    reportDictionary = {}
    
    code = request.form.get("code")
    reportDictionary.update({"device_code" : code})
    move_date = request.form.get("move_date")
    reportDictionary.update({"move_date" : move_date})
    to = request.form.get("to")
    reportDictionary.update({"to_dep" : to})
    
    selDevice = device_essentials.select().with_only_columns([device_essentials.c.serial,
      device_essentials.c.type,device_essentials.c.status]).where(device_essentials.c.code == code).limit(1)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchone()
    
    reportDictionary.update({"device_serial" : rows[0]})
    reportDictionary.update({"device_type" : rows[1]})
        
    updateDevice1 = device_extras.update().where(device_extras.c.d_code == code).values(department = to)
    
    selDevice = device_extras.select().with_only_columns([device_extras.c.name, device_extras.c.manufacturer,
        device_extras.c.department]).where(device_extras.c.d_code == code).limit(1)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchone()
    reportDictionary.update({"device_name" : rows[0]})
    reportDictionary.update({"device_manufacturer" : rows[1]})
    reportDictionary.update({"from_dep" : rows[2]})
    
    insertReport = report_move.insert().values(**reportDictionary)
    
    db.execute(updateDevice1)
    db.execute(insertReport)
    
    return None

@app.route("/move_device", methods=["GET", "POST"])
@login_man_required
def move_device():
    if request.method == "GET":
        return render_template("device/move_device.html", departments = departments)
    elif request.method == "POST":
        user = session.get("username")
        code = request.form.get("code")
        
        out = check_department(code)
        if out is not None:
            return out
        
        
        out = loginFunction(users_man, user = user)
        if(len(out) > 2):
            return out
        
        out = moveDevice()
        if out is not None:
             return out
        return render_template("control/main.html", message = "Device moved successfully")


def reviewDevices(status: str = None):
    rows = []
    out = []
    if status == "operational" or status == "obselete":
        # exclude the status column
        column_list = [col for col in device_essentials.c if col.key != "status"]
        selDevice = device_essentials.select().with_only_columns(column_list).where(device_essentials.c.status == status)
    else:
        selDevice = device_essentials.select()
        
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchall()
    for index in range(0, len(rows)):
        selDevice = device_extras.select().where(device_extras.c.d_code == rows[index][0]).where(device_extras.c.department == session.get("department")).limit(1)
        selDevice = db.execute(selDevice)
        row = selDevice.fetchone()
        if row is None:
            continue
        # convert parent row to list
        rows[index] = list(rows[index])
        
        if status == "operational" or status == "obselete":
            rows[index][3] = rows[index][3].strftime('%d-%m-%Y')
        else:
            rows[index][4] = rows[index][4].strftime('%d-%m-%Y')
            
        # convert the date time into string
        row = list(row)
        row[5] = row[5].strftime('%d-%m-%Y')
        
        rows[index].extend(row)
        
        num_elements = len(rows[index]) - 1
        elements = [None]* num_elements
        elements[0] = rows[index][0]
        elements[1] = row[1]
        elements[2] = row[2]
        elements[3] = row[3]
        elements[4] = rows[index][1]
        elements[5] = row[7]
        elements[6] = row[4]
        elements[7] = rows[index][2]
        elements[8] = row[5]
        if status == "operational" or status == "obselete":
            elements[9] = rows[index][3]
            elements[10] = row[6]
            elements[11] = row[8]
        else:
            elements[9] = rows[index][4]
            elements[10] = row[6]
            elements[11] = row[8]
            elements[12] = rows[index][3]
            
        out.append(elements)
    
    return out

@app.route("/review_devices", methods=["GET"])
@login_man_required
def review_devices():
    if request.method == "GET":
        status = request.args.get("show")
        if status == "operational":
            rows = reviewDevices("operational")
            return render_template("device/review_devices.html", status = "operational", rows = rows)
        elif status == "obsolete":
            rows = reviewDevices("obselete")
            return render_template("device/review_devices.html", status = "obsolete", rows = rows)
        else:
            rows = reviewDevices("all")
            return render_template("device/review_devices.html", status = "all", rows = rows)



def nearDates():
    rows = []
    out = []
    
    column_list = [col for col in device_essentials.c if col.key != "status"]
    selDevice = device_essentials.select().with_only_columns(column_list).where(device_essentials.c.status
        == "operational").order_by(device_essentials.c.maint_date)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchall()
    for index in range(0, len(rows)):
        selDevice = device_extras.select().where(device_extras.c.d_code 
             == rows[index][0]).where(device_extras.c.department == session.get("department")).limit(1)
        selDevice = db.execute(selDevice)
        row = selDevice.fetchone()
        if row is None:
            continue
        
        # convert parent row to list
        rows[index] = list(rows[index])
        
        rows[index][3] = rows[index][3].strftime('%d-%m-%Y')
            
        # convert the date time into string
        row = list(row)
        row[5] = row[5].strftime('%d-%m-%Y')
        
        rows[index].extend(row)
        
        num_elements = len(rows[index]) - 2
        elements = [None]* num_elements
        elements[0] = rows[index][0]
        elements[1] = rows[index][3]
        elements[2] = row[1]
        elements[3] = row[2]
        elements[4] = row[3]
        elements[5] = rows[index][1]
        elements[6] = row[7]
        elements[7] = row[4]
        elements[8] = rows[index][2]
        elements[9] = row[5]
        elements[10] = row[6]
            
        out.append(elements)
        
    return out


@app.route("/near_dates", methods=["GET"])
@login_man_required
def near_dates():
    if request.method == "GET":
        rows = nearDates()
        return render_template("device/near_maint_dates.html", rows = rows)


def getTech():
    department = session.get("department")
    selectStatment = tech_essentials.select().where(and_(tech_essentials.c.department == department, tech_essentials.c.status=="hired"))
    selectedData = db.execute(selectStatment)
    code_name = []
    for tech in selectedData:
        code = tech[0]
        name = tech[1]
        code_name.append([code,name])
    return code_name


@app.route("/assign_order", methods=["GET", "POST"])
@login_man_required
def assign_order():
    if request.method == "GET":
        techs = getTech()
        return render_template("order/assign_order.html", techs = techs)
    else:
        serial = request.form.get("serial")
        place = request.form.get("place")
        tech_code = request.form.get("tech")
        
        selectStatment = device_essentials.select().where(device_essentials.c.serial == serial
              ).where(device_essentials.c.status == "operational").limit(1)
        selectStatment = db.execute(selectStatment)
        device = selectStatment.fetchone()
        
        if device is None:
            return apology("Device serial is wrong or device is scraped", 400)
        
        table = ppm_map[device[2]]
        
        insert1 = order_essentials.insert().values(serial = serial, place = place,
                type = device[2], department = session.get("department"),
                tech_code = tech_code, date_issued = func.cast(func.now(), DATE))
        try:
            db.execute(insert1)
        except sqlalchemy.exc.IntegrityError:
            print("Error duplicate enteries")
            return apology("Can't enter duplicate enteries", 403)
        
        sel_command = order_essentials.select().with_only_columns([func.max(order_essentials.c.code)]
          ).where(order_essentials.c.serial == serial).limit(1)
        sel_command = db.execute(sel_command)
        r_code = sel_command.fetchone()[0]
        
        insert2 = table.insert().values(r_code = r_code)
        db.execute(insert2)
        
        return render_template("control/main.html", message = "Order assigned successfully")
      

def reviewOrders():
    out = []
    
    selDevice = order_essentials.select()
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchall()
    
    for index in range(0, len(rows)):
        selTech = tech_essentials.select().where(tech_essentials.c.code 
             == rows[index][5]).with_only_columns([tech_essentials.c.name]).limit(1)
        selTech = db.execute(selTech)
        row = selTech.fetchone()[0]
        if row is None:
            continue
        
        # convert parent row to list
        rows[index] = list(rows[index])
        
        rows[index][6] = rows[index][6].strftime('%d-%m-%Y')
        if rows[index][7] is not None:
            rows[index][7] = rows[index][7].strftime('%d-%m-%Y')
        
        num_elements = 9
        elements = [None]* num_elements
        if rows[index][7] is None:
            elements[0] = "No"
        else:
            elements[0] = "Yes"
        elements[1] = rows[index][0]
        elements[2] = rows[index][1]
        elements[3] = rows[index][2]
        elements[4] = rows[index][3]
        elements[5] = rows[index][4]
        elements[6] = row
        elements[7] = rows[index][6]
        elements[8] = rows[index][7]
            
        out.append(elements)
        
    return out

# TODO finish these

def shortppmReport():
    out = []
        
    order_ess = order_essentials.select().where(order_essentials.c.date_responded != None).where(
        order_essentials.c.department == session.get("department"))
    order_ess = db.execute(order_ess).fetchall()
    
    for order in order_ess:
        elements = [None]*9
        extras_table = ppm_map[order[3]]
        order_ext = extras_table.select().where(extras_table.c['r_code'] == order[0]).limit(1)
        order_ext = db.execute(order_ext).fetchone()
        
        tech_name = db.execute(tech_essentials.select().with_only_columns([tech_essentials.c['name']]
         ).where(tech_essentials.c['code'] == order[5])).fetchone()[0]
        
        for value in order_ext:
            if value == "found" or value == "not found":
                print(value)
                elements[0] = "red"
                elements[2] = "Yes"
                break
        if elements[0] is None:
            elements[0] ="green"
            elements[2] = "No"
        
        elements[1] = order[0]
        elements[3] = order[1]
        elements[4] = order[2]
        elements[5] = order[3]
        elements[6] = tech_name
        elements[7] = order[6]
        elements[8] = order[7]
        out.append(elements)
    
    return out
    

@app.route("/short_ppm_report", methods=["GET"])
@login_man_required
def short_ppm_report():
    if request.method == "GET":
        rows = shortppmReport()
        return render_template("report/short_ppm_report.html", rows = rows)


def detailedppmReport():
    out = []
        
    column_list = [col for col in order_essentials.c if col.key != "department"]
    order_ess = order_essentials.select().with_only_columns(column_list).where(order_essentials.c.date_responded != None).where(
        order_essentials.c.department == session.get("department"))
    order_ess = db.execute(order_ess).fetchall()
    
    col_append = [col for col in order_essentials.c.keys() if col != "department"]
    
    for order in order_ess:
        
        extras_table = ppm_map[order[3]]
        headers = []
        values = []
        
        headers.extend(col_append)
        values.extend(order)
        
        order_ext = extras_table.select().where(extras_table.c['r_code'] == order[0]).limit(1)
        order_ext = db.execute(order_ext).fetchone()
        
        tech_name = db.execute(tech_essentials.select().with_only_columns([tech_essentials.c['name']]
         ).where(tech_essentials.c['code'] == order[4])).fetchone()[0]
        
        headers[4] = "Tech name"
        values[4] = tech_name
        
        head_order_ext = list(extras_table.c.keys())
        head_order_ext.pop(0)
        
        val_order_ext = list(order_ext)
        val_order_ext.pop(0)
        
        headers.extend(head_order_ext)
        values.extend(val_order_ext)
        """
        for value in order_ext:
            if value == "found" or value == "not found":
                print(value)
                elements[0] = "red"
                elements[2] = "Yes"
                break
        if elements[0] is None:
            elements[0] ="green"
            elements[2] = "No"
        
        elements[1] = order[0]
        elements[3] = order[1]
        elements[4] = order[2]
        elements[5] = order[3]
        elements[6] = tech_name
        elements[7] = order[6]
        elements[8] = order[7]
        out.append(elements)
        """
        out.append(list(zip(headers,values)))
    
    return out


@app.route("/detailed_ppm_report", methods=["GET"])
@login_man_required
def detailed_ppm_report():
    rows = detailedppmReport()
    if request.method == "GET":
        return render_template("report/detailed_ppm_report.html", rows = rows)

@app.route("/installing_report", methods=["GET"])
@login_man_required
def installing_report():
    if request.method == "GET":
        select_command = report_install.select()
        select_command = db.execute(select_command)
        rows = select_command.fetchall()
        
        return render_template("report/installing_report.html", rows = rows)

@app.route("/moving_report", methods=["GET"])
@login_man_required
def moving_report():
    if request.method == "GET":
        select_command = report_move.select()
        select_command = db.execute(select_command)
        rows = select_command.fetchall()
        
        return render_template("report/moving_report.html", rows = rows)

@app.route("/scraping_report", methods=["GET"])
@login_man_required
def scraping_report():
    if request.method == "GET":
        select_command = report_scrap.select()
        select_command = db.execute(select_command)
        rows = select_command.fetchall()
        
        return render_template("report/scraping_report.html", rows = rows)



@app.route("/review_orders", methods=["GET", "POST"])
@login_man_required
def review_orders():
    if request.method == "GET":
        rows = reviewOrders()
        return render_template("order/review_orders.html", rows = rows)

def dueOrders():
    tech_code = db.execute(users_tech.select().with_only_columns([users_tech.c['r_code']]
             ).where(users_tech.c['username'] == session.get("username"))).fetchone()[0]
    
    selDevice = order_essentials.select().where(order_essentials.c.tech_code == tech_code).where(
        order_essentials.c.date_responded == None)
    selDevice = db.execute(selDevice)
    rows = selDevice.fetchall()
    
    for index in range(0, len(rows)):
        # convert parent row to list
        rows[index] = list(rows[index])
        
        rows[index][6] = rows[index][6].strftime('%d-%m-%Y')
        
        rows[index].pop(5)
        # 7 is now 6
        rows[index].pop(6)
        
    return rows

@app.route("/due_orders", methods=["GET", "POST"])
@login_tech_required
def due_orders():
    if request.method == "GET":
        message = None
        if session.get("message"):
            message = session.pop("message")
        rows = dueOrders()
        return render_template("order/due_orders.html",message = message, rows = rows)


@app.route("/submit_order", methods=["GET", "POST"])
@login_tech_required
def submit_order():
    if request.method == "GET":
        order_id = request.args.get("id")
        
        rows = []
        
        # check if a wrong argument is passed
        if order_id is None:
            return apology("Invalid request", 400)
        try:
            order_id = int(order_id)
        except:
            return apology("Invalid request", 400)
        
        tech_code = db.execute(users_tech.select().with_only_columns([users_tech.c['r_code']]
             ).where(users_tech.c['username'] == session.get("username"))).fetchone()[0]
        
        selOrder = order_essentials.select().where(order_essentials.c.tech_code == tech_code).where(
        order_essentials.c.date_responded == None).where(order_essentials.c.code == order_id).limit(1)
        selOrder = db.execute(selOrder)
        order_ess = selOrder.fetchone()
        
        serial = order_ess[1]
        place = order_ess[2]
        device_type = order_ess[3]
        date_issued = order_ess[6].strftime('%d-%m-%Y')
        
        device_code = db.execute(device_essentials.select().with_only_columns([device_essentials.c['code']]
             ).where(device_essentials.c['serial'] == serial)).fetchone()[0]
        
        tech_name = db.execute(tech_essentials.select().with_only_columns([tech_essentials.c['name']]
             ).where(tech_essentials.c['code'] == order_ess[5])).fetchone()[0]

        
        if order_ess is None:
            return apology("Order not found", 404)
        
        extras_table = ppm_map[device_type]
        order_extra = extras_table.c.keys()
        
        size = len(order_extra) - 1
        for index in range(1,size):
            rows.append([order_extra[index].replace("_"," "), order_extra[index]])
        
        return render_template("order/submit_order.html", serial = serial, place = place,
                device_type = device_type, device_code = device_code, date_issued = date_issued,
                tech_name = tech_name, order_id = order_id, rows = rows)
    
    
    elif request.method == "POST":
        code = request.form.get("code")
        device_type = request.form.get("device_type")
        device_code = request.form.get("device_code")
        
        updateDictionary = {}
        
        ignored_keys = ["code","notes","device_code","device_type"]
        for key in request.form.keys():
            if key not in ignored_keys:
                updateDictionary.update({key : func.cast(1, Integer)})

        up_command = order_essentials.update().where(order_essentials.c.code 
                == code).values(date_responded = func.cast(func.now(), DATE))
        db.execute(up_command)
        
        extras_table = ppm_map[device_type]
        
        if len(updateDictionary) != 0:
            up_command = extras_table.update().where(extras_table.c.r_code == code).values(**updateDictionary)
            db.execute(up_command)
        
        up_command = maintain_dates.update().where(maintain_dates.c.device_code == device_code
               ).values(maint_date = datetime.date.today() + datetime.timedelta(days = 30))
        db.execute(up_command)
        
        session["message"] = "Order submitted successfully"
        
        return redirect("/due_orders")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("control/error.html",name=e.name, code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


