import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load trained model
model = load_model("model.h5", compile=False)

# Load dataset (same dataset used for training)
data = pd.read_csv("AirQualityUCI.csv")

values = data.iloc[:,2].values.reshape(-1,1)

# Normalize
scaler = MinMaxScaler()
scaled = scaler.fit_transform(values)

window = 24

# Initial sequence
sequence = scaled[:window]

predictions = []
actual = []

print("Starting Real-Time CO2 Prediction...\n")

for i in range(window, len(scaled)):

    input_seq = sequence.reshape(1,window,1)

    # Predict next CO2 value
    pred = model.predict(input_seq, verbose=0)

    # Convert back to real value
    pred_real = scaler.inverse_transform(pred)[0][0]
    actual_real = scaler.inverse_transform(scaled[i].reshape(1,-1))[0][0]

    predictions.append(pred_real)
    actual.append(actual_real)

    print(f"Actual CO2: {actual_real:.2f} | Predicted CO2: {pred_real:.2f}")

    # Ventilation logic
    if pred_real > 800:
        print("⚠ Ventilation ON (High CO2)")
    else:
        print("✓ Air Quality Normal")

    print("-----------------------")

    # Update sequence
    sequence = np.append(sequence[1:], scaled[i])

    # Simulate real-time sensor delay
    time.sleep(1)

# Plot results
plt.plot(actual,label="Actual CO2")
plt.plot(predictions,label="Predicted CO2")
plt.legend()
plt.title("Real-Time CO2 Prediction")
plt.show()