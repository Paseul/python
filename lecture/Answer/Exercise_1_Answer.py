import tensorflow as tf
import numpy as np
from tensorflow import keras
model = keras.models.Sequential([
    keras.layers.Dense(1)
])
model.compile(
    optimizer= 'sgd',
    loss='mse')
xs = np.array([1, 2, 3, 4, 5])
ys = np.array([100, 150, 200, 250, 300])
model.fit(xs, ys, epochs=500)

print(model.predict([7.0]))

model.save('exercise1.h5')
# It can be used to reconstruct the model identically.
reconstructed_model = keras.models.load_model("exercise1.h5")
print(reconstructed_model.predict([7.0]))