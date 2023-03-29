from PIL import Image
import os


def resize_and_pad_images(input_path: str, output_path: str, size: tuple = (512, 512)) -> None:
    """
    Resizes all images in the input folder to the specified size with padding if necessary and saves them in the output folder.

    Args:
        input_path (str): Path to the folder containing input images.
        output_path (str): Path to the folder where output images will be saved.
        size (tuple, optional): A tuple containing the desired width and height of the output images. Defaults to (512, 512).

    Raises:
        IOError: If an input file cannot be opened.
        OSError: If the output folder does not exist or cannot be created.

    Returns:
        None
    """
    # Loop through all the files in the input folder
    for filename in os.listdir(input_path):
        try:
            # Open the file using PIL
            img = Image.open(os.path.join(input_path, filename))

            # Calculate the new size of the canvas
            img_width, img_height = img.size
            ratio = img_width / img_height
            if img_width > img_height:
                img_width = size[0]
                img_height = int(size[0] / ratio)
            else:
                img_width = int(size[0] * ratio)
                img_height = size[0]

            # Calculate the position of the image in the canvas
            x = (size[0] - img_width) // 2
            y = (size[1] - img_height) // 2

            # Create a new image with white background
            new_img = Image.new("RGB", size, (255, 255, 255))

            # Paste the image in the canvas with white padding
            new_img.paste(img.resize(
                (img_width, img_height), Image.ANTIALIAS), (x, y))

            # Save the new image with the same filename in the output folder
            new_img.save(os.path.join(output_path, filename))
        except (IOError, OSError):
            continue
