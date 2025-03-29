import argparse
import os
from distutils.dep_util import newer_group

from PIL import Image


def get_encrypted_pixel_value(r, g, b, char_asci_value):
  r_add = char_asci_value // 100
  char_asci_value = char_asci_value - r_add * 100
  g_add = char_asci_value // 10
  char_asci_value = char_asci_value - g_add * 10
  b_add = char_asci_value

  new_r = r + r_add
  new_g = g + g_add
  new_b = b + b_add

  if new_r > 255:
    new_r = r - r_add
  if new_g > 255:
    new_g = g - g_add
  if new_b > 255:
    new_b = b - b_add
  return new_r, new_g, new_b


def read_image_pixels(image_path, message):
  """Reads an image pixel by pixel, prints RGB values, and encodes a message.

  Args:
    image_path: The path to the image file.
    message: The message to encode.
  """
  try:
    image_name = os.path.basename(image_path)
    new_image_name = "encrypted_" + image_name
    new_image_path=os.path.join(os.path.dirname(image_path), new_image_name)


    img = Image.open(image_path)
    pixels = img.load()  # Load pixel data

    width, height = img.size  # Get image dimensions

    if(len(message) > width * height):
      raise ValueError("Message is too long")

    new_img = Image.new("RGBA", (width, height))  # Create a new image with the same dimensions
    new_pixels = new_img.load()  # Load pixel data for the new image

    i = 0
    for y in range(height):
      for x in range(width):
        r, g, b, o = pixels[x, y]  # Get RGB values at (x, y)
        new_pixels[x, y] = (r, g, b, o)  # Set RGB val
        if i < len(message):
          char_asci_value = ord(message[i])
          new_pixels[x, y] = get_encrypted_pixel_value(r, g, b, char_asci_value)  # Set RGB values in the new image
          i = i + 1
    new_img.save(new_image_path)  # Save the new image
    # Encode the message here (implementation not included)

  except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}")
  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read image pixels and encode a message.")
  parser.add_argument("image_path", help="Path to the image file.")
  parser.add_argument("message", help="The message to encode.")
  args = parser.parse_args()

  read_image_pixels(args.image_path, args.message)