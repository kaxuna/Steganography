import argparse

from PIL import Image


def get_pixel_diff(pixel1, pixel2):
    r1, g1, b1, o1 = pixel1
    r2, g2, b2, o2 = pixel2

    return abs((r1 - r2) * 100) + abs((g1 - g2) * 10) + abs((b1 - b2))


def compare_images(image1_path, image2_path):
    """Compares two images pixel by pixel.

    Args:
        image1_path: Path to the first image.
        image2_path: Path to the second image.

    Returns:
        True if the images are identical, False otherwise.
    """
    diffs = []
    try:
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

        if img1.size != img2.size:
            return False  # Images have different dimensions

        width, height = img1.size

        for y in range(height):
            for x in range(width):
                pixel1 = img1.getpixel((x, y))
                pixel2 = img2.getpixel((x, y))
                
                diff = get_pixel_diff(pixel1, pixel2)
                if diff != 0:
                    diffs.append(chr(diff))
        return "".join(diffs)

    except FileNotFoundError:
        print("Error: One or both image files not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read image pixels and encode a message.")
  parser.add_argument("image_path_1", help="Path to the image file.")
  parser.add_argument("image_path_2", help="Path to the image file to compare.")
  args = parser.parse_args()

  message = compare_images(args.image_path_1, args.image_path_2)
  print(message)
