import hashlib
import os
from datetime import time
from PIL import Image, ImageDraw, ImageFont
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import time


# CREATE FILES
def generate_random_size():
    width = random.randint(200, 800)
    height = random.randint(200, 800)
    return width, height


def sha256_hash(input):
    sha256_hash_obj = hashlib.sha256()
    sha256_hash_obj.update(input.encode("utf-8"))
    hashed_input = sha256_hash_obj.hexdigest()
    return hashed_input


def generate_image_with_letter(letter):
    image_size = generate_random_size()
    image = Image.new('RGB', image_size)
    draw = ImageDraw.Draw(image)
    draw.text((100, 100), letter)
    return image


def generate_files(letters):
    random.seed(int(time.time()))
    sizes = []
    headers = []
    letter_frequency = {}
    for letter in letters:
        if letter == ' ':
            continue
        letter_image = generate_image_with_letter(letter)
        file_path = f'task2/original/{letter}'
        if letter in letter_frequency:
            letter_frequency[letter] += 1
            letter_image.save(f'{file_path}{letter_frequency[letter]}.ppm', 'PPM')
        else:
            letter_frequency[letter] = 0
            letter_image.save(f'{file_path}.ppm', 'PPM')
        sizes.append(letter_image.size)

    for size in sizes:
        hashed_header = sha256_hash(f"P6 {size[0]} {size[1]} 255")
        headers.append(hashed_header)

    return sizes, headers


message = "RADU SI MARIA"
# sizes, headers = generate_files(message)
# print(sizes)
# print(headers)
# exit(0)


sizes = [(314, 763), (242, 554), (424, 472), (595, 702), (343, 586), (229, 631), (356, 700), (719, 253), (736, 298), (694, 270), (608, 499)]
headers = ['2344400b83bac31695af8a1b03e84df001179ae73e2bd9701097f6f156f00d03',
           'fef056f513776e434b7a7983c1a6355217f0734c3dfc964d96c993c4bbf133d4',
           'e79ebf9d8650ac463fd8c493c0f0f4b349f11a3fbdb21e4b2e345a6bcf386975',
           '78df4f389c89aeac082a3d064e9aabf594bb94f29557150dfcc08f689c6274fe',
           'f4e75ec2ccfc505d5676cc93021b23e966508e55e577d29b3a411e513cfc8ffa',
           'c402c4a36ac2a3f7f3dd97ca44acbf90dbd081e1352eb2a07f54067c3eac922d',
           '7e81447e86d1fb949f67301d0a406a0720482ae0a627cf1c9adc758a463ba173',
           '0a4b2afc4528881ac4f8317ae0f08752428fbe5cfc52852d357a233f02db9164',
           '99fcb00fca3e2e2c6e98f1f854213de9c99ef4a1ca7a5c1d07c97a4580a8eb5c',
           'c73c0398382266fe308bb4616f4a0a9e9e50cebe1eb9bf90fd46dd80369f6f96',
           '86cca9f69993671e6212a6d69e6235068c806918a05b7f043fe220d95ce78292']


# ENCRYPT FILES
def encrypt_files():
    key = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.ECB())

    folder_path = 'task2/original'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as file:
            plaintext = file.read()
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        with open(f'task2/encrypted/{filename}', 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)


# encrypt_files()
# exit(0)


# SOLVE THE PROBLEM
def grtPairsOfDivisors(number):
    divisors = []
    i = 1
    while i * i <= number:
        if number % i == 0:
            divisors.append([i, number // i])
        i += 1
    return divisors


nr_pixels = []
files_folder = 'task2/original'
for file in os.listdir(files_folder):
    file_path = os.path.join(files_folder, file)
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()
        nr_pixels.append(len(content) // 3)


for image_index in range(len(nr_pixels)):
    for padding_length in range(6):
        possible_dimensions = grtPairsOfDivisors(nr_pixels[image_index] - padding_length)
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
                print(
                    f"Image: {image_index}, Header number: {headers.index(possible_hashed_headers[j])}, Header: {possible_hashed_headers[j]}, Dimensions: {dimensions[j][0]} x {dimensions[j][1]} px")
