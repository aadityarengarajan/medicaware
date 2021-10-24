#!/usr/bin/env python

import requests,json
print(requests.post("https://api.medicaware.intellx.co.in/write?key=$OSC&file=patients",data={"content":json.dumps([
    {
        "id" : "MAP1",
        "name" : "Aarti Khare",
        "DOB" : "01/12/1983",
        "phone" : "+915684555247",
        "join" : "14/05/2019",
        "history" : "DIABETIC PATIENT\nBYPASS SURGERY",
        "hospital" : [
                        {
                            "date" : "14/05/2019",
                            "doc"  : "MAS8",
                            "issue" : "Urinary Infection",
                            "lab" : "",
                            "appointment" : "MA.APP.D1",
                        },
                        {
                            "date" : "14/05/2019",
                            "doc"  : "MAS5",
                            "issue" : "Urinary Infection",
                            "lab" : "Sample Test - Urine",
                            "appointment" : "MA.APP.L1",
                        }
                     ],
        "country" : "India",
        "password" : "akhare",
        "email" : "thisisaarti@gmail.com"
    }
],indent=4)}).text)