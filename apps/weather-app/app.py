from flask import Flask, request

app = Flask(__name__)

@app.route('/send-data', methods=['POST'])
def receive_data():
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    
    # Do something with the received data (store in DB, process, etc.)
    print(f"Received Temperature: {temperature}, Humidity: {humidity}")
    
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run your Flask app
