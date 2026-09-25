import random

import cv2
import numpy as np

SHAPE_NAMES = ["circle", "square", "triangle", "plus"]


class Dataset:
    def __init__(self, dataset_size, image_size=16, seed=None):
        self.dataset_size = dataset_size
        self.image_size = image_size
        self.dataset = []

        self.center = (image_size - 1) // 2
        self.min_size = image_size // 8
        # The largest radius/half-size that still leaves at least one
        # valid center position inside the image (see generate_circle).
        self.max_size = (image_size - 1) // 2

        self.rng = random.Random(seed)
        self.generate_dataset()

    def generate_dataset(self):
        for _ in range(self.dataset_size):
            shape = self.rng.randint(1, 4)
            image = np.zeros(
                (self.image_size, self.image_size),
                dtype=np.uint8
            )

            if shape == 1:
                cv2.circle(image, *self.generate_circle())
            elif shape == 2:
                cv2.rectangle(image, *self.generate_square())
            elif shape == 3:
                cv2.drawContours(image, *self.generate_triangle())
            elif shape == 4:
                cv2.drawContours(image, *self.generate_plus_sign())

            self.dataset.append({
                "image": image,
                # 0-indexed label for direct use as a classifier target.
                "label": shape - 1,
                "label_name": SHAPE_NAMES[shape - 1]
            })

    def generate_circle(self):

        radius = self.rng.randint(self.min_size, self.max_size)

        # The center must leave room for the radius on every side --
        # this is what makes the position actually vary across the
        # full image instead of being confined to one region.
        center_coordinates_x = self.rng.randint(radius, self.image_size - 1 - radius)
        center_coordinates_y = self.rng.randint(radius, self.image_size - 1 - radius)
        center_coordinates = (center_coordinates_x, center_coordinates_y)

        return center_coordinates, radius, 1, -1  # thickness = -1 (filled), color = 1

    def generate_square(self):

        # half_size plays the same role as the circle's radius: the
        # distance from the square's own center to each of its edges.
        half_size = self.rng.randint(self.min_size, self.max_size)

        center_x = self.rng.randint(half_size, self.image_size - 1 - half_size)
        center_y = self.rng.randint(half_size, self.image_size - 1 - half_size)

        start_coordinates = (center_x - half_size, center_y - half_size)
        end_coordinates = (center_x + half_size, center_y + half_size)

        return start_coordinates, end_coordinates, 1, -1

    def generate_triangle(self):

        # Capped at max_size, matching the other three shapes' scale
        # ceiling instead of allowing triangles up to the full canvas.
        base = self.rng.randint(self.min_size, self.max_size)
        height = self.rng.randint(self.min_size, self.max_size)

        point1_x = self.rng.randint(0, self.image_size - 1 - base)
        point1_y = self.rng.randint(height, self.image_size - 1)
        point1 = (point1_x, point1_y)

        point2_x = point1_x + base
        point2_y = point1_y
        point2 = (point2_x, point2_y)

        point3_x = point1_x + base // 2
        point3_y = point1_y - height
        point3 = (point3_x, point3_y)

        contour = np.array(
            [point1, point2, point3]
        )

        return [contour], 0, 1, -1

    def generate_plus_sign(self):

        size = self.rng.randint(self.min_size, self.max_size)
        side_length = self.rng.randint(size // 6, size // 3)

        # A random center, leaving room for the arms on every side --
        # the same treatment as circle/square, instead of being pinned
        # to the canvas center on every single sample.
        center_x = self.rng.randint(size, self.image_size - 1 - size)
        center_y = self.rng.randint(size, self.image_size - 1 - size)

        corner1 = (center_x - size, center_y - side_length // 2)
        corner2 = (center_x - size, center_y + side_length // 2)
        vertice1 = (center_x - side_length // 2, center_y + side_length // 2)
        corner3 = (center_x - side_length // 2, center_y + size)
        corner4 = (center_x + side_length // 2, center_y + size)
        vertice2 = (center_x + side_length // 2, center_y + side_length // 2)
        corner5 = (center_x + size, center_y + side_length // 2)
        corner6 = (center_x + size, center_y - side_length // 2)
        vertice3 = (center_x + side_length // 2, center_y - side_length // 2)
        corner7 = (center_x + side_length // 2, center_y - size)
        corner8 = (center_x - side_length // 2, center_y - size)
        vertice4 = (center_x - side_length // 2, center_y - side_length // 2)

        contour = np.array(
            [corner1, corner2, vertice1, corner3, corner4, vertice2,
             corner5, corner6, vertice3, corner7, corner8, vertice4]
        )

        return [contour], 0, 1, -1