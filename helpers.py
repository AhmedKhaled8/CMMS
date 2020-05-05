import os

from flask import redirect, session,render_template
from functools import wraps

def apology(name,code):
    print("Apology raised")
    return render_template("control/error.html",name=name, code=code)
    

def admin_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (session.get("admin") is None) or (session.get("password") is None):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_admin_cookies():
    user = os.environ.get("admin1_user") == session.get("admin") or os.environ.get("admin2_user") == session.get("admin") or os.environ.get("admin3_user") == session.get("admin")
    passer = os.environ.get("admin1_pass") == session.get("password") or os.environ.get("admin2_pass") == session.get("password") or os.environ.get("admin3_pass") == session.get("password")
    if user and passer:
        return True
    return render_template("control/banned.html")

def check_admins():
    if not os.environ.get("admin1_user"):
        raise RuntimeError("admin1_user not set")
        exit(1)
    if not os.environ.get("admin1_pass"):
        raise RuntimeError("admin1_pass not set")
        exit(1)
		
    if not os.environ.get("admin2_user"):
        raise RuntimeError("admin2_user not set")
        exit(1)
    if not os.environ.get("admin2_pass"):
        raise RuntimeError("admin2_pass not set")
        exit(1)
		
    if not os.environ.get("admin3_user"):
        raise RuntimeError("admin3_user not set")
        exit(1)
    if not os.environ.get("admin3_pass"):
        raise RuntimeError("admin3_pass not set")
        exit(1)
    return True

