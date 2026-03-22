from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Initialize app
app = Flask(__name__)
CORS(app)  # 🔥 IMPORTANT FIX

# Load model
model = load_model("model.h5", compile=False)

# Scaler
scaler = MinMaxScaler()

# CO2 estimation function
def estimate_co2(pm25, temp, people):
    return 400 + (pm25 * 2) + (temp * 3) + (people * 20)

# Root route (optional but removes 404 confusion)
@app.route("/")
def home():
    return "CO2 AI Backend Running 🚀"

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        pm25 = float(data.get("pm25", 0))
        temp = float(data.get("temp", 0))
        people = int(data.get("people", 1))

        # Create sequence of 24 values
        sequence = [pm25] * 24
        seq_array = np.array(sequence).reshape(-1, 1)

        # Normalize
        scaled = scaler.fit_transform(seq_array)
        input_seq = scaled.reshape(1, 24, 1)

        # Predict
        pred = model.predict(input_seq, verbose=0)
        pred_pm = scaler.inverse_transform(pred)[0][0]

        # Convert to CO2
        co2 = estimate_co2(pred_pm, temp, people)

        return jsonify({
            "predicted_pm25": float(pred_pm),
            "co2": float(co2),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        })

# Run server
if __name__ == "__main__":
    app.run(debug=True)