#!/usr/bin/env python

'''
                                                                                                                                           
 _|      _|                  _|  _|              _|_|                                                            _|_|    _|_|_|    _|_|_|  
 _|_|  _|_|    _|_|      _|_|_|        _|_|_|  _|    _|  _|      _|      _|    _|_|_|  _|  _|_|    _|_|        _|    _|  _|    _|    _|    
 _|  _|  _|  _|_|_|_|  _|    _|  _|  _|        _|_|_|_|  _|      _|      _|  _|    _|  _|_|      _|_|_|_|      _|_|_|_|  _|_|_|      _|    
 _|      _|  _|        _|    _|  _|  _|        _|    _|    _|  _|  _|  _|    _|    _|  _|        _|            _|    _|  _|          _|    
 _|      _|    _|_|_|    _|_|_|  _|    _|_|_|  _|    _|      _|      _|        _|_|_|  _|          _|_|_|      _|    _|  _|        _|_|_|  
                                                                                                                                           
                                                                                                                                           
API for MedicAware
Suite of Software for Hospitals
for the SOSC HackNight
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 22:23 10/22/21 22 10 2021
[TO-DO]
- Change Flask Port
- Remove Debuggers on Production Deployment
- API at ('api.medicaware.intellx.co.in') to co-ordinate everything
'''
#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip
from flask import render_template, Flask, request, jsonify
import json
#==============DEFINING BASIC FUNCTIONS======================================================
app = Flask(__name__)
def getJson(file):
    with open(f"data/{file}.json") as f:
        content = json.load(f)
    return content
def getKey(key):
    APIKeys = []
    for x in getJson("keys"):
        APIKeys.append(x["key"])
    if key in APIKeys:
        return (getJson("keys")[APIKeys.index(key)])
    return ({"key":"Not Found","validity":"invalid","error":"404/403"})
#==============ROUTES======================================================
#/- routes are defined by  @app.route decorator
@app.route('/validate')
def ValidateKey():
    return jsonify(getKey(request.args.get("key")))
@app.route('/read')
def ReadFile():
    argumentConverter = {
                    "APPOINTMENTS" : "appointments",
                    "EQUIPMENT-LIST" : "eqpt",
                    "EQUIPMENTS" : "eqpt",
                    "LAB" : "eqpt",
                    "NEWSLETTER" : "newsletter",
                    "TECH" : "newsletter",
                    "PATIENTS" : "patients",
                    "PHARMACY" : "pharma",
                    "SELF-DIAGNOSIS" : "self-diag",
                    "SYMPTOMS" : "self-diag",
                    "STAFF" : "staff",
                    "EMPLOYEES" : "staff",
                    "EQPT" : "eqpt",
                    "PHARMA":"pharma",
                    "MEDIC" :"pharma",
                    "SELF-DIAG":"self-diag"
                        }
    fileRequired = argumentConverter.get(request.args.get("file").upper())
    if (getKey(request.args.get("key")).get("error") == None) and (fileRequired != None):
        if "R" in getKey(request.args.get("key")).get("permissions"):
            return jsonify(getJson(fileRequired))
    return jsonify(getKey("INVALIDKEYRESPONSE")),403
@app.route('/write', methods=['POST'])
def WriteFile():
    argumentConverter = {
                    "APPOINTMENTS" : "appointments",
                    "EQUIPMENT-LIST" : "eqpt",
                    "EQUIPMENTS" : "eqpt",
                    "LAB" : "eqpt",
                    "NEWSLETTER" : "newsletter",
                    "TECH" : "newsletter",
                    "PATIENTS" : "patients",
                    "PHARMACY" : "pharma",
                    "SELF-DIAGNOSIS" : "self-diag",
                    "SYMPTOMS" : "self-diag",
                    "STAFF" : "staff",
                    "EMPLOYEES" : "staff",
                    "EQPT" : "eqpt",
                    "PHARMA":"pharma",
                    "MEDIC" :"pharma",
                    "SELF-DIAG":"self-diag"
                        }
    fileRequired = argumentConverter.get(request.args.get("file").upper())
    if (getKey(request.args.get("key")).get("error") == None) and (fileRequired != None):
        if "W" in getKey(request.args.get("key")).get("permissions"):
            with open(f"data/{fileRequired}.json.bak","w") as backupFile:
                json.dump(getJson(fileRequired),backupFile,indent=4)
            with open(f"data/{fileRequired}.json","w") as JSONFile:
                print(json.loads(request.form.get("content")))
                json.dump(json.loads(request.form.get("content")),JSONFile,indent=4)
            return jsonify(getKey(request.args.get("key")).update({"write":"complete"}))
    return jsonify(getKey("INVALIDKEYRESPONSE")),403

#==============PROGRAM RUN======================================================
if __name__=="__main__":
    #/- note : remove debuggers and change port respectively
    #/- on production deployment.
    app.run(
        port=8080,
        threaded=True)
#==============END OF WEBAPP======================================================