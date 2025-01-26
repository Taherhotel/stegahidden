from PIL import Image

def encode_image(input_image_path, secret_message, output_image_path):
    img = Image.open(input_image_path)
    encoded = img.convert("RGB")  # Ensure image is in RGB format
    width, height = img.size
    index = 0

    # Convert the secret message to binary and add a delimiter (1111111111111110)
    binary_message = ''.join([format(ord(char), '08b') for char in secret_message]) + '1111111111111110'

    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(encoded.getpixel((col, row)))  # Always treat as RGB
                for channel in range(3):  # Iterate through RGB channels
                    if index < len(binary_message):
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_message[index])
                        index += 1
                encoded.putpixel((col, row), tuple(pixel))

    encoded.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    binary_message = ''
    width, height = img.size

    # Extract LSBs from the image
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            if isinstance(pixel, int):  # Grayscale pixel
                binary_message += str(pixel & 1)
            else:  # RGB pixel
                for channel in range(3):
                    binary_message += str(pixel[channel] & 1)

    # Group binary message into 8-bit chunks (bytes)
    bytes_data = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]

    decoded_message = ''
    for byte in bytes_data:
        if byte == '11111110':  # Delimiter for the end of the message
            break
        decoded_message += chr(int(byte, 2))

    if decoded_message:
        print(f"Decoded message: {decoded_message}")
    else:
        print("No hidden message found.")

def main():
    print("LSB Steganography")
    choice = input("Do you want to (E)ncode or (D)ecode? ").lower()
    if choice == 'e':
        input_image_path = input("Enter the input image path: ")
        secret_message = input("Enter the secret message: ")
        output_image_path = input("Enter the output image path: ")
        encode_image(input_image_path, secret_message, output_image_path)
    elif choice == 'd':
        encoded_image_path = input("Enter the encoded image path: ")
        decode_image(encoded_image_path)
    else:
        print("Invalid choice. Please enter 'E' or 'D'.")

if __name__ == "__main__":
    main()