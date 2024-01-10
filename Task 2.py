import hashlib
import os
from datetime import time
from PIL import Image, ImageDraw, ImageFont
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import time

# INITIALIZARE FISIERE
def generate_random_size():
    width = random.randint(200, 800)
    height = random.randint(200, 800)
    return width, height

def generate_image_with_letter(letter):
    image_size = generate_random_size()
    image = Image.new('RGB', image_size)
    draw = ImageDraw.Draw(image)
    draw.text((100,100), letter)
    return image

def sha256_hash(input):
    sha256_hash_obj = hashlib.sha256()
    sha256_hash_obj.update(input.encode("utf-8"))
    hashed_input = sha256_hash_obj.hexdigest()
    return hashed_input


sizes = [(346, 447), (548, 553), (708, 557), (222, 416), (236, 528)]
headers = ['86dcedb09f344f6afc28ab52b81989a5b37c7265cc7930c3249ec089f339d720',
           '3273584382cdf68bd84f00047124b559cd6c6690516986c459481042f8464b07',
           'ffca5a23b88643fa3950af4491f7c330101fddf36b4e87818d65bb05ce738551',
           '79575d3bec00973e030495b6bbac23e3f13903b138adda4f7559ad0ad2c6b99a',
           'b0e5f6a8e998f160664436990e6abcf95e978242bf3fea8fb62da218a5ee0e51']

# random.seed(int(time.time()))
# for letter in "MARIA":
#     letter_image = generate_image_with_letter(letter)
#     letter_image.save(f'{letter}.ppm', 'PPM')
#     sizes.append(letter_image.size)
# print(sizes)
# for size in sizes:
#     hashed_header = sha256_hash(f"P6 {size[0]} {size[1]} 255")
#     headers.append(hashed_header)
# print(headers)
# exit(0)

# CRIPTARE FISIERE
# key = os.urandom(16)
# cipher = Cipher(algorithms.AES(key), modes.ECB())
#
# for letter in "MARIA":
#     file_path = f"{letter}.ppm"
#     with open(file_path, 'rb') as file:
#         plaintext = file.read()
#
#         encryptor = cipher.encryptor()
#         padder = padding.PKCS7(algorithms.AES.block_size).padder()
#         padded_data = padder.update(plaintext) + padder.finalize()
#         ciphertext = encryptor.update(padded_data) + encryptor.finalize()
#     with open(f"encrypted_{letter}.ppm", 'wb') as encrypted_file:
#         encrypted_file.write(ciphertext)
#
# exit(0)
# REZOLVAREA
def grtPairsOfDivisors(number):
    divisors = []
    i = 1
    while i*i <= number:
        if number % i == 0:
            divisors.append([i, number//i])
        i += 1
    return divisors

nr_pixels = []

for letter in "MARIA":
    file_path = f"encrypted_{letter}.ppm"
    with open(file_path, 'rb') as f:
        content = f.read()
        nr_pixels.append(len(content)//3)

for image_index in range(len(nr_pixels)):
    for padding_length in range(16):
        possible_dimensions = grtPairsOfDivisors(nr_pixels[image_index]-padding_length)
        possible_hashed_headers = []
        dimensions = []
        for dimension in possible_dimensions:
            hashed_header = sha256_hash(f"P6 {dimension[0]} {dimension[1]} 255")
            dimensions.append((dimension[0], dimension[1]))
            possible_hashed_headers.append(hashed_header)

            if dimension[0] != dimension[1]:
                hashed_header = sha256_hash(f"P6 {dimension[1]} {dimension[0]} 255")
                dimensions.append((dimension[1], dimension[0]))
                possible_hashed_headers.append(hashed_header)

        for j in range(len(possible_hashed_headers)):
            if possible_hashed_headers[j] in headers:
                print(image_index, possible_hashed_headers[j])
                print(dimensions[j])
    print()