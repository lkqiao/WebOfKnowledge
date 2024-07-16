from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data_request = request.get_json()
        # Process data
        return jsonify({'message': 'Data received', 'data': data_request})

    if request.method == 'GET':
        return jsonify({'message': 'Data received', 'data': 'Hello World'})

    else:
        return jsonify({'message': 'Send some data'})


if __name__ == '__main__':
    app.run(debug=True)
