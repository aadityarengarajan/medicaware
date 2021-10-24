#!/usr/bin/env python

'''
                                                                                                                                                                                         
 _|      _|                  _|  _|              _|_|                                                          _|_|_|                _|      _|                        _|                
 _|_|  _|_|    _|_|      _|_|_|        _|_|_|  _|    _|  _|      _|      _|    _|_|_|  _|  _|_|    _|_|        _|    _|    _|_|_|  _|_|_|_|        _|_|    _|_|_|    _|_|_|_|    _|_|_|  
 _|  _|  _|  _|_|_|_|  _|    _|  _|  _|        _|_|_|_|  _|      _|      _|  _|    _|  _|_|      _|_|_|_|      _|_|_|    _|    _|    _|      _|  _|_|_|_|  _|    _|    _|      _|_|      
 _|      _|  _|        _|    _|  _|  _|        _|    _|    _|  _|  _|  _|    _|    _|  _|        _|            _|        _|    _|    _|      _|  _|        _|    _|    _|          _|_|  
 _|      _|    _|_|_|    _|_|_|  _|    _|_|_|  _|    _|      _|      _|        _|_|_|  _|          _|_|_|      _|          _|_|_|      _|_|  _|    _|_|_|  _|    _|      _|_|  _|_|_|    
                                                                                                                                                                                         
                                                                                                                                                                                         
Android Client for MedicAware
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 22:23 10/22/21 22 10 2021

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
- Website for Reception//Front Desk at ('frontdesk.medicaware.intellx.co.in') where one can
    - Book an Appointment
    - Register a Patient
    - Book a Lab Appointment
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
- Pharmacy Management at ('pharmacy.medicaware.intellx.co.in') where one can
    - Update Medicine Database by uploading Excel Sheet
    - Simple POS System for Stock Management and Accounts Management
- Change Flask Port
- Remove Debuggers on Production Deployment
'''
#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip

from flask import redirect, render_template, Flask, request, url_for, send_file, session
import requests, json, datetime

#==============DEFINING BASIC FUNCTIONS======================================================
app = Flask(__name__)

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

#==============ROUTES======================================================
#/- routes are defined by  @app.route decorator

@app.route('/favicon.ico')
def favicon():
    return send_file("thumb.png")

@app.route('/')
def index():

    data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=newsletter").json()["notices"]

    newsletter = []

    for i in data:
        if "O" in i["scope"]:
            newsletter.append(i)

    covid19 = requests.get("https://data.covid19india.org/data.json").json()["tested"]

    doses = human_format(int(covid19[-1]["totaldosesadministered"]))
    rtpcr = human_format(int(covid19[-1]["dailyrtpcrsamplescollectedicmrapplication"]))
    vaccines = human_format(int(covid19[-1]["totalvaccineconsumptionincludingwastage"]))

    return render_template("index.html",
                            doses=doses,
                            rtpcr=rtpcr,
                            vaccines=vaccines,
                            news=newsletter)

@app.route('/staff')
def staff():

    data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()

    staff = []

    for i in data:
        if "D" in i["permissions"].upper():
            if i["status"]=="active":
                staff.append(i)
        if "L" in i["permissions"].upper():
            if i["status"]=="active":
                staff.append(i)

    data = staff

    return render_template("staff.html",staff=data)


@app.route('/self-diagnosis',methods=['POST','GET'])
def self_diagnosis_form():

    if request.method == "GET":

        data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=symptoms").json()

        allsymps = []
        for i in list(data.values()):
            for j in i["symptoms"]:
                allsymps.append(j)

        listb = []
        for i in allsymps:
            if i not in listb : listb.append(i)

        allsymps = listb

        return render_template("self-diagnosis.html",symptoms = allsymps)

    else:

        mysymps = request.form.getlist('symptom')

        data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=symptoms").json()

        docs = []
        for i in list(data.values()):
            for j in i["symptoms"]:
                if j in mysymps:
                    for k in i["doctors"]:
                        docs.append(k)

        docb = []
        for i in docs:
            if i not in docb: docb.append(i)

        data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=staff").json()

        docs = []

        def getDocByID(id):
            for i in data:
                if i["id"] == id:
                    return i

        for i in docb:
            docs.append(getDocByID(i))

        return render_template("suggested-docs.html",doctors = docs)

@app.route('/webMD')
def webMD():

        data = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=pharmacy").json()

        return render_template("webmd.html")


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