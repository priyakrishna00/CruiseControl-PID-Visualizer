from flask import Flask, request, jsonify, send_from_directory
from pid_simulation import run_pid_simulation

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        kp = float(data.get("kp", 1.0))
        ki = float(data.get("ki", 0.1))
        kd = float(data.get("kd", 0.05))
        results = run_pid_simulation(kp, ki, kd)
        return jsonify(results)
    except Exception as e:
        print("Error in /simulate:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
