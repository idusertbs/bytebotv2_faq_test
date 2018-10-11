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

    flagRequiereParametro = False
    if intentDisplayName.find("unico") or len(parameters):
        flagRequiereParametro = False
    else:
        flagRequiereParametro = True 

    #Proceso de recolección de parámetro:

    return {

"fulfillmentText": "displayed&spoken response",

"fulfillmentMessages": [

{

"text": [

"text response"

],

}

],

"source": "example.com",

"payload": {

"google": {

"expectUserResponse": True,

"richResponse": {

"items": [

{

"simpleResponse": {

"textToSpeech": "this is a simple response"

}

}

]

}

},

"facebook": {

"text": "Hello, Facebook!"

},

"slack": {

"text": "This is a text response for Slack."

}

},

"outputContexts": [

{

"name": "aa",

"lifespanCount": 5,

"parameters": {

"param": "param value"

}

}

],

"followupEventInput": {

"name": "event name",

"languageCode": "en-US",

"parameters": {

"param": "param value"

}

}

}
    


    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















