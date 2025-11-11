from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Weather API',
        'status': 'running'
    })

@app.route('/api/weather/current')
def weather_current():
    city = request.args.get('city', 'Unknown')
    return jsonify({
        'city': city,
        'temperature_c': 25,
        'condition': 'Sunny',
        'humidity': 60
    })

@app.route('/api/weather/forecast')
def weather_forecast():
    city = request.args.get('city', 'Unknown')
    days = int(request.args.get('days', 3))

    forecast = []
    for d in range(1, days + 1):
        forecast.append({
            'day': d,
            'temperature_c': 25 + d,
            'condition': 'Sunny' if d % 2 == 0 else 'Cloudy'
        })

    return jsonify({
        'city': city,
        'days': days,
        'forecast': forecast
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)