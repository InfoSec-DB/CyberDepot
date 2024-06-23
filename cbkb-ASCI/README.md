
# 🎨 CBKB ASCII Art Converter

Welcome to the CBKB ASCII Art Converter! This project empowers you to transform images into stunning ASCII art. Additionally, it features the display of random ASCII art banners for a unique visual experience.

## 🌟 Features

- **🖼️ Image to ASCII Conversion:** Easily convert your images into detailed ASCII art.
- **🎲 Random ASCII Banners:** Display random ASCII art banners from the `ASCIArt` folder each time you run the script.
- **🔢 Density Variations:** Choose from three variations of ASCII art density to suit your needs.
- **📏 Configurable Width:** Adjust the width of the output ASCII art to fit your desired format.

![CBKB - ASCII Art ](https://colorblindkeybangers.com/imgs/cbkb-asci.png)
![CBKB - ASCII Art ](https://colorblindkeybangers.com/imgs/cbkb-asci2.png)



## 🗂️ File Structure

    ├── cbkb-asci/
    │ ├── ASCIArt/
    │ │ ├── art1.txt
    │ │ ├── art2.txt
    │ │ ├── art3.txt
    │ │ └── ... (more ASCII art files)
    │ │
    │ ├── ASCIText/
    │ │ ├── phrases.txt
    │ │
    │ ├── img/
    │ │ ├── cbkb.jpeg
    │ │ └── ... (more image files)
    │ │
    │ ├── cbkb-asci.py
    │ └── requirements.txt

## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/InfoSec-DB/CyberDepot.git
    cd CyberDepot/cbkb-asci
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

To convert an image to ASCII art and save the output to a text file, run:

    python cbkb-asci.py input_image_path output_text_path --variations VARIATION --width WIDTH


## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/InfoSec-DB/CyberDepot.git
    cd CyberDepot/cbkb-asci
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

To convert an image to ASCII art and save the output to a text file, run:
python cbkb-asci.py input_image_path output_text_path --variations VARIATION --width WIDTH

### Options

-   `input_image_path`: Path to the input image file.
-   `output_text_path`: Path to save the output ASCII art text file.
-   `-v, --variations {1,2,3}`: Number of ASCII variations (default: 3).
-   `-w, --width WIDTH`: Width of the output ASCII art (default: 80).
-   `-d, --debug`: Enable debug mode.

### Variations

    1.  Dense characters
    2.  Mixed characters
    3.  Sparse characters

### Example

    python cbkb-asci.py input.png output.txt --variations 2 --width 80
    python cbkb-asci.py img/cbkb.jpeg ASCIArt/cbkb.txt --variations 2 --width 100

This will convert the `cbkb.jpeg` image to ASCII art and save it to `cbkb.txt` using the second variation of ASCII density with a width of 100 characters.


## 🤝 Contributing
Feel free to fork this repository and submit pull requests. All contributions are welcome!


