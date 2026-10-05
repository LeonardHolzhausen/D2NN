import globals
import D2NN

import numpy as np
import tensorflow as tf

#All tests must pass given the margin of error (should be around 1 %) before desigining physical parts.
class Tests:

    def __init__(self, images, margin_of_error=0.01):

        self.images = images
        self.margin_of_error = margin_of_error # Usually 1 %
        self.layers = [D2NN.DiffractiveSimulationLayer(globals.IMAGE_SIZE) for _ in range(3)]
        
    def run_all(self):
        pass

    def run_one(self, test_number):
        pass

    # Test to see if energy stays conserved in the system (Both more and less energy in the system after propagation are possible, both mean different errors)
    def energy_conservation_test(self):

        for image in self.images:
            # Get the total brigthness of two fields, one  of the fields must propagate to test for energy conservation
            field = self.layers[0].B1(image)
            field = self.layers[0].B2(field)
            field1_brightness = tf.reduce_sum(tf.abs(field) ** 2)

            field = self.layers[0].B3(field)
            field = self.layers[1].B2(field)
            field2_brightness = tf.reduce_sum(tf.abs(field) ** 2)

            difference = field1_brightness / field2_brightness

            if 1 + self.margin_of_error < difference or difference < 1 - self.margin_of_error: # Slight energy loss at the set percentage of margin_of_error is allowed
                return "ENERGY_CONSERVATON_TEST_FAIL"
            
        return

    def diffraction_pattern_test(self):

        image = np.zeros(
            (self.layers[0].N, self.layers[0].N),
            dtype=np.uint8
        )

        center_x = self.layers[0].N // 2
        center_y = self.layers[0].N // 2

        image[center_x][center_y] = 1

        # Temporarily double the value of z for the easier calculations of dark spot on the propagated field
        original_z = self.layers[0].z
        self.layers[0].z /= 2

        H_half = self.layers[0].simulation_setup()

        original_H = self.layers[0].H
        self.layers[0].H = H_half

        field = self.layers[0].B1(image)

        field = self.layers[0].B2(field)
        field = self.layers[0].B3(field)

        intensity = self.layers[-1].B4(field)

        intensity_centre_right_line = intensity[131, 131:]
        intensity_centre_left_line = intensity[131, :131][::-1]

        distance = 0

        # Search the side right from the center
        for i in range(len(intensity_centre_right_line)):
            if intensity_centre_right_line[i - 1] > intensity_centre_right_line[i] < intensity_centre_right_line[i + 1]:
                distance_to_local_minima_right = distance * globals.P / 8
                distance = 0
                break

            distance += 1

        # Search the side left from the center
        for i in range(len(intensity_centre_left_line)):
                    if intensity_centre_left_line[i - 1] > intensity_centre_left_line[i] < intensity_centre_left_line[i + 1]:
                        distance_to_local_minima_left = distance * globals.P / 8
                        distance = 0
                        break
        
                    distance += 1

        distance_to_local_minima = (distance_to_local_minima_right + distance_to_local_minima_left) / 2

        calculated_distance = (globals.WAVELENGTH * (self.layers[0].z / 2)) / globals.P

        difference = distance_to_local_minima / calculated_distance

        self.layers[0].z = original_z
        self.layers[0].H = original_H

        if 1 + (self.margin_of_error * 3) < difference or difference < 1 - (self.margin_of_error * 3): #Margin of error needs to be bigger because the grid is not refined enough (Row of 256 pixel with) 
            return "DIFFRACTION_PATTERN_TEST_FAIL"

        return

    # Propagate by distance z and reverse the propagation by -z, original field must remain the same.
    def forward_backward_test(self):

        for image in self.images:
            field = self.layers[0].B1(image)
            original_field = self.layers[0].B2(field)
            propagated_field = self.layers[0].B3(original_field)

            # Temporarily reverse the value of z for the reverse angular spectrum calculation on the propagated field
            original_z = self.layers[0].z
            self.layers[0].z = - self.layers[0].z

            H_inverse = self.layers[0].simulation_setup()

            original_H = self.layers[0].H
            self.layers[0].H = H_inverse
            
            backward_propagated_field = self.layers[0].B3(propagated_field)

            self.layers[0].z = original_z
            self.layers[0].H = original_H

            difference = tf.reduce_max(abs(backward_propagated_field)) / tf.reduce_max(abs(original_field))

            if 1 + self.margin_of_error < difference or difference < 1 - self.margin_of_error:
                return "FORWARD_BACKWARD_TEST_FAIL"

        return

    def A_grating_test(self):

        # Temporarily set delays to a constant alternation of 0 and π
        original_delays = self.layers[0].delays
        pattern = tf.constant([
            0,
            np.pi
        ])
        self.layers[0].delays.assign(pattern)

        for image in self.images:
            field = self.layers[0].B1(image)
            field = self.layers[0].B2(field)
            far_field = self.layers[0].B3(field)

            intensity = tf.abs(far_field) ** 2
            threshold = 0.05 * tf.reduce_max(intensity) # 5 % of peak intensity
            bright_field = intensity > threshold

            coords = tf.where(bright_field)

    def resolution_padding_test(self):

        for image in self.images:
            field1 = self.layers[0].B1(image)

            #Propagate fully without any changes and save the outcoming intensity
            for layer in self.layers:
                field1 = layer.B2(field1)
                field1 = layer.B3(field1)

            intensity1 = self.layers[-1].B4(field1)

            # Temporarily double the refine_size to test for image coarsness, adjustment of new pad_size for new refine_size
            original_refine_size = self.layers[0].refine_size
            original_pad_size = self.layers[0].pad_size
            original_H = self.layers[0].H

            for layer in self.layers: 
                layer.refine_size *= 2
                layer.pad_size = original_refine_size # Original_refine_size = new_refine_size // 2 = new_pad_size

                H_inverse = self.layers[0].simulation_setup()
                self.layers[0].H = H_inverse

            # propagate again with new refine_size
            field2 = self.layers[0].B1(image)

            for layer in self.layers:
                field2 = layer.B2(field2)
                field2 = layer.B3(field2)

            intensity2 = self.layers[-1].B4(field2)

            difference = intensity1 / intensity2

            if 1 + self.margin_of_error < difference or difference < 1 - self.margin_of_error: # Slight energy loss at the set percentage of margin_of_error is allowed
                for layer in self.layers: 
                    layer.refine_size = original_refine_size
                    layer.pad_size = original_pad_size
                    layer.H = original_H
                return "HIGHER_RESOLUTION_TEST_FAIL"

             # Temporarily double the pad_size to test for light wrapping around the egdes, keep the doubled refined_size
            for layer in self.layers: 
                layer.pad_size *= 2
            
                H_inverse = self.layers[0].simulation_setup()
                self.layers[0].H = H_inverse

            # propagate again with new pad_size
            field3 = self.layers[0].B1(image)

            for layer in self.layers:
                field3 = layer.B2(field3)
                field3 = layer.B3(field3)

            intensity3 = self.layers[-1].B4(field3)

            difference = intensity1 / intensity3

            if 1 + self.margin_of_error < difference or difference < 1 - self.margin_of_error: # Slight energy loss at the set percentage of margin_of_error is allowed
                for layer in self.layers: 
                    layer.refine_size = original_refine_size
                    layer.pad_size = original_pad_size
                    layer.H = original_H
                return "HIGHER_PADDING_TEST_FAIL"

        return