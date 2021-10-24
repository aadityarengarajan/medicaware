#!/usr/bin/env python

'''
                                                                                                                                                                                                             
 _|      _|                  _|  _|              _|_|                                                          _|_|_|_|                                  _|          _|_|_|                        _|        
 _|_|  _|_|    _|_|      _|_|_|        _|_|_|  _|    _|  _|      _|      _|    _|_|_|  _|  _|_|    _|_|        _|        _|  _|_|    _|_|    _|_|_|    _|_|_|_|      _|    _|    _|_|      _|_|_|  _|  _|    
 _|  _|  _|  _|_|_|_|  _|    _|  _|  _|        _|_|_|_|  _|      _|      _|  _|    _|  _|_|      _|_|_|_|      _|_|_|    _|_|      _|    _|  _|    _|    _|          _|    _|  _|_|_|_|  _|_|      _|_|      
 _|      _|  _|        _|    _|  _|  _|        _|    _|    _|  _|  _|  _|    _|    _|  _|        _|            _|        _|        _|    _|  _|    _|    _|          _|    _|  _|            _|_|  _|  _|    
 _|      _|    _|_|_|    _|_|_|  _|    _|_|_|  _|    _|      _|      _|        _|_|_|  _|          _|_|_|      _|        _|          _|_|    _|    _|      _|_|      _|_|_|      _|_|_|  _|_|_|    _|    _|  
                                                                                                                                                                                                             
                                                                                                                                                                                                             
Front Desk Client for MedicAware
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
- Website for Technical Staff at ('tech.medicaware.intellx.co.in') where one can
    - Publish to Newsletter
    - Update Notices
    - Update Staff and Vacancies
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
import json, requests, datetime

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
                    if "F" in member["permissions"]:
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

@app.route('/book-appointment',methods=['GET','POST'])
def appointment():

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    if request.method=="GET":

        session["patient"] = request.args.get("patient")

        print("PATIENT SET TO",session.get("patient"))

        step=0
        staff = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()
        docs = []
        for doc in staff:
            if "doctor" in doc["position"].lower():
                docs.append(doc)
            if "lab" in doc["position"].lower():
                docs.append(doc)
        return render_template("appointment.html",doctors=docs,step=step)

    if request.method=="POST":

        if request.form.get("check_availability") == "true":
            step=1
            appt = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=appointments").json()
            staff = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()
            doc = request.form.get("doctor")
            bookings = []
            for i in staff:
                if i["id"] == doc:
                    TheDoctor = i
                    break
            for i in appt:
                if i["doctor"] == doc:
                    dt = i["d&t"].strip()
                    a = (datetime.datetime.strptime(dt,"%d/%m/%Y %H:%M"))
                    a = a.strftime("%d/%m/%Y %H:%M")
                    timefor = a + " - " + (datetime.datetime.strptime(dt,"%d/%m/%Y %H:%M") + datetime.timedelta(minutes=30)).strftime("%d/%m/%Y %H:%M")
                    bookings.append(timefor)
            return render_template("appointment.html",doc=TheDoctor,step=step,bookings=bookings)
        else:
            step=2
            issue = request.form.get("issue")
            dt = request.form.get("dt")
            appt = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=appointments").json()
            staff = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()
            doc = request.form.get("doctor")
            bookings = []
            for i in staff:
                if i["id"] == doc:
                    TheDoctor = i
                    break
            for i in appt:
                if i["doctor"] == doc:
                    mydt = i["d&t"].strip()
                    start = datetime.datetime.strptime(mydt,"%d/%m/%Y %H:%M")
                    end = datetime.datetime.strptime(mydt,"%d/%m/%Y %H:%M") + datetime.timedelta(minutes=30)
                    delta = end - start
                    seconds = [start + datetime.timedelta(seconds=i) for i in range(delta.seconds + 1)]
                    bookings.append(seconds)
                    start = datetime.datetime.strptime(mydt,"%d/%m/%Y %H:%M") - datetime.timedelta(minutes=15)
                    end = datetime.datetime.strptime(mydt,"%d/%m/%Y %H:%M")
                    delta = end - start
                    seconds = [start + datetime.timedelta(seconds=i) for i in range(delta.seconds + 1)]
                    bookings.append(seconds)
            dt = datetime.datetime.strptime(dt,"%Y-%m-%dT%H:%M")
            for i in bookings:
                if dt in i:
                    return "ERROR. TIME RESERVED."

            apps = []
            for i in appt:
                ds = i["id"].split(".")[-1]
                dst = ''
                for i in ds:
                    if i.isnumeric():
                        dst+=i
                ds = dst
                apps.append(int(ds))
            data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=patients").json()
            
            print(session.get("patient"))

            for i in data:
                if i["id"] == session.get("patient"):
                    patient = i

            appointment = {
                "id" : f"MA.APP.D{max(apps)+1}",
                "patient" : patient["id"],
                "doctor" : TheDoctor["id"],
                "issue" : issue,
                "d&t" : dt.strftime("%d/%m/%Y %H:%M"),
                "complete" : False
            }

            appt.append(appointment)
            requests.post("https://api.medicaware.intellx.co.in/write?key=$OSC&file=appointments",data={"content":json.dumps(appt,indent=4)})

            session.pop('patient')
            return "BOOKED!"

@app.route('/register-patient',methods=['GET','POST'])
def register_pat():

    if request.method == "GET":
        if session.get("logged-in") != "true" : return redirect(url_for("login"))

    if request.method=="POST":

        ids = []
        data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=patients").json()
        # return json.dumps(requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=patients").json(),indent=4)
        for i in data:
            print(i['name'],data.index(i),i.keys(),"id" in i.keys())
            ids.append(int(i["id"][3:]))
        patient =  {
                        "name" : request.form.get("name"),
                        "DOB" : request.form.get("dob"),
                        "phone" : request.form.get("phone"),
                        "join" : datetime.datetime.now().strftime("%d/%m/%Y"),
                        "history" : request.form.get("medhist"),
                        "hospital" : [],
                        "country" : request.form.get("address"),
                        "password" : request.form.get("passwd"),
                        "email" : request.form.get("email")
                    }
        topop = []
        for i in data:
            j = i.copy()
            del j['id']
            if j==patient:
                return "ALR EXSTS"
        MYID = f"MAP{max(ids)+1}"
        patient.update({"id" : MYID})
        data.append(patient)

        requests.post("https://api.medicaware.intellx.co.in/write?key=$OSC&file=patients",data={"content":json.dumps(data,indent=4)})

        return 'REGISTERED!'

    return render_template("reg-pat.html")


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