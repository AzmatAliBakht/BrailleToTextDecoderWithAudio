# Braille Decoding Algorithm

This is an algorithm implemented in Python for decoding Braille characters from an input image. The algorithm traverses a 3x2 Braille matrix, detects the dots present, and maps them to corresponding characters based on their positions. The aim of this project is to provide a reliable and efficient method for decoding Braille characters from digital images.

## Algorithm Overview

1. The input image is read using the OpenCV library and converted to a binary image with two values: 0 (black) and 255 (white).
2. The algorithm performs 8-connectivity analysis on the binary image to identify individual Braille dots and assigns labels to them.
3. The center points of all the dots are calculated to determine the shortest distance between two dots.
4. The algorithm traverses the image pixel by pixel, decodes the Braille characters using clockwise and anticlockwise traversal, and generates the final output string.
5. Spaces are added between words based on the distance between dots.
6. The decoded output is printed on the console and saved in a text file named "Algorithm Output".
7. The decoded output is also converted into sound and saved into a mp3 file, the file is automatically run after conversion.

## Results

The algorithm successfully decodes Braille characters from the input image and provides the corresponding text output. The output is both printed on the console and saved in a text file for further analysis or usage as well as an audio file is created and run. The algorithm demonstrates efficient Braille decoding capabilities and can be used for various applications involving Braille text recognition.

Please note that the algorithm assumes the input image follows the standard Braille dot arrangement and may not be suitable for non-standard layouts or variations in Braille representation.
