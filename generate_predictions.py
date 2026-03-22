import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load model
model = load_model("model.h5", compile=False)

# Load dataset
data = pd.read_csv("BeijingDataset.csv")
print(data.columns.tolist())

# Use one numeric column (sensor reading)
values = data["pm2.5"].dropna().values.reshape(-1,1)

# Clean missing values
values = values[~np.isnan(values)]

scaler = MinMaxScaler()
scaled = scaler.fit_transform(values.reshape(-1,1))

window = 24

predictions = []
actual = []

for i in range(window, len(scaled)):

    seq = scaled[i-window:i].reshape(1,window,1)

    pred = model.predict(seq, verbose=0)

    pred_real = scaler.inverse_transform(pred)[0][0]
    actual_real = scaler.inverse_transform([[scaled[i][0]]])[0][0]

    predictions.append(pred_real)
    actual.append(actual_real)

df = pd.DataFrame({
    "Actual_CO2": actual,
    "Predicted_CO2": predictions
})

df.to_csv("website/predictions.csv", index=False)

print("Predictions exported to website folder")