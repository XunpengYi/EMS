import os
import argparse
import cv2


def create_output_dirs(lr_img_dir):
    os.makedirs(os.path.join(lr_img_dir, "X2"), exist_ok=True)
    os.makedirs(os.path.join(lr_img_dir, "X4"), exist_ok=True)


def is_supported_format(filename):
    supported_img_formats = (".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2",
                             ".png", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tif",
                             ".tiff")
    return filename.endswith(supported_img_formats)


def downsample_and_save(hr_img, filename, lr_img_dir):
    # GaussianBlur + downsample
    hr_img_blurred = cv2.GaussianBlur(hr_img, (0, 0), 1, 1)

    # 2x downsampling
    lr_image_2x = cv2.resize(hr_img_blurred, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    lr_image_2x = cv2.resize(lr_image_2x, (hr_img.shape[1], hr_img.shape[0]), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(lr_img_dir, "X2", filename), lr_image_2x)

    # 4x downsampling
    lr_image_4x = cv2.resize(hr_img_blurred, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
    lr_image_4x = cv2.resize(lr_image_4x, (hr_img.shape[1], hr_img.shape[0]), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(lr_img_dir, "X4", filename), lr_image_4x)


def main():
    parser = argparse.ArgumentParser(description='Downsize images at 2x/4x using bicubic interpolation')
    parser.add_argument("-k", "--keepdims", action="store_true",help="keep original image dimensions in downsampled images")
    parser.add_argument('--hr_img_dir', type=str, default='', help='path to high resolution image dir')
    parser.add_argument('--lr_img_dir', type=str, default='',
                        help='path to desired output dir for downsampled images')
    args = parser.parse_args()

    hr_image_dir = args.hr_img_dir
    lr_image_dir = args.lr_img_dir

    create_output_dirs(lr_image_dir)

    for filename in os.listdir(hr_image_dir):
        if not is_supported_format(filename):
            continue

        hr_img = cv2.imread(os.path.join(hr_image_dir, filename))
        if hr_img is None:
            print(f"Error loading image: {filename}")
            continue

        downsample_and_save(hr_img, filename, lr_image_dir)

if __name__ == "__main__":
    main()