from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def index2():
    return render_template('index.html')

@app.route('/weather')
def weatherPage():
    return render_template('concept.html') 

@app.route('/info')
def infoPage():
    return render_template('info.html')     

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = os.getenv('TOKEN') 
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except Exception as err:
        return jsonify({"error": f"Other error occurred: {err}"}), 500

    data = response.json()
    formatted_data = {
        "temperature": round(data['main']['temp'], 1),
        "humidity": round(data['main']['humidity'], 1),
        "description": data['weather'][0]['description'].capitalize(),
        "wind_speed": round(data['wind']['speed'], 1),
        "city": data['name'],
        "country": data['sys']['country']
    }
    
    return jsonify(formatted_data)

@app.route('/forecast', methods=['GET'])
def get_weather_forecast():
    city = request.args.get('city')
    api_key = os.getenv('TOKEN')
    api_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except Exception as err:
        return jsonify({"error": f"Other error occurred: {err}"}), 500

    data = response.json()
    forecast_data = []

    for forecast in data['list'][:12]:  
        forecast_data.append({
            "date": forecast['dt_txt'],
            "temperature": round(forecast['main']['temp'], 1),
            "humidity": round(forecast['main']['humidity'], 1),
            "description": forecast['weather'][0]['description'].capitalize(),
            "wind_speed": round(forecast['wind']['speed'], 1)
        })

    return jsonify(forecast_data)

if __name__ == '__main__':
    from waitress import serve
    #serve(app, host="0.0.0.0", port=8008)
    app.run(host="0.0.0.0", port=8030)
