import os
import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, std=10):
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image

def add_poisson_noise(image):
    value = np.random.randint(70, 91)
    noisy_image = np.random.poisson(image / 255.0 * value) / value * 255
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image


# Input and output directories
input_dir = ''
output_dir = ''

# Create output directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all image files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.png') or filename.endswith('.jpg'):  # Adjust extensions as needed
        # Load image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        # Add noise
        noisy_image_gaussian = add_gaussian_noise(image)
        noisy_image_poisson = add_poisson_noise(noisy_image_gaussian)
        # Save noisy image
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, noisy_image_poisson)
        print(f"Random noise added to {filename} and saved to {output_path}")