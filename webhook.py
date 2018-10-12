# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:37:23 2018

@author: amanosalva
"""

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):

    queryResult = req.get("queryResult")
    parameters = queryResult.get("parameters")
    intent = queryResult.get("intent")
    intentDisplayName = intent.get("displayName")
    queryText = queryResult.get("queryText")

    flagRequiereParametro = False
    if intentDisplayName.find("unico") >= 0 or len(parameters) > 0:
        flagRequiereParametro = False
    else:
        flagRequiereParametro = True 

    #Proceso de recolección de parámetro:
    if flagRequiereParametro:
        return {
        "fulfillmentText":"¿Para qué producto necesita saber la respuesta?" ,        
        "source":"example.com",
        "outputContexts": [
                {
                "name": "projects/bytebot-faq-demo-1/agent/sessions/30739716-36e5-8e8b-1758-584c5419e3f1/contexts/memoria_total",
                "lifespanCount": 5,
                "parameters": {
                    "pregunta": queryText
                }
        }]        
        }

    else:
        #Proceso de reformulación

        #####

        return {
        "fulfillmentText":"La respuesta es:" ,        
        "source":"example.com",
        "outputContexts": [
            {
            "name": "projects/bytebot-faq-demo-1/agent/sessions/30739716-36e5-8e8b-1758-584c5419e3f1/contexts/memoria_1",
            "lifespanCount": 5,
            "parameters": {
                "pregunta": queryText
                }
        }]        
        }



    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















