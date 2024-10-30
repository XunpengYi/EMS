import cv2
import numpy as np


def get_noise(img, value=10):
    noise = np.random.uniform(0, 256, img.shape[0:2])

    v = value * 0.01
    noise[np.where(noise < (256 - v))] = 0
    k = np.array([[0, 0.1, 0],
                  [0.1, 8, 0.1],
                  [0, 0.1, 0]])

    noise = cv2.filter2D(noise, -1, k)
    return noise


def rain_blur(noise, length=10, angle=0, w=1):
    trans = cv2.getRotationMatrix2D((length / 2, length / 2), angle - 45, 1 - length / 100.0)
    dig = np.diag(np.ones(length))
    k = cv2.warpAffine(dig, trans, (length, length))
    k = cv2.GaussianBlur(k, (w, w), 0)

    blurred = cv2.filter2D(noise, -1, k)

    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred


def alpha_rain(rain, img, beta=0.8):
    rain = np.expand_dims(rain, 2)
    rain_effect = np.concatenate((img, rain), axis=2)
    rain_result = img.copy()
    rain = np.array(rain, dtype=np.float32)
    rain_result[:, :, 0] = rain_result[:, :, 0] * (255 - rain[:, :, 0]) / 255.0 + beta * rain[:, :, 0]
    rain_result[:, :, 1] = rain_result[:, :, 1] * (255 - rain[:, :, 0]) / 255 + beta * rain[:, :, 0]
    rain_result[:, :, 2] = rain_result[:, :, 2] * (255 - rain[:, :, 0]) / 255 + beta * rain[:, :, 0]


def add_rain(rain, img, alpha=0.9):
    rain = np.expand_dims(rain, 2)
    rain = np.repeat(rain, 3, 2)
    result = cv2.addWeighted(img, alpha, rain, 1 - alpha, 1)


import os
import random
def add_rain_folder(input_folder, output_folder, alpha=0.9, beta=0.8, value=500, length=50, angle=-30, w=3):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            angle = random.uniform(-45, 45)
            add_rain_to_image(input_path, output_path, alpha, beta, value, length, angle, w)


def add_rain_to_image(input_path, output_path, alpha=0.9, beta=0.6, value=500, length=50, angle=-30, w=3):
    img = cv2.imread(input_path)
    noise = get_noise(img, value)
    rain = rain_blur(noise, length, angle, w)
    rain = np.expand_dims(rain, 2)
    rain = np.repeat(rain, 3, 2)
    result = cv2.addWeighted(img, alpha, rain, 1 - alpha, beta)
    cv2.imwrite(output_path, result)


if __name__ == '__main__':
    input_folder = ''
    output_folder = ''

    add_rain_folder(input_folder, output_folder)