import tensorflow as tf
import numpy as np

# mnist = tf.keras.datasets.mnist
#
# (x_train, y_train), (x_test, y_test) = mnist.load_data()

path = tf.keras.utils.get_file('mnist.npz', 'dataset/mnist.npz')
data = np.load(path)

class myCallbacks(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('accuracy')>0.99):
            print("\nReached 99% accuracy so cancelling training!")
            self.model.stop_training=True

callbacks = myCallbacks()
x_train, x_test = data['x_train'] / 255.0, data['x_test'] / 255.0
# YOUR CODE SHOULD END HERE
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(256, activation=tf.nn.relu),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# YOUR CODE SHOULD START HERE
model.fit(x_train, data['y_train'], epochs=10, callbacks=[callbacks])
# YOUR CODE SHOULD END HERE