import tensorflow as tf
import os
import zipfile


DESIRED_ACCURACY = 0.999

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs['accuracy']>DESIRED_ACCURACY):
            print("Reached 99.9% accuracy so cancelling training!")
            self.model.stop_training = True
  # Your Code

callbacks = myCallback()

# This Code Block should Define and Compile the Model
model = tf.keras.models.Sequential([
# Your Code Here
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

from tensorflow.keras.optimizers import RMSprop

model.compile(optimizer= RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# This code block should create an instance of an ImageDataGenerator called train_datagen
# And a train_generator by calling train_datagen.flow_from_directory

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255 #,
    # rotation_range=30,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    # horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    'h-or-s',
    target_size=(150, 150),
    batch_size=10,
    class_mode='binary'
)

# Expected output: 'Found 80 images belonging to 2 classes'

# This code block should call model.fit and train for
# a number of epochs.
history = model.fit(train_generator, steps_per_epoch=8, epochs=100, callbacks=[callbacks])

# Expected output: "Reached 99.9% accuracy so cancelling training!""