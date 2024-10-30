import os
import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, std=20):
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image

def add_poisson_noise(image):
    noisy_image = np.random.poisson(image / 255.0 * 80) / 80 * 255
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image

def add_salt_and_pepper_noise(image, salt_prob=0.000003, pepper_prob=0.000001):
    noisy_image = np.copy(image)
    salt_mask = np.random.rand(*image.shape) < salt_prob
    pepper_mask = np.random.rand(*image.shape) < pepper_prob
    noisy_image[salt_mask] = 255
    noisy_image[pepper_mask] = 0
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
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Add noise
        noisy_image_gaussian = add_gaussian_noise(image)
        noisy_image_poisson = add_poisson_noise(noisy_image_gaussian)
        noisy_image_salt_pepper = add_salt_and_pepper_noise(noisy_image_poisson)

        # Save noisy image
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, noisy_image_salt_pepper)
        print(f"Noise added to {filename} and saved to {output_path}")