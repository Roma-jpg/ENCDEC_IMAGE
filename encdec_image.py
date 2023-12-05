import argparse
from PIL import Image
import numpy as np
import os

def convert_key_to_seed(key):
    seed = int(key) % 4294967295
    return seed

def encrypt_image(image_path, seed):
    try:
        img = Image.open(image_path)
        img_array = np.array(img)

        height, width, channels = img_array.shape

        np.random.seed(seed)

        indices = np.arange(height * width)
        np.random.shuffle(indices)

        encrypted_data = [img_array[:, :, i].ravel()[indices].reshape((height, width)) for i in range(channels)]
        encrypted_data = np.stack(encrypted_data, axis=-1)

        # Save the encrypted image with the original file path
        Image.fromarray(encrypted_data.astype('uint8')).save(image_path)
        print(f"Encryption completed for {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def decrypt_image(image_path, seed):
    try:
        encrypted_img = Image.open(image_path)
        encrypted_data = np.array(encrypted_img)

        height, width, channels = encrypted_data.shape

        np.random.seed(seed)

        indices = np.arange(height * width)
        np.random.shuffle(indices)

        decrypted_data = [encrypted_data[:, :, i].ravel()[np.argsort(indices)].reshape((height, width)) for i in range(channels)]
        decrypted_data = np.stack(decrypted_data, axis=-1)

        # Save the decrypted image with the original file path
        Image.fromarray(decrypted_data.astype('uint8')).save(image_path)
        print(f"Decryption completed for {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def encrypt_images_in_folder(folder_path, seed):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            encrypt_image(image_path, seed)

def decrypt_images_in_folder(folder_path, seed):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            decrypt_image(image_path, seed)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt images by shuffling pixels based on a key.")
    parser.add_argument("-p", "--path", help="Path to the image file or folder")
    parser.add_argument("-s", "--seed", help="Seed for pixel shuffling", type=int)
    parser.add_argument("-m", "--mode", help="Encryption or decryption mode (enc or dec)", choices=["enc", "dec"])

    args = parser.parse_args()

    if not args.path:
        args.path = input("Enter the path to the image file or folder: ")

    if not args.seed:
        args.seed = int(input("Enter the seed for pixel shuffling: "))

    if not args.mode:
        args.mode = input("Enter the mode (enc or dec): ")

    if os.path.isfile(args.path):
        if args.mode == "enc":
            encrypt_image(args.path, args.seed)
        elif args.mode == "dec":
            decrypt_image(args.path, args.seed)
    elif os.path.isdir(args.path):
        if args.mode == "enc":
            encrypt_images_in_folder(args.path, args.seed)
        elif args.mode == "dec":
            decrypt_images_in_folder(args.path, args.seed)
    else:
        print("Invalid path provided.")

if __name__ == "__main__":
    main()