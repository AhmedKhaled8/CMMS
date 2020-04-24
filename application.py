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


#for connecting and executing queries
import mysql.connector
#for SQL error handling
from mysql.connector import errorcode

#login_required & admin_required decorators, error page, and check_admins

#if the normal import function is not executed in some python interpreters,
#use exec function instead
from helpers import login_required,admin_required, apology, check_admins, check_admin_cookies,logger
#exec(open(os.environ.get("lab_exec")+"/helpers.py").read())

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#set db as global variable
db = None
#Load database at first request
# Make sure admins are set
check_admins()

DB_NAME= "Labs"

try:
    cnx = mysql.connector.connect(user='root',password="sqldata",host='127.0.0.1',charset='utf8mb4')
    db = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    else:
        print(err)
	
try:
    db.execute("USE {}".format(DB_NAME))
    print("Database in use")
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    print(err)


#check for cookies
def check_cookies():
    db.execute("SELECT * FROM users WHERE username = '{username}' AND token = '{token}' LIMIT 1"
               .format(username = session.get("username"),token = session.get("token")))
    cookie = db.fetchone()
    if cookie is None:
        return render_template("control/banned.html")
    return True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if session.get("admin") is None and session.get("token") is None:
        return render_template("control/index_none.html")
    elif session.get("admin"):
        check_admin_cookies()
        return render_template("control/index_admin.html")
    elif session.get("token"):
        check_cookies()
        return render_template("control/index_user.html")

