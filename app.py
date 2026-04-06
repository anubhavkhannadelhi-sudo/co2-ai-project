from flask import Flask, request, jsonify
from flask_cors import CORS

# =========================
# APP INITIALIZATION
# =========================
app = Flask(__name__)
CORS(app)  # Allow frontend access

# =========================
# HEALTH CHECK ROUTE
# =========================
@app.route('/')
def home():
    return "CO2 AI Backend Running 🚀"

# =========================
# CO2 CALCULATION FUNCTION
# =========================
def calculate_co2(pm25, temp, people):
    """
    Lightweight CO2 estimation function
    Replaces ML inference for deployment stability
    """
    base_co2 = 400  # baseline ppm
    co2 = base_co2 + (pm25 * 2) + (temp * 3) + (people * 20)
    return round(co2, 2)

# =========================
# PREDICTION ROUTE
# =========================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ensure JSON exists
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()

        # Safe extraction with defaults
        pm25 = float(data.get('pm25', 50))
        temp = float(data.get('temp', 25))
        people = int(data.get('people', 1))

        # Compute CO2
        co2_value = calculate_co2(pm25, temp, people)

        # Condition classification
        if co2_value < 600:
            condition = "Safe"
        elif co2_value < 1000:
            condition = "Warning"
        else:
            condition = "Critical"

        # Ventilation logic
        ventilation = "ON" if co2_value > 800 else "OFF"

        # Response
        return jsonify({
            "co2": co2_value,
            "condition": condition,
            "ventilation": ventilation
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

# =========================
# RUN SERVER (RENDER SAFE)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)