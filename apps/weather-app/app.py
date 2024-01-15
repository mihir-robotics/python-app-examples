from flask import Flask, render_template, request
import asyncio

app = Flask(__name__)

sensor_data=""

@app.route('/')
def index():
    return render_template('index.html', sensor_data=sensor_data)

@app.route('/send-data', methods=['POST'])
def receive_data():
    global sensor_data
    temperature =  request.form.get('temperature')
    humidity = request.form.get('humidity')
    sensor_data = "Temperature: " + str(temperature) + " | Humidity: " + str(humidity) 
    asyncio.run(update_sensor_data())  # Run the asynchronous update
    # Log the received data along with the default log statement
    app.logger.info(f'Received data: {sensor_data}')
    return str(sensor_data)

async def update_sensor_data():
    await asyncio.sleep(1)  # Simulating some asynchronous task
    print(f"Updated sensor data: {sensor_data}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Expose this app
