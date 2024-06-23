import os
import sys
import logging
from PIL import Image, UnidentifiedImageError
import argparse
import random
from tqdm import tqdm

# Enhanced ASCII character sets for distinct variations
ASCII_VARIATIONS = {
    1: "@%#*+=-:. ",
    2: "@#W$9876543210?!abc;:+=-,._ ",
    3: " .:-=+*#%@"
}

def print_banner():
    banner_folder = "ASCIArt"
    if os.path.isdir(banner_folder):
        banners = [f for f in os.listdir(banner_folder) if os.path.isfile(os.path.join(banner_folder, f))]
        if banners:
            with open(os.path.join(banner_folder, random.choice(banners)), 'r') as f:
                banner = f.read()
                phrase = get_random_phrase()
                banner_lines = banner.split('\n')
                max_length = max(len(line) for line in banner_lines)
                
                if phrase:
                    # Calculate the position to place the phrase in the middle-right
                    middle_index = len(banner_lines) // 2
                    phrase_offset = max_length - len(phrase) - 1  # Offset from the right
                    if len(banner_lines[middle_index]) > phrase_offset:
                        banner_lines[middle_index] = banner_lines[middle_index][:phrase_offset] + phrase
                    else:
                        banner_lines[middle_index] = banner_lines[middle_index].ljust(phrase_offset) + phrase

                banner_with_phrase = "\n".join(banner_lines)
                print(banner_with_phrase)
                return banner_with_phrase
        else:
            print("No ASCII art banners found in ASCIArt folder.")
            return ""
    else:
        print("ASCIArt folder not found.")
        return ""

def get_random_phrase():
    phrases_file = "ASCIText/phrases.txt"
    if os.path.isfile(phrases_file):
        with open(phrases_file, 'r') as f:
            phrases = f.readlines()
        if phrases:
            phrase = random.choice([phrase.strip() for phrase in phrases])
            logging.debug(f"Selected phrase: {phrase}")
            return phrase
        else:
            logging.debug(f"No phrases found in {phrases_file}.")
            return "No phrases found in ASCIText file."
    else:
        logging.debug("ASCIText file not found.")
        return "ASCIText file not found."

def resize_image(image, new_width):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = "".join([ascii_chars[int(pixel / 256 * len(ascii_chars))] for pixel in tqdm(pixels, desc="Converting pixels to ASCII")])
    return ascii_str

def convert_image_to_ascii(image_path, ascii_chars, new_width):
    try:
        image = Image.open(image_path)
    except UnidentifiedImageError as e:
        logging.error(f"Unable to open image file: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

    image = resize_image(image, new_width)
    image = grayify(image)
    
    try:
        ascii_str = pixels_to_ascii(image, ascii_chars)
    except IndexError as e:
        logging.error(f"Error converting pixels to ASCII: {e}")
        return None
    
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:index + img_width] for index in range(0, ascii_str_len, img_width)])

    return ascii_img

def save_ascii_to_file(ascii_img, output_path):
    try:
        with open(output_path, "w") as f:
            f.write(ascii_img)
            logging.info(f"ASCII art saved to {output_path}")
            print(f"ASCII art saved to {output_path}")
    except Exception as e:
        logging.error(f"Unable to save ASCII art to file: {e}")
        print(f"Unable to save ASCII art to file: {e}")

def validate_input_path(input_path):
    if not os.path.isfile(input_path):
        logging.error("The input file does not exist.")
        print("The input file does not exist.")
        return False
    return True

def validate_output_path(output_path):
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            logging.error(f"Error creating output directory: {e}")
            print(f"Error creating output directory: {e}")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Convert an image to ASCII art.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example:
  python cbkb-asci.py input.png output.txt --variations 2 --width 80

Variations:
  1. Dense characters
  2. Mixed characters
  3. Sparse characters
        """
    )
    parser.add_argument("input_image_path", type=str, help="Path to the input image file", nargs='?')
    parser.add_argument("output_text_path", type=str, help="Path to save the output ASCII art text file", nargs='?')
    parser.add_argument("-v", "--variations", type=int, default=3, choices=ASCII_VARIATIONS.keys(), help="Number of ASCII variations (default: 3)")
    parser.add_argument("-w", "--width", type=int, default=80, help="Width of the output ASCII art (default: 80)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=logging_level, format="%(levelname)s: %(message)s")

    if not args.input_image_path or not args.output_text_path:
        print_banner()
        parser.print_help()
        sys.exit(1)

    if not validate_input_path(args.input_image_path):
        sys.exit(1)

    if not validate_output_path(args.output_text_path):
        sys.exit(1)

    ascii_chars = ASCII_VARIATIONS[args.variations]
    ascii_img = convert_image_to_ascii(args.input_image_path, ascii_chars, args.width)

    if ascii_img:
        save_ascii_to_file(ascii_img, args.output_text_path)
        print(ascii_img)
        logging.info(f"ASCII art has been saved to {args.output_text_path}")
    else:
        logging.error("Failed to create ASCII art")
        print("Failed to create ASCII art")

if __name__ == "__main__":
    main()
