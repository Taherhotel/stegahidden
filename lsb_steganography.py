from PIL import Image

def encode_image(input_image, secret_message, output_image):
    img = Image.open(input_image)
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '11111111'  # Add EOF marker
    pixels = list(img.getdata())
    new_pixels = []
    msg_index = 0

    for pixel in pixels:
        new_pixel = []
        for value in pixel:
            if msg_index < len(binary_message):
                # Modify the LSB
                new_pixel.append((value & ~1) | int(binary_message[msg_index]))
                msg_index += 1
            else:
                new_pixel.append(value)
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_image)
    print("Message encoded and saved to", output_image)
    
def decode_image(encoded_image):
    img = Image.open(encoded_image)
    binary_message = ''
    for pixel in img.getdata():
        for value in pixel:
            binary_message += str(value & 1)

    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    if 'ÿ' in message:  # Detect EOF marker
        return message.split('ÿ')[0]
    return message

    