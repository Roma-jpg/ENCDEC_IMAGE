from PIL import Image
import os

def convert_images_to_png(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if os.path.isfile(input_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
            # Open the image
            with Image.open(input_path) as img:
                # Create the output file path with a .png extension
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')

                # Save the image in PNG format
                img.save(output_path, 'PNG')
                print(f"Converted {filename} to {output_path}")

if __name__ == "__main__":
    # Replace 'input_folder' and 'output_folder' with your actual folder paths
    input_folder = 'path/to/input/folder'
    output_folder = 'path/to/output/folder'

    convert_images_to_png(input_folder, output_folder)
