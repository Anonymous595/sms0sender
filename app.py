from flask import Flask, render_template, request, jsonify
from vonage import Client, Sms
import os

app = Flask(__name__)

# Initialize Vonage client
vonage_client = Client(key='1d809289', secret='MrCzg9gNFleieRqQ')
sms = Sms(vonage_client)

# In-memory storage for SMS history
sms_history = []

@app.route('/')
def index():
    return render_template('index.html', history=sms_history)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    to_number = request.form['to_number']
    message = request.form['message']
    response = sms.send_message({
        'from': 'VonageSMS',
        'to': to_number,
        'text': message
    })
    
    status = 'sent' if response['messages'][0]['status'] == '0' else 'failed'
    sms_history.append({
        'to_number': to_number,
        'message': message,
        'status': status
    })
    return jsonify(success=(status == 'sent'))

@app.route('/delete_sms/<int:index>', methods=['POST'])
def delete_sms(index):
    if 0 <= index < len(sms_history):
        del sms_history[index]
        return jsonify(success=True)
    return jsonify(success=False), 400

if __name__ == '__main__':
    app.run(debug=True)