@app.route("/admin")
@admin_required
def admin_index():
    check_admin_cookies()
    return render_template("control/index_admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
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

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = '{username}' LIMIT 1".format(username=user))
        rows = db.fetchone()

        # Ensure username exists and password is correct
        if rows is None:
            return apology("invalid username and/or password", 403)

        pass_chk = check_password_hash("pbkdf2:sha256:150000$" + rows[2], passer)
        if not pass_chk:
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["token"] = rows[3]
        session["username"] = rows[1]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("control/login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("control/register.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

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
        
        #check if the registered match one of the admins
        chck_admin = os.environ.get("admin1_user") == user or os.environ.get("admin2_user") == user or os.environ.get("admin3_user") == user
        
        if chck_admin:
            return apology("Username already exists", 400)
        
        db.execute("SELECT username FROM users WHERE username = '{username}' LIMIT 1;".format(username=user))
        rows = db.fetchone()
        
        if rows:
            return apology("Username already exists", 400)

        hasher = generate_password_hash(request.form.get("password"))
        # Strip hash from extra characters
        # Extra characters are "pbkdf2:sha256:150000$"
        hasher = hasher[21:]
        
        # Make a random number for token
        token = binascii.hexlify(os.urandom(16))
        token = token.decode("utf-8")
        
        
        if not request.form.get("insurance") or request.form.get("insurance")== '':
            print("\n No insurance Entered")
            # Insert essentials in table
            db.execute("insert into patient_essentials (name) values ('{name}');".format(name = request.form.get("name")))
            # Get the unique code of the current user
            db.execute("SELECT max(code) FROM patient_essentials where name = '{name}';".format(name = request.form.get("name")))
            code = db.fetchone()[0]
            # Insert extras in table
            db.execute("insert into patient_extras (p_code, SSN, sex, phone, bdate, blood_type, street, province)"
                       "values ('{coder}', '{SSN}', '{sex}', '{phone}', '{bdate}', '{blood_type}', '{street}', '{province}')".format(coder = code, SSN = request.form.get("SSN"), sex = request.form.get("sex"), phone = request.form.get("phone"), bdate = request.form.get("bdate"), blood_type = request.form.get("blood_type"), street = request.form.get("street"), province = request.form.get("province")))
            
            #Log operation
            logger(db,'register','user',code,'add')
        # Of the patient inserted insurance ID
        else:
            print("\n insurance EXIST")
            # Insert essentials in table
            db.execute("insert into patient_essentials (name, insurance) values ('{name}', '{insurance}');".format(name = request.form.get("name"), insurance = request.form.get("insurance")))
            # Get the unique code of the current user
            db.execute("SELECT max(code) FROM patient_essentials where name = '{name}';".format(name = request.form.get("name")))
            code = db.fetchone()[0]
            # Insert extras in table
            db.execute("insert into patient_extras (p_code, SSN, sex, phone, bdate, blood_type, street, province)"
                       "values ('{coder}', '{SSN}', '{sex}', '{phone}', '{bdate}', '{blood_type}', '{street}', '{province}')".format(coder = code, SSN = request.form.get("SSN"),
                       sex = request.form.get("sex"), phone = request.form.get("phone"), bdate = request.form.get("bdate"), blood_type = request.form.get("blood_type"), street = request.form.get("street"), province = request.form.get("province")))
            # Log operation
            logger(db, 'register','user',code,'add')

        # Insert new user credentials
        db.execute("insert into users (username, hash, token, email, p_code) values ('{username}', '{hashed}', '{token}', '{email}', '{coder}')".format(username = user, hashed=hasher, token = token, email = request.form.get("email"), coder = code))
        
        
        cnx.commit()
        
        # automatically login
        session["token"] = token
        session["username"] = user
        return redirect("/")



@app.route("/patient_access", methods=["GET", "POST"])
@admin_required
def pat_acc():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("patient/patient_access.html")
	
    if request.method == "POST":
        # Make row list to include data of patient
        row = [None] * 9
        db.execute("SELECT * FROM patient_essentials WHERE name = '{name}' LIMIT 1".format(name = request.form.get("name")))
        ret = db.fetchone()
        if ret is None:
            return apology("Name not found", 404)
        # Make code hold the code of patient
        code = ret[0]
        # Assign name to first element
        row[0] = ret[1]
        # Assign insurance ID
        row[5] = ret[2]
        # If the insurance is zero return none as the value
        if (row[5] == 0):
            row[5] = 'None'
        
        # Start a new select statement
        db.execute("SELECT * FROM patient_extras WHERE p_code = '{coder}' LIMIT 1".format(coder = code))
        ret = db.fetchone()
        # Assign SSN
        row[1] = ret[1]
        # Assign sex
        row[2] = ret[2]
        # Assign phone
        row[4] = ret[3]
        # Assign birth date
        row[3] = ret[4]
        # Assign blood type
        row[6] = ret[5]
        # Assign street address
        row[7] = ret[6]
        # Assign province
        row[8] = ret[7]
        return render_template("patient/patient_accessed.html", row = row)


@app.route("/devices")
@admin_required
def device():
    check_admin_cookies()
    return render_template("device/devices.html")


@app.route("/add_device", methods=["GET", "POST"])
@admin_required
def add_device():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("device/add_device.html")
    
    if request.method == "POST":
        db.execute("insert into device_essentials (serial, type, maint_date) values ('{serial}', '{typer}', '{maint_date}');".format(serial = request.form.get("serial"), typer = request.form.get("type"), maint_date = request.form.get("maint_date")))
        # Get the unique code of the current device
        db.execute("SELECT max(code) FROM device_essentials where serial = '{serial}';".format(serial = request.form.get("serial")))
        code = db.fetchone()[0]
        # Insert extras in table
        db.execute("insert into device_extras (d_code, name, model, manufacturer, country, receive_date, cost)"
                   "values ('{coder}', '{name}', '{model}', '{manufacturer}', '{country}', '{receive_date}', '{cost}')".format(coder = code, name = request.form.get("name"), model = request.form.get("model"), manufacturer = request.form.get("manufacturer"), country = request.form.get("country"), receive_date = request.form.get("receive_date"), cost = request.form.get("cost")))
        # Insert description
        db.execute("insert into device_description (d_code, description) values ('{coder}', '{description}')".format(coder = code, description = request.form.get("description")))
        # Insert log operation
        logger(db,session.get("admin"),'device',code,'add')
        # commit insertions
        cnx.commit()
        return redirect("/")


@app.route("/view_devices")
@admin_required
def view_device():
    check_admin_cookies()
    if request.method == "GET":
        # Make row list to include data of patient
        rows = []
        db.execute("SELECT * FROM device_essentials INNER JOIN device_extras ON code = d_code")
        rets = db.fetchall()
        for ret in rets:
            app = [None] * 10
            # Assign code to first element
            app[0] = ret[0]
            # Assign serial
            app[4] = ret[1]
            # Assign Type
            app[6] = ret[2]
            # Assign Maintainance date
            app[8] = ret[3]
            # Assign name
            app[1] = ret[5]
            # Assign model
            app[2] = ret[6]
            # Assign manufacturer
            app[3] = ret[7]
            # Assign country
            app[5] = ret[8]
            # Assign recieve date
            app[7] = ret[9]
            # Assign cost
            app[9] = ret[10]
            # append to row
            rows.append(app)
            
        
        return render_template("device/view_devices.html", rows = rows)


@app.route("/modify_device", methods=["GET", "POST"])
@admin_required
def mod_device():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("device/modify_devices.html")
    
    if request.method == "POST":
        # Make sure the device exist
        db.execute("SELECT code FROM device_essentials WHERE code = '{code}';".format(code = request.form.get("code")))
        code = db.fetchone()
        if code is None:
            return apology("No devices found", 404)
        code = code[0]
        # Update modify date
        db.execute("UPDATE device_essentials SET maint_date = '{date}' WHERE code = '{coder}';".format(date = request.form.get("maint_date"), coder = code))
        # Insert log operation
        logger(db,session.get("admin"),'device',code,'modify')
        # commit insertions
        cnx.commit()
        return redirect("/")



@app.route("/delete_device", methods=["GET", "POST"])
@admin_required
def del_device():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("device/delete_device.html")
    
    if request.method == "POST":
        user = session.get("admin")
        passer = request.form.get("password")
        # Ensure password was submitted
        if not passer:
            return apology("must provide password", 403)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        # Check whether the password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)
        #check if the admin is the one who signed in
        chck_admin1 = os.environ.get("admin1_user") == user and os.environ.get("admin1_pass") == passer
        chck_admin2 = os.environ.get("admin2_user") == user and os.environ.get("admin2_pass") == passer
        chck_admin3 = os.environ.get("admin3_user") == user and os.environ.get("admin3_pass") == passer
        if chck_admin1 or chck_admin2 or chck_admin3:
            # Make sure the device exist
            db.execute("SELECT code FROM device_essentials WHERE code = '{code}';".format(code = request.form.get("code")))
            code = db.fetchone()
            if code is None:
                return apology("No devices found", 404)
            code = code[0]
            # Delete device
            db.execute("DELETE FROM device_essentials WHERE code = '{coder}';".format(coder = code))
            # Insert log operation
            logger(db, user, 'device', code, 'delete')
            # commit insertions
            cnx.commit()
            return redirect("/")
        return apology("Wrong Credentials", 400)



@app.route("/analytics")
@admin_required
def analytic():
    check_admin_cookies()
    return render_template("analytic/analytic.html")


@app.route("/add_analytic", methods=["GET", "POST"])
@admin_required
def add_analytic():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("analytic/add_analytic.html")
    
    if request.method == "POST":
        db.execute("insert into analytics (name,SSN,sex,bdate,position,street,province,exp_years,salary,phone,join_date)"
                   "values ('{name}', '{SSN}', '{sex}','{bdate}','{position}','{street}','{province}','{exp_years}','{salary}','{phone}','{join_date}');".format(name = request.form.get("name"), SSN = request.form.get("SSN"), sex = request.form.get("sex"), bdate = request.form.get("bdate"), position = request.form.get("position"), street = request.form.get("street"), province = request.form.get("province"), exp_years = request.form.get("exp_years"), salary = request.form.get("salary"), phone = request.form.get("phone"), join_date = request.form.get("join_date")))
        # Get the unique code of the current device
        db.execute("SELECT max(code) FROM analytics where name = '{name}';".format(name = request.form.get("name")))
        code = db.fetchone()[0]
        # Insert extras in table
        db.execute("insert into a_qualifications (a_code, qualification)"
                   "values ('{coder}', '{qual}');".format(coder = code, qual = request.form.get("qualification")))
        # Insert log operation
        logger(db,session.get("admin"),'analytic',code,'add')
        # commit insertions
        cnx.commit()
        return redirect("/")


@app.route("/view_analytics")
@admin_required
def view_analytic():
    check_admin_cookies()
    if request.method == "GET":
        # Make row list to include data of patient
        rows = []
        db.execute("SELECT * FROM analytics INNER JOIN a_qualifications ON code = a_code")
        rets = db.fetchall()
        for ret in rets:
            app = [None] * 14
            # Assign ID to first element
            app[0] = ret[0]
            # Assign name
            app[2] = ret[1]
            # Assign SSN
            app[1] = ret[2]
            # Assign sex
            app[3] = ret[3]
            # Assign birth date
            app[4] = ret[4]
            # Assign position
            app[5] = ret[5]
            # Assign street
            app[10] = ret[6]
            # Assign province
            app[11] = ret[7]
            # Assign experience years
            app[7] = ret[8]
            # Assign Salary
            app[6] = ret[9]
            # Assign Phone
            app[12] = ret[10]
            # Assign join date
            app[8] = ret[11]
            # Assign retirement date
            app[9] = ret[12]
            # Assign qualification
            app[13] = ret[14]
            # append to row
            rows.append(app)
        
        return render_template("analytic/view_analytic.html", rows = rows)
    return apology("Not set", 400)


@app.route("/modify_analytic", methods=["GET", "POST"])
@admin_required
def mod_analytic():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("analytic/modify_analytic.html")
    
    if request.method == "POST":
        code = request.form.get("code")
        salary = request.form.get("salary")
        position = request.form.get("position")
        street = request.form.get("street")
        province = request.form.get("province")
        exp_years = request.form.get("exp_years")
        phone = request.form.get("phone")
        retirement_date = request.form.get("retirement_date")
        qualification = request.form.get("qualification")
        
        string = ""
        
        if code == "":
            return apology("Must enter code", 403)
            
        if salary == "":
            string = ""
        else:
            if string != "":
                string += ", "
            string = "salary =" + "'" + salary + "'"
            
        if position == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "position =" + "'" + position + "'"
            
        if street == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string +="street =" + "'" + street + "'"
            
        if province == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "province =" + "'" + province  + "'"
            
        if exp_years == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "exp_years =" + "'" + exp_years + "'"
            
        if phone == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "phone =" + "'" + phone + "'"
            
        if retirement_date == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "retirement_date =" + "'" + retirement_date + "'"
            
        
        
        logged = False
        if string != "":    
            db.execute("UPDATE analytics SET " + string + " WHERE code = '{coder}';".format(coder = code))
            logged = True
        
        if qualification != "":
            db.execute("UPDATE a_qualifications SET qualification = '{qual}' WHERE a_code = '{coder}';".format(qual = qualification, coder = code))
            logged = True
        
        if logged == True:
            logger(db,session.get("admin"),'analytic',code,'modify')
        
        cnx.commit()
            
        return redirect("/")



@app.route("/delete_analytic", methods=["GET", "POST"])
@admin_required
def del_analytic():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("analytic/delete_analytic.html")
    
    if request.method == "POST":
        user = session.get("admin")
        passer = request.form.get("password")
        # Ensure password was submitted
        if not passer:
            return apology("must provide password", 403)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        # Check whether the password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)
        #check if the admin is the one who signed in
        chck_admin1 = os.environ.get("admin1_user") == user and os.environ.get("admin1_pass") == passer
        chck_admin2 = os.environ.get("admin2_user") == user and os.environ.get("admin2_pass") == passer
        chck_admin3 = os.environ.get("admin3_user") == user and os.environ.get("admin3_pass") == passer
        if chck_admin1 or chck_admin2 or chck_admin3:
            # Make sure the analytic exist
            db.execute("SELECT code FROM analytics WHERE code = '{code}';".format(code = request.form.get("code")))
            code = db.fetchone()
            if code is None:
                return apology("No analytics found", 404)
            code = code[0]
            # Delete analytic
            db.execute("DELETE FROM analytics WHERE code = '{coder}';".format(coder = code))
            # Insert log operation
            logger(db, user, 'analytic', code, 'delete')
            # commit insertions
            cnx.commit()
            return redirect("/")
        return apology("Wrong Credentials", 400)



@app.route("/staff")
@admin_required
def staff():
    check_admin_cookies()
    return render_template("staff/staff.html")


@app.route("/add_staff", methods=["GET", "POST"])
@admin_required
def add_staff():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("staff/add_staff.html")
    
    if request.method == "POST":
        db.execute("insert into staff (name,SSN,sex,bdate,role,street,province,exp_years,salary,phone,join_date)"
                   "values ('{name}', '{SSN}', '{sex}','{bdate}','{role}','{street}','{province}','{exp_years}','{salary}','{phone}','{join_date}');".format(name = request.form.get("name"), SSN = request.form.get("SSN"), sex = request.form.get("sex"), bdate = request.form.get("bdate"), role = request.form.get("role"), street = request.form.get("street"), province = request.form.get("province"), exp_years = request.form.get("exp_years"), salary = request.form.get("salary"), phone = request.form.get("phone"), join_date = request.form.get("join_date")))
        # Get the unique code of the current staff
        db.execute("SELECT max(code) FROM staff where name = '{name}';".format(name = request.form.get("name")))
        code = db.fetchone()[0]
        # Insert extras in table
        db.execute("insert into s_qualifications (s_code, qualification)"
                   "values ('{coder}', '{qual}');".format(coder = code, qual = request.form.get("qualification")))
        # Insert log operation
        logger(db,session.get("admin"),'staff',code,'add')
        # commit insertions
        cnx.commit()
        return redirect("/")


@app.route("/view_staff")
@admin_required
def view_staff():
    check_admin_cookies()
    if request.method == "GET":
        # Make row list to include data of patient
        rows = []
        db.execute("SELECT * FROM staff INNER JOIN s_qualifications ON code = s_code")
        rets = db.fetchall()
        for ret in rets:
            app = [None] * 14
            # Assign ID to first element
            app[0] = ret[0]
            # Assign name
            app[2] = ret[1]
            # Assign SSN
            app[1] = ret[2]
            # Assign sex
            app[3] = ret[3]
            # Assign birth date
            app[4] = ret[4]
            # Assign role
            app[5] = ret[5]
            # Assign street
            app[10] = ret[6]
            # Assign province
            app[11] = ret[7]
            # Assign experience years
            app[7] = ret[8]
            # Assign Salary
            app[6] = ret[9]
            # Assign Phone
            app[12] = ret[10]
            # Assign join date
            app[8] = ret[11]
            # Assign retirement date
            app[9] = ret[12]
            # Assign qualification
            app[13] = ret[14]
            # append to row
            rows.append(app)
        
        return render_template("staff/view_staff.html", rows = rows)
    return apology("Not set", 400)



@app.route("/modify_staff", methods=["GET", "POST"])
@admin_required
def mod_staff():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("staff/modify_staff.html")
    
    if request.method == "POST":
        code = request.form.get("code")
        salary = request.form.get("salary")
        role = request.form.get("role")
        street = request.form.get("street")
        province = request.form.get("province")
        exp_years = request.form.get("exp_years")
        phone = request.form.get("phone")
        retirement_date = request.form.get("retirement_date")
        qualification = request.form.get("qualification")
        
        string = ""
        
        if code == "":
            return apology("Must enter code", 403)
            
        if salary == "":
            string = ""
        else:
            if string != "":
                string += ", "
            string = "salary =" + "'" + salary + "'"
            
        if role == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "role =" + "'" + role + "'"
            
        if street == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string +="street =" + "'" + street + "'"
            
        if province == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "province =" + "'" + province  + "'"
            
        if exp_years == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "exp_years =" + "'" + exp_years + "'"
            
        if phone == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "phone =" + "'" + phone + "'"
            
        if retirement_date == "":
            string += ""
        else:
            if string != "":
                string += ", "
            string += "retirement_date =" + "'" + retirement_date + "'"
            
        
        
        logged = False
        if string != "":    
            db.execute("UPDATE staff SET " + string + " WHERE code = '{coder}';".format(coder = code))
            logged = True
        
        if qualification != "":
            db.execute("UPDATE s_qualifications SET qualification = '{qual}' WHERE a_code = '{coder}';".format(qual = qualification, coder = code))
            logged = True
        
        if logged == True:
            logger(db,session.get("admin"),'staff',code,'modify')
        
        cnx.commit()
            
        return redirect("/")


@app.route("/delete_staff", methods=["GET", "POST"])
@admin_required
def del_staff():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("staff/delete_staff.html")
    
    if request.method == "POST":
        user = session.get("admin")
        passer = request.form.get("password")
        # Ensure password was submitted
        if not passer:
            return apology("must provide password", 403)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        # Check whether the password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)
        #check if the admin is the one who signed in
        chck_admin1 = os.environ.get("admin1_user") == user and os.environ.get("admin1_pass") == passer
        chck_admin2 = os.environ.get("admin2_user") == user and os.environ.get("admin2_pass") == passer
        chck_admin3 = os.environ.get("admin3_user") == user and os.environ.get("admin3_pass") == passer
        if chck_admin1 or chck_admin2 or chck_admin3:
            # Make sure the staff exist
            db.execute("SELECT code FROM staff WHERE code = '{code}';".format(code = request.form.get("code")))
            code = db.fetchone()
            if code is None:
                return apology("No staff found", 404)
            code = code[0]
            # Delete staff
            db.execute("DELETE FROM staff WHERE code = '{coder}';".format(coder = code))
            # Insert log operation
            logger(db, user, 'staff', code, 'delete')
            # commit insertions
            cnx.commit()
            return redirect("/")
        return apology("Wrong Credentials", 400)


# Dependents can be an improvement in next versions
'''
@app.route("/depend")
@admin_required
def depend():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_depend")
@admin_required
def view_depend():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)

@app.route("/add_depend", methods=["GET", "POST"])
@admin_required
def add_depend():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/delete_depend", methods=["GET", "POST"])
@admin_required
def del_depend():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)
'''
# Dependents part done


# Schedule can be an improvement in next versions
'''
@app.route("/schedule")
@admin_required
def schedule():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)
'''

@app.route("/tests")
@admin_required
def tests():
    check_admin_cookies()
    return render_template("tests/test.html")


@app.route("/view_tests")
@admin_required
def view_tests():
    check_admin_cookies()
    db.execute("SELECT * FROM tests  ORDER BY code")
    rows = db.fetchall()
    return render_template("tests/view_tests.html", rows = rows)


@app.route("/add_result", methods=["GET", "POST"])
@admin_required
def add_result():
    check_admin_cookies()
    if request.method == "GET":
        return render_template("tests/add_result.html")
    
    if request.method == "POST":
        # Update modify date
        db.execute("UPDATE tests SET deliver_date = NOW(), results = '{result}' WHERE code = '{coder}';".format(result = request.form.get("result"), coder = request.form.get("code")))
        # Insert log operation
        logger(db,session.get("admin"),'test',request.form.get("code"),'modify')
        # commit insertions
        cnx.commit()
        return redirect("/")

# medical condition can be an improvement in next versions
'''
@app.route("/add_medcon", methods=["GET", "POST"])
@admin_required
def add_medcon():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)
'''

@app.route("/log")
@admin_required
def log():
    check_admin_cookies()
    db.execute("SELECT * FROM log")
    rows = db.fetchall()
    return render_template("control/log.html", rows = rows)
    

@app.route("/book_test", methods=["GET", "POST"])
@login_required
def book_test():
    check_cookies()
    if request.method == "GET":
        return render_template("user/book_test.html")
    
    if request.method == "POST":
        test = request.form.get("test")
        date = request.form.get("date")
        db.execute("SELECT code FROM users WHERE token = '{token}' LIMIT 1"
               .format(token = session.get("token")))
        code = db.fetchone()[0]
        
        # ensure the test is registered once for a current patient and a current date
        try:
            db.execute("INSERT INTO tests (p_code, t_type, start_date)"
                   "values ('{coder}', '{test}', '{date}');".format(coder = code, test = test, date = date))
            db.execute("SELECT max(code) FROM tests where p_code = '{coder}';".format(coder = code))
            test_code = db.fetchone()[0]
            # Insert log operation
            logger(db,'user: ' + str(session.get("username")),'test',test_code,'add')
            
            cnx.commit()
            
            return redirect("/")
            
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return apology("Already registered this test on that date", 400)
            else:
                return apology("Unknown error happened", 400)
        

@app.route("/results")
@login_required
def results():
    check_cookies()
    db.execute("SELECT code FROM users WHERE token = '{token}' LIMIT 1"
               .format(token = session.get("token")))
    code = db.fetchone()[0]
    db.execute("SELECT code, t_type, start_date, deliver_date, results FROM tests WHERE p_code = '{coder}'  ORDER BY code".format(coder = code))
    rows = db.fetchall()
    return render_template("user/result.html", rows = rows)
    


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",name=e.name, code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
