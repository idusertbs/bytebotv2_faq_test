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

    producto = False
    outputContexts_producto = queryResult.get("outputContexts")
    for element in outputContexts_producto:
        if element.get("name").find("requiere_parametro") > 0:            
            if element.get("parameters").get("producto") != None:
                producto = element.get("parameters").get("producto")            
                break
            else: 
                producto = False
        else:
            pregunta = False

    flagRequiereParametro = False
    if intentDisplayName.find("unico") >= 0 or len(parameters) > 0:
        flagRequiereParametro = False
    else:
        flagRequiereParametro = True

    #Proceso de recolección de parámetro:
    if flagRequiereParametro and not(producto):
        return {
        "fulfillmentText":"¿Para qué producto necesita saber la respuesta?" ,        
        "source":"example.com",
        "outputContexts": [
                {
                "name": "projects/bytebot-faq-demo-1/agent/sessions/30739716-36e5-8e8b-1758-584c5419e3f1/contexts/memoria_total",
                "lifespanCount": 1,
                "parameters": {
                    "pregunta": queryText
                }
        }]        
        }

    else:
        #Proceso de reformulación
        #Se debe extraer la pregunta de la memoria_total: parámetro "pregunta"
        #####

        pregunta = False
        outputContexts = queryResult.get("outputContexts")
        for element in outputContexts:
            if element.get("name").find("memoria_total") > 0:
                pregunta = element.get("parameters").get("pregunta")
                producto = element.get("parameters").get("producto")
                break
            else:
                pregunta = False
                
        if pregunta:
            return {
            "fulfillmentText": "Concatenando: " + pregunta +  " + " + producto,        
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
        else:
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

    



        #Va al servicio de Ranking.
        


    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















