import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load dataset
data = pd.read_csv("BeijingDataset.csv")

# Select CO2 related column (or proxy sensor)
values = data.iloc[:, 2].values.reshape(-1,1)

# Normalize
scaler = MinMaxScaler()
scaled = scaler.fit_transform(values)

# Create time series sequences
X = []
y = []

window = 24

for i in range(window, len(scaled)):
    X.append(scaled[i-window:i])
    y.append(scaled[i])

X = np.array(X)
y = np.array(y)

# Train test split
split = int(len(X)*0.8)

X_train = X[:split]
y_train = y[:split]

X_test = X[split:]
y_test = y[split:]

# Build LSTM model
model = Sequential()

model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(
    optimizer='adam',
    loss='mse'
)

# Train
model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32
)

# Save model
model.save("model.h5")

# Predictions
pred = model.predict(X_test)

pred = scaler.inverse_transform(pred)
y_test = scaler.inverse_transform(y_test)

# Plot
plt.plot(y_test,label="Actual CO2")
plt.plot(pred,label="Predicted CO2")
plt.legend()
plt.show()