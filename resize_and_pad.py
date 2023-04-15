from PIL import Image
import os
import argparse


def resize_and_pad_images(args):
    """
    Resizes all images in the input folder to the specified size with padding if necessary and saves them in the output folder.

    Args:
        args (argparse.Namespace): Namespace object containing command-line arguments.

    Raises:
        IOError: If an input file cannot be opened.
        OSError: If the output folder does not exist or cannot be created.

    Returns:
        None
    """
    # Loop through all the files in the input folder
    for filename in os.listdir(args.input_path):
        try:
            # Open the file using PIL
            img = Image.open(os.path.join(args.input_path, filename))

            # Calculate the new size of the canvas
            img_width, img_height = img.size
            ratio = img_width / img_height
            if img_width > img_height:
                img_width = args.size[0]
                img_height = int(args.size[0] / ratio)
            else:
                img_width = int(args.size[0] * ratio)
                img_height = args.size[0]

            # Calculate the position of the image in the canvas
            x = (args.size[0] - img_width) // 2
            y = (args.size[1] - img_height) // 2

            # Create a new image with white background
            new_img = Image.new("RGB", args.size, (255, 255, 255))

            # Paste the image in the canvas with white padding
            new_img.paste(img.resize(
                (img_width, img_height), Image.ANTIALIAS), (x, y))

            # Save the new image with the same filename in the output folder
            new_img.save(os.path.join(args.output_path, filename))
        except (IOError, OSError):
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Resize and pad images in a folder.')
    parser.add_argument('--input_path', type=str, required=True,
                        help='Path to the folder containing input images.')
    parser.add_argument('--output_path', type=str, required=True,
                        help='Path to the folder where output images will be saved.')
    parser.add_argument('--size', type=int, nargs=2, default=(512, 512),
                        help='A tuple containing the desired width and height of the output images. Default is (512, 512).')

    args = parser.parse_args()

    resize_and_pad_images(args)
