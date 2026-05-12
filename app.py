from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "app": "my-app",
        "status": "running",
        "message": "Hello from Jenkins CI/CD Pipeline Test! 🚀"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    return jsonify({"result": a + b})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
