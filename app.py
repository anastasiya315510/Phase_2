from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/health')
def healthz():
    return jsonify(status="ok"), 200

@app.route('/ready')
def ready():
    return jsonify(status="ready"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
