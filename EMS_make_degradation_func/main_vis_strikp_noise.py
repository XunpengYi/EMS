import cv2
import os
import numpy as np

def add_stripe(image_path):
    im = cv2.imread(image_path)

    stdN_G = np.random.uniform(3, 5) # random value
    noise_G= np.random.normal(0, stdN_G, im.shape)

    beta = np.random.uniform(3, 8)  # strikp value
    noise_col = np.random.normal(0, beta, im.shape[1])

    S_noise = np.tile(noise_col, (im.shape[0], 1))
    S_noise = np.stack([S_noise, S_noise, S_noise], axis=2)

    return im+1 * noise_G + 1 * S_noise  # noise_G is not necessary

input_folder = ''
output_folder = ''

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        enhanced_image = add_stripe(input_path)
        cv2.imwrite(output_path, enhanced_image)
        print(f"Random noise added to {filename} and saved to {output_path}")