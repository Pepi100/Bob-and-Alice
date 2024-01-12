
<h1 align = "center"> Bob and Alice </h1>

### Contributors:

- :koala: [Radu Nedelcu](https://github.com/Pepi100)

- :nail_care: [Maria Cioclov](https://github.com/993m)


## Task 1

<img src="https://github.com/Pepi100/Bob-and-Alice/blob/master/mickey.png" align="right"
     alt="Mickey" width="300">

[Requirement](https://nsucrypto.nsu.ru/media/Olympiads/2023/Round_1/Section%20B/Tasks/2023-round-1-section-B-3-kjfs.pdf)    


Alice and Bob are exchanging with encrypted messages. To encrypt data, they use the Present cipher with an 80-bit secret key in ECB format.
Bob prepared eight files for Alice, without headers, encrypted using the Present algorithm with the same secret key. He has sent the files themselves and hash values of the headers to Alice.

Help Alice decipher the message from Bob by associating each image with it's corresponding header.

> To solve this problem we will be calculating the aproximate dimensions (number of pixels) of each image and matching each possible dimension with the correspoding header, if any.



<br>

- Collect aproximate number of pixels in each image by reading the encrypted file's size.
```py
files_folder = 'task1'
for file in os.listdir(files_folder):
    file_path = os.path.join(files_folder, file)
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()
        nr_pixels.append(len(content) // 3)
```

<br>

- Since [Present](https://en.wikipedia.org/wiki/PRESENT) cipher is a block cipher, it encrypts data in 64-bit chunks (8 bytes). Therefore, it is possible that the file has been padded up to a file size that is a multiple of 8 bytes.

- To account for those cases, we will consider that up to 2 pixels (6 bytes) have been added extra due to padding. Any more than 2 pixels would be too much, as it doesn't make sense for the encryption to append more than 8 bytes.

```py
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

```

<br>

<details>
    <summary style="font-size:20px" > &#128206Output </summary>
<br>

Image: **0**, Header number: **2**, Header: **aa1...bb5**, Dimensions: **512 x 512** px

Image: **1**, Header number: **6**, Header: **bd0...81d**, Dimensions: **598 x 605** px

Image: **2**, Header number: **4**, Header: **77a...cb6**, Dimensions: **585 x 577** px

Image: **3**, Header number: **3**, Header: **70f...450**, Dimensions: **525 x 489** px

Image: **4**, Header number: **0**, Header: **602...71d**, Dimensions: **400 x 433** px

Image: **5**, Header number: **5**, Header: **456...c01**, Dimensions: **513 x 613** px

Image: **6**, Header number: **7**, Header: **372...305**, Dimensions: **465 x 464** px

Image: **7**, Header number: **1**, Header: **f40...7d5**, Dimensions: **559 x 530** px

</details>

<br>
<br>

## Task 2

Using the same strategy as Bob, create your own encrypted images, extracting the file header. You can implement this using any other block cypher. 


> We will achieve this by generating a set of images and and associated hashed header. We will than solve the problem with the method presented in task 1.

- Generate images and associated headers using Python Imaging Library ([PIL](https://pillow.readthedocs.io/en/stable/)).

```python
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
        letter_image = generate_image_with_letter(letter) # generate an image
        file_path = f'task2/original/{letter}'
        if letter in letter_frequency:
            letter_frequency[letter] += 1
            # generate asociated header
            letter_image.save(f'{file_path}{letter_frequency[letter]}.ppm', 'PPM')
        else:
            letter_frequency[letter] = 0
            letter_image.save(f'{file_path}.ppm', 'PPM')
        sizes.append(letter_image.size)

    # hash headers
    for size in sizes:
        hashed_header = sha256_hash(f"P6 {size[0]} {size[1]} 255")
        headers.append(hashed_header)

    return sizes, headers


message = "RADU SI MARIA"
sizes, headers = generate_files(message)

```

- Encrypt images. We chose [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption. 

```python
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

```

- Hash headers with 256

```python
for size in sizes:
        hashed_header = sha256_hash(f"P6 {size[0]} {size[1]} 255")
        headers.append(hashed_header)
```

At this point Alice and attempt to solve the problem with the provided [encrypted images](https://github.com/Pepi100/Bob-and-Alice/tree/master/task2/encrypted) and headers.

<details>
    <summary> Headers:</summary>
    
> 2344400b83bac31695af8a1b03e84df001179ae73e2bd9701097f6f156f00d03

> fef056f513776e434b7a7983c1a6355217f0734c3dfc964d96c993c4bbf133d4

> e79ebf9d8650ac463fd8c493c0f0f4b349f11a3fbdb21e4b2e345a6bcf386975

> 78df4f389c89aeac082a3d064e9aabf594bb94f29557150dfcc08f689c6274fe

> f4e75ec2ccfc505d5676cc93021b23e966508e55e577d29b3a411e513cfc8ffa

> c402c4a36ac2a3f7f3dd97ca44acbf90dbd081e1352eb2a07f54067c3eac922d

>7e81447e86d1fb949f67301d0a406a0720482ae0a627cf1c9adc758a463ba173

>0a4b2afc4528881ac4f8317ae0f08752428fbe5cfc52852d357a233f02db9164

>99fcb00fca3e2e2c6e98f1f854213de9c99ef4a1ca7a5c1d07c97a4580a8eb5c

>c73c0398382266fe308bb4616f4a0a9e9e50cebe1eb9bf90fd46dd80369f6f96

>86cca9f69993671e6212a6d69e6235068c806918a05b7f043fe220d95ce7829

</details>
