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

    result = req.get("result")
    metadata = result.get("metadata")
    intentName = metadata.get("intentName")
    
    if intentName == "prediccion.clima":
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        date = parameters.get("date")
        if city is None:
            return None
        r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=a788b8747f3d4299c2592fdedb2b1e45')
        json_object = r.json()
        weather=json_object['list']
        for i in range(0,30):
            if date in weather[i]['dt_txt']:
                condition= weather[i]['weather'][0]['description']
                break
        speech = "La predicción para "+city+ " el "+date+" es: "+condition
        return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
        }
        
    

    if intentName == "promocion.webhook":             
        result = req.get("result")
        parameters = result.get("parameters")
        nombre = parameters.get("promo")
        if nombre is None:
            return None
        r=requests.get('http://181.177.228.114:8095/items/')
        json_object = r.json()
        promociones=json_object['promociones']
        for i in range(0,30):
            if nombre in promociones[i]['nombre']:
                descripcionPromo = promociones[i]['descripcion']
                moneda = promociones[i]['moneda']
                costo = promociones[i]['costo']
                break
        speech = "La promoción nombre consta de "+descripcionPromo+ " a tan solo "+moneda+" "+costo + "!!!"
        print(speech)
        return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
        }


    if intentName == "test-facebook-webhook":             
        result = req.get("result")
        parameters = result.get("parameters")
        nombre = parameters.get("promo")        
        return {
        "speech": "speech",
        "displayText": "speech",
        "source": "apiai-weather-webhook",
        "messages": [
				{
					"type": "simple_response",
					"platform": "google",
					"textToSpeech": "Te escribo desde el webhook! - textToSpeech"
				},
				{
					"type": 3,
                    "platform": "facebook",
                    "imageUrl": "https://firebasestorage.googleapis.com/v0/b/dialogflowproyect.appspot.com/o/Para-qu%C3%A9-sirve-un-histograma_opt.png?alt=media&token=1ca38de2-5c07-4bff-bcea-7f3e60d78c11"
				},
				{
					"type": 0,
					"speech": "Lo siento, aún no configuro nada para whatsapbi"
				}
			]
        }

    if intentName == "test-facebook-webhook-card":
        result = req.get("result")
        parameters = result.get("parameters")
        cliente_id = parameters.get("cliente_id")              
        r=requests.get('http://181.177.228.114:5000/grafico/'+str(cliente_id))
        json_object = r.json()
        url_image=json_object['url_image']       
        return {
        "speech": "speech",
        "displayText": "speech",
        "source": "apiai-weather-webhook",
        "messages": [
				{
					"type": "simple_response",
					"platform": "google",
					"textToSpeech": "Te escribo desde el webhook! - textToSpeech"
				},
				{
					"type": 3,
                    "platform": "facebook",
                    "imageUrl": url_image
				},
				{
					"type": 0,
					"speech": "Lo siento, aún no configuro nada para whatsapbi"
				}
			]
        }    


    if intentName == "promocion.planes.consultar":             
        result = req.get("result")       
        
        r=requests.get('http://181.177.228.114:8095/items/')
        json_object = r.json()
        promociones=json_object['promociones']
        descripcionPromo = []
        for i in range(0,len(promociones)):
            temp = []
            temp.append(promociones[i]['descripcion'])
            descripcionPromo.append(temp)
            speech = "Te escribo desde el webhook! - speech"
			
        	
        return {
			"speech": speech,
			"displayText": speech,
			"source": "apiai-weather-webhook",
			"messages": [
				{
					"type": "simple_response",
					"platform": "google",
					"textToSpeech": "Te escribo desde el webhook! - textToSpeech"
				},
				{
					"type": 4,
					"platform": "telegram",
					"payload": {
						"telegram": {
							"text": "¡Elija su promoción!",
							"reply_markup": {
								"keyboard": descripcionPromo,
								"one_time_keyboard": False,
								"resize_keyboard": True
								}
							}
						}
				},
				{
					"type": 0,
					"speech": "Lo siento, aún no configuro nada para whatsapbi"
				}
			]
		}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















