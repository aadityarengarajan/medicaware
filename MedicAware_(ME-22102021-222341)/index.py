#!/usr/bin/env python

'''
                                                                                                           
 _|      _|                  _|  _|              _|_|                                                      
 _|_|  _|_|    _|_|      _|_|_|        _|_|_|  _|    _|  _|      _|      _|    _|_|_|  _|  _|_|    _|_|    
 _|  _|  _|  _|_|_|_|  _|    _|  _|  _|        _|_|_|_|  _|      _|      _|  _|    _|  _|_|      _|_|_|_|  
 _|      _|  _|        _|    _|  _|  _|        _|    _|    _|  _|  _|  _|    _|    _|  _|        _|        
 _|      _|    _|_|_|    _|_|_|  _|    _|_|_|  _|    _|      _|      _|        _|_|_|  _|          _|_|_|  
                                                                                                           
                                                                                                           
Suite of Software for Hospitals
for SOSC HackNight 2021
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
    - Book an Appointment ('patient.medicaware.intellx.co.in')
        - Sign Up
            - Name
            - E-Mail
            - Phone
            - Address
            - Medical History
            - Date of Birth
            - Passport Photo
        - Log In
- Website for Patients at ('patient.medicaware.intellx.co.in') where one can enter a Patient Code alongwith their e-mail to get an OTP
    - Book an Appointment
    - See Newsletter
    - First-Aid and Self-Diagnosis
    - Report COVID Symptoms
    - Book Vaccination (URL to CoWin)
    - See Medical History and Edit Profile
- Android WebApp at ('android.medicaware.intellx.co.in') where one can
    - See COVID Database
    - See Hospital Staff
    - Self Diagnosis
    - See Patient Profile
    - See WebMD
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
from flask import redirect, render_template, Flask, request, url_for, send_file
import requests, json

#==============DEFINING BASIC FUNCTIONS======================================================
app = Flask(__name__)

#==============ROUTES======================================================
#/- routes are defined by  @app.route decorator

@app.route('/favicon.ico')
def favicon():
    return send_file("thumb.png")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/why-us')
def why_us():
    return render_template("why_us.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/rights-and-responsibilities')
def rnr():
    return render_template("rnr.html")

@app.route('/contact-us')
def contact():
    return render_template("contact.html")

@app.route('/careers')
def careers():

    positions = requests.get("https://api.medicaware.intellx.co.in/read?key=$OSC&file=STAFF").json()
    vacancies = []
    for i in positions:
        if i["status"] == "vacant":
            vacancies.append(i)

    return render_template("careers.html",vacancies=vacancies)


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