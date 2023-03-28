import argparse
import os
from PIL import Image


def crop_images_from_instagram_screenshot(*, input_path: str, output_path: str) -> None:
    """
    Crop Instagram screenshots to remove top and bottom margins.

    Args:
        input_path (str): The path to the directory containing the Instagram screenshots.
        output_path (str): The path to the directory where the cropped images will be saved.

    Returns:
        None: The function saves the cropped images to the output_path directory.
    """

    # loop through all files in the input directory
    for filename in os.listdir(input_path):
        try:
            # open image file
            im = Image.open(os.path.join(input_path, filename))
            width, height = im.size

            # find center line
            centerLine = height // 2

            # crop top margin
            white = (255, 255, 255)
            for y in range(centerLine, 0, -1):
                if len([1 for x in range(width) if im.getpixel((x, y)) == white]) == width:
                    box = (0, y, width, height)
                    crop = im.crop(box)
                    crop.save(os.path.join(output_path, filename))
                    break

            # crop bottom margin
            image_file = os.path.join(output_path, filename)
            im = Image.open(image_file)
            width, height = im.size
            for y in range(1, height, 1):
                if len([1 for x in range(width) if im.getpixel((x, y)) == white]) == width:
                    box = (0, 0, width, y)
                    crop = im.crop(box)
                    crop.save(os.path.join(output_path, filename))
                    break
        except Exception as e:
            print(f"Error occurred while processing {filename}: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crop Instagram screenshots to remove top and bottom margins.")
    parser.add_argument("--input-path", type=str, required=True,
                        help="The path to the directory containing the Instagram screenshots.")
    parser.add_argument("--output-path", type=str, required=True,
                        help="The path to the directory where the cropped images will be saved.")
    args = parser.parse_args()

    crop_images_from_instagram_screenshot(
        input_path=args.input_path, output_path=args.output_path)
