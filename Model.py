import numpy as np
from tensorflow.keras.models import load_model

model = load_model("model.h5", compile=False)

sample = np.random.rand(24,1)
sample = sample.reshape(1,24,1)

prediction = model.predict(sample)

print("Predicted CO2 Level:", prediction)