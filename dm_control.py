from astropy.io import fits
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

dmCommand = fits.open('data/dmCommands.fits')
wfs_frames_00 = fits.open('data/wfs_frames_00.fits')
sciPsfInst_00 = fits.open('data/sciPsfInst_00.fits')
sciResidual_00 = fits.open('data/sciResidual_00.fits')
slopes = fits.open('data/slopes.fits')

print(dmCommand.info())
print(slopes.info())
print(dmCommand[0].data[1])

plt.figure(1)
plt.imshow(wfs_frames_00[0].data[100])
plt.show()

# images = np.array(sciResidual_00[0].data)
# images =  np.expand_dims(images, axis=3)
# images = images/255.0
# labels = np.array(dmCommand[0].data)
#
# split = 1000
# train_images = images[:split]
# train_labels = labels[:split]
# val_images = images[split:]
# val_labels = labels[split:]
#
# model = tf.keras.models.Sequential([
#   tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(102, 102, 1)),
#   tf.keras.layers.MaxPooling2D(2,2),
#   tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
#   tf.keras.layers.MaxPooling2D(2,2),
#   tf.keras.layers.Flatten(),
#   tf.keras.layers.Dense(128, activation='relu'),
#   tf.keras.layers.Dense(83, activation='softmax')
# ])
#
# # Compile Model.
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Train the Model
# history=model.fit(
#     train_images,
#     train_labels,
#     epochs=100
# )
