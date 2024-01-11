
<h1 align = "center"> Bob and Alice </h1>

### Contributors:

- :koala: [Radu Nedelcu](https://github.com/Pepi100)

- :nail_care: [Maria Cioclov](https://github.com/993m)


## Task 1

<img src="https://github.com/Pepi100/IntroductionToRobotics/blob/master/%232%20-%20RGB%20Led/FinalDiagram.png" align="right"
     alt="Mickey" width="100">

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

- Since Present cipher is a block cipher, it encrypts data in 64-bit chunks (8 bytes). Therefore, it is possible that the file has been padded up to a file size that is a multiple of 8 bytes.

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
    <summary style="font-size:20px" > &#128206 Output </summary>
<br>

Image: 0, Header number: 2, Header: aa1...bb5, Dimensions: 512 x 512 px

Image: 1, Header number: 6, Header: bd0...81d, Dimensions: 598 x 605 px

Image: 2, Header number: 4, Header: 77a...cb6, Dimensions: 585 x 577 px

Image: 3, Header number: 3, Header: 70f...450, Dimensions: 525 x 489 px

Image: 4, Header number: 0, Header: 602...71d, Dimensions: 400 x 433 px

Image: 5, Header number: 5, Header: 456...c01, Dimensions: 513 x 613 px

Image: 6, Header number: 7, Header: 372...305, Dimensions: 465 x 464 px

Image: 7, Header number: 1, Header: f40...7d5, Dimensions: 559 x 530 px

</details>

<br>
<br>

## Task 2