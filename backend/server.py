from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        # Process data
        return jsonify({'message': 'Data received', 'data': data})
    else:
        return jsonify({'message': 'Send some data'})

if __name__ == '__main__':
    app.run(debug=True)
