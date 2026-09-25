import numpy as np
import cmath
import tensorflow as tf

import dataset


class DiffractiveSimulationLayer:

    def __init__(self, image_size, refine_size=128):

        self.N = image_size
        self.refine_size = refine_size

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

        self.H = tf.constant(self.simulation_setup(), dtype=tf.complex64)

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
                    (2*self.refine_size, 2*self.refine_size),
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
                [self.refine_size // 2, self.refine_size // 2],
                [self.refine_size // 2, self.refine_size // 2]
            ]
        )

    def get_fft_frequencies(self):

        n = self.refine_size * 2
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

    def B1(self, image): #refine size must be the same as in the previous functions

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

# Get the dataset training data
image_size=16
data = dataset.Dataset(4000, image_size=16, seed=42)
X = np.array([s["image"] for s in data.dataset], dtype="float32")
y = np.array([s["label"] for s in data.dataset])    # integer labels 0-3

# Simulation forward pass logic (only logic so far!)
simulation = DiffractiveSimulationLayer(image_size)
starting_pattern = simulation.B1(image)

layer1_sim = DiffractiveSimulationLayer(image_size)
layer1 = layer1_sim.B2(starting_pattern)
propagated_layer = layer1_sim.B3(layer1)

layer2_sim = DiffractiveSimulationLayer(image_size)
layer2 = layer2_sim.B2(propagated_layer)
propagated_layer = layer2_sim.B3(layer2)

layer3_sim = DiffractiveSimulationLayer(image_size)
layer3 = layer3_sim.B2(propagated_layer)
propagated_layer = layer3_sim.B3(layer3)

output = simulation.B4(layer3)