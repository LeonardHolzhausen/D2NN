import numpy as np
import cmath

import tensorflow as tf
from sklearn.model_selection import train_test_split

import dataset
import globals


class DiffractiveSimulationLayer:

    def __init__(self, image_size, refine_size=128):

        self.N = image_size
        self.refine_size = refine_size
        self.pad_size = refine_size // 2

        self.wave_length = 532E-9 #Green laser light
        self.p = 150E-6 #pitch

        self.z = (self.N * self.p**2) / self.wave_length

        self.delays = tf.Variable(
            tf.random.uniform(
                shape=(self.N, self.N),
                minval=0.0,
                maxval=cmath.pi / 2,
                dtype=tf.float32
            )
        )

        self.H = tf.constant(self.simulation_setup(), dtype=tf.complex64) #Needs to be cached before actual training (after all tests (D2NN_tests.py) return positive).

    def simulation_setup(self):

        frequencies = self.get_fft_frequencies()
        H_array = self.transform_to_propagation_array(*frequencies)

        return H_array

    def refine_image(self, image, complex=False):
        """
        Refine the image up to 'size' 
        (16x16 image becomes for example 128x128 image, one pixel taking up an 8x8 block of space in the matrix)
        """

        refined_image = np.zeros(
                (self.refine_size, self.refine_size),
                dtype=np.float64
        )

        for row in range(self.N):
            for col in range(self.N):
                refined_image[((self.refine_size // self.N) * row):((self.refine_size // self.N)* (row + 1)), ((self.refine_size // self.N) * col):((self.refine_size // self.N)* (col + 1))] = image[row][col]

        if complex:
            return tf.complex(tf.constant(refined_image, dtype=tf.float32), tf.zeros_like(refined_image, dtype=tf.float32))

        return refined_image

    def pad_image(self, image, complex=False):

        if complex == False:

            empty_grid = np.zeros(
                    (self.pad_size * 4, self.pad_size * 4),
                    dtype=np.float64
                    )

            #Place the (refined) image into an empty patted grid of double the size of the (refined) image
            empty_grid_length = len(empty_grid[0])

            for row in range(empty_grid_length):
                for col in range(empty_grid_length):
                    if 1/4 * empty_grid_length <= row < 3/4 * empty_grid_length and 1/4 * empty_grid_length <= col < 3/4 * empty_grid_length:
                        empty_grid[row][col] = image[row - 64][col - 64]

            return empty_grid

        return tf.pad(
            image,
            paddings=[ # Padding of half the refined image width, doubling the image size (128x128 -> 256x256)
                [self.pad_size, self.pad_size],
                [self.pad_size, self.pad_size]
            ]
        )

    def get_fft_frequencies(self):

        n = self.pad_size * 4
        d = self.p / (self.refine_size // self.N)
        freq = np.fft.fftfreq(n, d=d)
        fx, fy = np.meshgrid(freq, freq)

        return fx, fy

    def transform_to_propagation_array(self, fx, fy):

        H_array = []

        for row in range(len(fx)):
            for col in range(len(fy)):
                if ((1/self.wave_length)**2 - fx[row, col]**2 - fy[row, col]**2) < 0:
                    H = 0
                    H_array.append(H)
                else:
                    H = cmath.exp(2 * cmath.pi * 1j * self.z * cmath.sqrt((1/self.wave_length)**2 - fx[row, col]**2 - fy[row, col]**2))
                    H_array.append(H)

        H_array = np.array(H_array)
        H_array = H_array.reshape(fx.shape)

        return H_array

    def B1(self, image):

        light_field = self.refine_image(image, complex=True)
        patted_light_field = self.pad_image(light_field, complex=True)

        return patted_light_field

    def B2(self, light_field):

        refined_delays = tf.repeat(tf.repeat(self.delays, self.refine_size // self.N, axis=0), self.refine_size // self.N, axis=1)
        patted_delays = self.pad_image(refined_delays, complex=True)

        complex_grid = tf.complex(
            tf.zeros_like(patted_delays),
            patted_delays
        )

        return light_field * tf.exp(complex_grid)

    def B3(self, field):

        spectrum = tf.signal.fft2d(field)
        propagated_field = spectrum * self.H
        return tf.signal.ifft2d(propagated_field)

    def B4(self, field):

        return tf.abs(field) ** 2

def forward(layers, image):
    
    field = layers[0].B1(image)
    for layer in layers:
        field = layer.B2(field)
        field = layer.B3(field)
    brightness = layers[-1].B4(field)
    region_sums = read_output_regions(brightness)
    return region_sums / (tf.reduce_sum(region_sums) + 1e-8)

def train_step(layers, image, label, optimizer, temperature=20.0):

    with tf.GradientTape() as tape:
        probs = tf.nn.softmax(forward(layers, image) * temperature)
        loss = tf.keras.losses.sparse_categorical_crossentropy(
            tf.constant([label]), tf.expand_dims(probs, 0)
        )[0]
    trainable_vars = [layer.delays for layer in layers]
    grads = tape.gradient(loss, trainable_vars)
    optimizer.apply_gradients(zip(grads, trainable_vars))
    return loss

def read_output_regions(brightness_image, center=128, half=10, gap=4):

    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 2x2 arrangement, close together
    sums = []
    for dr, dc in offsets:
        r0 = center + dr * (half + gap) - half
        c0 = center + dc * (half + gap) - half
        sums.append(tf.reduce_sum(brightness_image[r0:r0+2*half, c0:c0+2*half]))
    return tf.stack(sums)

def train(epochs, X_train, y_train, layers=4, optimizer=tf.keras.optimizers.Adam(learning_rate=0.05)):

    for epoch in range(epochs):
        epoch_loss = 0

        for image, label in zip(X_train, y_train):
            loss = train_step(layers, image, label, optimizer)
            epoch_loss += float(loss)

        print(epoch, epoch_loss / len(X_train))
    
def evaluate(X_test, y_test, layers=4):

    accuracy = 0
    total_loss = 0

    for image, label in zip(X_test, y_test):
        probs = forward(layers, image)
        predicted = int(tf.argmax(probs).numpy())
        accuracy += int(predicted == label)
        total_loss += float(tf.keras.losses.sparse_categorical_crossentropy(
            tf.constant([label]), tf.expand_dims(probs, 0)
        )[0])

    val_accuracy = accuracy / len(X_test)
    val_loss = total_loss / len(X_test)

    return val_accuracy, val_loss

if __name__ == "__main__":

    # Get the dataset training data
    data = dataset.Dataset(4000, image_size=globals.IMAGE_SIZE, seed=42)
    X = np.array([s["image"] for s in data.dataset], dtype="float32")
    y = np.array([s["label"] for s in data.dataset])    # integer labels 0-3

    # Remove duplicates BEFORE splitting
    _, unique_idx = np.unique(X.reshape(len(X), -1), axis=0, return_index=True)
    X, y = X[unique_idx], y[unique_idx]
    
    # Balance the classes
    counts = np.bincount(y)
    k = counts.min()
    rng = np.random.default_rng(0)
    keep = np.concatenate([rng.choice(np.where(y == c)[0], k, replace=False)
                        for c in range(4)])
    X, y = X[keep], y[keep]
    print(f"{len(X)} images after dedup + balancing ({k} per class)")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numbers_of_layers = 3
    layers = [DiffractiveSimulationLayer(globals.IMAGE_SIZE) for _ in range(numbers_of_layers)]

    train(30, X_train, y_train, layers)
    accuracy, avg_loss = evaluate(X_test, y_test, layers)
    print(f'test accuracy: {accuracy:.3f}   test loss: {avg_loss:.4f}')