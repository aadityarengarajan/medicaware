#!/usr/bin/env python

'''
                                                                                                                                                                                             
 _|      _|                  _|  _|              _|_|                                                          _|_|_|_|_|                    _|                  _|                      _|  
 _|_|  _|_|    _|_|      _|_|_|        _|_|_|  _|    _|  _|      _|      _|    _|_|_|  _|  _|_|    _|_|            _|      _|_|      _|_|_|  _|_|_|    _|_|_|          _|_|_|    _|_|_|  _|  
 _|  _|  _|  _|_|_|_|  _|    _|  _|  _|        _|_|_|_|  _|      _|      _|  _|    _|  _|_|      _|_|_|_|          _|    _|_|_|_|  _|        _|    _|  _|    _|  _|  _|        _|    _|  _|  
 _|      _|  _|        _|    _|  _|  _|        _|    _|    _|  _|  _|  _|    _|    _|  _|        _|                _|    _|        _|        _|    _|  _|    _|  _|  _|        _|    _|  _|  
 _|      _|    _|_|_|    _|_|_|  _|    _|_|_|  _|    _|      _|      _|        _|_|_|  _|          _|_|_|          _|      _|_|_|    _|_|_|  _|    _|  _|    _|  _|    _|_|_|    _|_|_|  _|  
                                                                                                                                                                                             
                                                                                                                                                                                             
Technical Staff Client for MedicAware
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 23:21 10/22/21 22 10 2021

[TO-DO]

[X] API at ('api.medicaware.intellx.co.in') to co-ordinate everything
[X] Website for Customers at ('medicaware.intellx.co.in')
    [X] Home Page
    [X] Why Us? Page
    [X] Services Page
    [X] Rights and Responsibilities Page
    [X] Contact Us Page
    [X] Careers Page
[X] Website for Patients at ('patient.medicaware.intellx.co.in') where one can
    [X] Sign Up
        [X] Name
        [X] E-Mail
        [X] Phone
        [X] Address
        [X] Medical History
        [X] Date of Birth
        [X] Passport Photo
    [X] Log In
    [X] Book an Appointment
    [X] First-Aid and Self-Diagnosis
    [X] Report COVID Symptoms
    [X] Book Vaccination (URL to CoWin)
    [X] See Medical History
[X] Android WebApp at ('android.medicaware.intellx.co.in') where one can
    [X] See COVID Database
    [X] See Hospital Staff
    [X] Self Diagnosis
    [X] See WebMD
[X] Website for Reception//Front Desk at ('frontdesk.medicaware.intellx.co.in') where one can
    [X] Book an Appointment
    [X] Register a Patient
    [X] Book a Lab Appointment
[X] Website for Technical Staff at ('tech.medicaware.intellx.co.in') where one can
    [X] Publish to Newsletter
    [X] Update Notices
    [] (SKIPPED) Update Staff and Vacancies
- Website for Doctors at ('doctor.medicaware.intellx.co.in') where one can
    - See list of appointments
    - Complete an appointment
    - Book a Lab Appointment
- Website for Lab Technicians at ('labs.medicaware.intellx.co.in') where one can
    - Register a Machine
    - Book a Lab Appointment
    - See List of Lab Appointments
    - Upload and Send Lab Report(s)
- Change Flask Port
- Remove Debuggers on Production Deployment

'''
#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip

from flask import redirect, render_template, Flask, request, url_for, send_file, session
import json, requests, uuid
#==============DEFINING BASIC FUNCTIONS======================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any random string'

#==============ROUTES======================================================
#/- routes are defined by @app.route decorator

@app.route('/favicon.ico')
def favicon():
    return send_file("thumb.png")

@app.route('/login', methods = ['GET','POST'])
def login():

    if request.method == "GET":
        return render_template("login.html")

    else:
        name = request.form.get("email")
        pwd = request.form.get("pwd")
        staff = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()
        for member in staff:
            if member["email"] == name:
                if member["password"] == pwd:
                    if "T" in member["permissions"]:
                        session["user"] = {"name" : member["name"],"position": member["position"]}
                        session["logged-in"] = "true"
                        return redirect(url_for('index'))
        return "INVALID AUTH"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
def index():

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    return render_template("index.html",user=session.get("user"))

@app.route('/notice')
def notice():

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    circulars = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=tech").json()["notices"]

    return render_template("notice.html",notams=circulars)

@app.route('/notice/delete/<code>')
def notice_delete(code):

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    circulars = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=tech").json()["notices"]

    new_circ = []

    for i in circulars:
        if i["code"]!=code:
            new_circ.append(i)

    requests.post("https://api.medicaware.intellx.co.in/write?key=$OSC&file=tech",data={"content":json.dumps({"notices":new_circ})})

    return 'DELETED!'

@app.route('/notice/publish', methods=['GET','POST'])
def notice_publish():

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    circulars = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=tech").json()["notices"]

    circ = {
                "code" : str(uuid.uuid4()).split("-")[0].upper(),
                "title" : request.form.get("title"),
                "content" : request.form.get("content"),
                "scope" : str(''.join(list(request.form.getlist("scope")))),
                "valid" : request.form.get("until").split("T")[0]
            }

    circulars.append(circ)

    requests.post("https://api.medicaware.intellx.co.in/write?key=$OSC&file=tech",data={"content":json.dumps({"notices":circulars})})

    return 'ADDED!'

#==============ERROR HANDLING======================================================
#/- custom error handling using custom template to get fancy ;)

@app.errorhandler(404)
def page_not_found(e):
    return str((render_template('error.html',
                code="404",
                type="Not Found",
                content="Sorry, this page was not found!"))), 404
@app.errorhandler(500)
def internal_server_error(e):
    return str((render_template('error.html',
                code="500",
                type="Internal Server Error",
                content=f"Oh No! Something Went Wrong!<br/>{e}"))), 500
@app.errorhandler(410)
def gone(e):
    return str((render_template('error.html',
                code="410",type="Gone",
                content="Sorry, this page is has mysteriously vanished!"))), 410
@app.errorhandler(403)
def forbidden(e):
    return str((render_template('error.html',
                code="403",
                type="Forbidden",
                content="Sorry, you are not allowed to access this page!"))), 403
@app.errorhandler(401)
def unauthorized(e):
    return str((render_template('error.html',
                code="401",
                type="Unauthorized",
                content="Sorry, you are not authorized to access this page!"))), 401

#==============PROGRAM RUN======================================================

if __name__=="__main__":
    #/- note : remove debuggers and change port respectively
    #/- on production deployment.
    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=8080,
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        )

#==============END OF WEBAPP======================================================