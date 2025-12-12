from PIL import Image
import argparse
import sys
import os


def crop_center(image_path, output_path, ratio=3.0):
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # Calculate new height based on width and target ratio
            new_height = int(width / ratio)

            if new_height > height:
                # If original is too short, warn but proceed with max height (or fail? let's stick to warn and clamp)
                print(
                    f"Warning: Image too short for {ratio}:1 ratio. Clamping to original height."
                )
                new_height = height

            # Calculate crop coordinates (centered vertically)
            top = (height - new_height) // 2
            bottom = top + new_height
            left = 0
            right = width

            # Crop
            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(output_path)
            print(
                f"✅ Success: Cropped {image_path} ({width}x{height}) -> {output_path} ({width}x{new_height}) [Ratio: {ratio}:1]"
            )

    except FileNotFoundError:
        print(f"❌ Error: File not found at {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Crop an image to a specific aspect ratio from the center."
    )
    parser.add_argument("input_path", type=str, help="Path to the input image file")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to save the cropped image (default: overwrite input)",
    )
    parser.add_argument(
        "--ratio",
        "-r",
        type=float,
        default=3.0,
        help="Target aspect ratio (width/height), default 3.0",
    )

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output if args.output else input_path

    # Safety check for overwrite
    if input_path == output_path:
        print(f"ℹ️ Overwriting input file: {input_path}")

    crop_center(input_path, output_path, args.ratio)


if __name__ == "__main__":
    main()
