import hashlib
import os


def getDivisorsPair(number):
    divisors = []
    i = 1
    while i*i <= number:
        if number % i == 0:
            divisors.append([i, number//i])
        i += 1
    return divisors

def sha256(input):
    sha256_hash_obj = hashlib.sha256()
    sha256_hash_obj.update(input.encode("utf-8"))
    hashed_input = sha256_hash_obj.hexdigest()
    return hashed_input

nr_pixels = []

headers = ["602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d",
           "f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5",
           "aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5",
           "70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450",
           "77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6",
           "456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01",
           "bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d",
           "372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305"]


# collect aproximate number of pixels in each image by reading the encrypted file's size
files_folder = 'task1'
for file in os.listdir(files_folder):
    file_path = os.path.join(files_folder, file)
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()
        nr_pixels.append(len(content)//3)

# since Present cipher is a block cipher, it encrypts data in 64-bit chunks (8 bytes)
# therefore, it is possible that the file has been padded up to a file size that is a multiple of 8 bytes
# to account for those cases, we will consider that up to 2 pixels (6 bytes) have been added extra due to padding
# any more than 2 pixels would be too much, as it doesn't make sense for the encryption to append more than 8 bytes.
for image_index in range(len(nr_pixels)):
    for padding_length in range(3):
        possible_dimensions = getDivisorsPair(nr_pixels[image_index] - padding_length)
        possible_hashed_headers = []
        dimensions = []

        for dimension in possible_dimensions:
            hashed_header = sha256(f"P6 {dimension[0]} {dimension[1]} 255")
            dimensions.append((dimension[0], dimension[1]))
            possible_hashed_headers.append(hashed_header)

            if dimension[0] != dimension[1]:
                hashed_header = sha256(f"P6 {dimension[1]} {dimension[0]} 255")
                dimensions.append((dimension[1], dimension[0]))
                possible_hashed_headers.append(hashed_header)

        for j in range(len(possible_hashed_headers)):
            if possible_hashed_headers[j] in headers:
                print(f"Image: {image_index}, Header number: {headers.index(possible_hashed_headers[j])}, Header: {possible_hashed_headers[j]}, Dimensions: {dimensions[j][0]} x {dimensions[j][1]} px")

