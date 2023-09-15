import numpy as np
import cv2

# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

# Mapping of dots of braille to character done by traversing in clockwise direction
# A bit string of 1's and 0's is made where the dots are shown by 1.
# For example for A
#   |1  0|
#   |0  0|
#   |0  0|
# A -> 100000
braille_dict = {
    "100000": "A",
    "100001": "B",
    "110000": "C",
    "111000": "D",
    "101000": "E",
    "110001": "F",
    "111001": "G",
    "101001": "H",
    "010001": "I",
    "011001": "J",
    "100010": "K",
    "100011": "L",
    "110010": "M",
    "111010": "N",
    "101010": "O",
    "110011": "P",
    "111011": "Q",
    "101011": "R",
    "010011": "S",
    "011011": "T",
    "100110": "U",
    "100111": "V",
    "011101": "W",
    "110110": "X",
    "111110": "Y",
    "101110": "Z"
}


# function to calculate distance between two points. Arguments are in form of (x,y) tuples
def calculate_distance(pnt1, pnt2):
    distance = pow((pow(pnt1[1] - pnt2[1], 2)) + (pow(pnt1[0] - pnt2[0], 2)), 0.5)
    return distance


# Traversing the 3x2 Braille Matrices by the clockwise and anticlockwise traversal functions

# Calculating the bit string and weight in clockwise direction. Argument is label of dot from where traversal starts
# Weight of the string is calculated by adding all the 1's in the string
# function will return a tuple that contains bit string and the weight of the string
def clockwise_traverse(c_label):
    b_string = ""  # string to hold 1's and 0's mapping to the braille
    weight = 0
    x_co = int(centers_list[c_label][0])
    y_co = int(centers_list[c_label][1])
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    # traversing right
    y_co += shortest_x
    c_label = label_matrix[x_co][y_co]
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    # traversing down
    x_co += shortest_x
    c_label = label_matrix[x_co][y_co]
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    # traversing down
    x_co += shortest_x
    c_label = label_matrix[x_co][y_co]
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    # traversing left
    y_co -= shortest_x
    c_label = label_matrix[x_co][y_co]
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    # traversing up
    x_co -= shortest_x
    c_label = label_matrix[x_co][y_co]
    if c_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(c_label)
        weight += 1

    return b_string, weight


# Calculating the bit string and weight in anticlockwise direction. Argument is label of dot from where traversal starts
# Weight of the string is calculated by adding all the 1's in the string
# function will return a tuple that contains bit string and the weight of the string
def anticlockwise_traverse(a_label):
    b_string = ""  # string to hold 1's and 0's mapping to the braille
    weight = 0
    x_co = int(centers_list[a_label][0])
    y_co = int(centers_list[a_label][1])
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    # traversing left
    y_co -= shortest_x
    a_label = label_matrix[x_co][y_co]
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    # traversing down
    x_co += shortest_x
    a_label = label_matrix[x_co][y_co]
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    # traversing down
    x_co += shortest_x
    a_label = label_matrix[x_co][y_co]
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    # traversing right
    y_co += shortest_x
    a_label = label_matrix[x_co][y_co]
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    # traversing up
    x_co -= shortest_x
    a_label = label_matrix[x_co][y_co]
    if a_label == 0:
        b_string = b_string + "0"
    else:
        b_string = b_string + "1"
        dots_traversed.append(a_label)
        weight += 1

    b_string = b_string[1:] + b_string[:1]  # rotating string left
    b_string = b_string[1:] + b_string[:1]  # rotating string left again
    b_string = b_string[::-1]  # reversing the entire string

    return b_string, weight


# CODE STARTS FROM HERE

# im = cv2.imread("Braille.png", 0)
#im = cv2.imread("example.png", 0)
im = cv2.imread("result.png", 0)

# Adding padding of 255 around the image
im_padded = np.pad(im, 1, "constant", constant_values=255)

size_rows = len(im_padded)
size_columns = len(im_padded[0])

# converting to binary image with two values: 0 and 255
im_padded = (im_padded // 128) * 255

black = 0
white = 255

label_matrix = np.zeros((size_rows, size_columns))
label = 0
list_label = {}  # equivalency list
arrange_array = []  # temporary array for storing neighbours. Used in 8-connectivity

# 8-connectivity code

for i in range(1, size_rows - 1):
    for j in range(1, size_columns - 1):
        if im_padded[i][j] == black:

            # if all the 4 neighbours have zero label
            if label_matrix[i - 1][j] == 0 and label_matrix[i][j - 1] == 0 and label_matrix[i - 1][j - 1] == 0 and \
                    label_matrix[i - 1][j + 1] == 0:
                label += 1
                label_matrix[i][j] = label
                list_label.update({label: label})

            # if at least one of the 4 neighbours have label not equal to zero
            else:
                if label_matrix[i - 1][j] != 0:
                    arrange_array.append(label_matrix[i - 1][j])

                if label_matrix[i][j - 1] != 0:
                    arrange_array.append(label_matrix[i][j - 1])

                if label_matrix[i - 1][j - 1] != 0:
                    arrange_array.append(label_matrix[i - 1][j - 1])

                if label_matrix[i - 1][j + 1] != 0:
                    arrange_array.append(label_matrix[i - 1][j + 1])

                min_val = min(arrange_array)
                label_matrix[i][j] = min_val

                for x in arrange_array:

                    if x in list_label.keys():
                        list_label.update({x: list_label[min_val]})

                arrange_array = []

matrix_check = label_matrix.copy()

# reiterating the matrix to update the labels according to the list
for i in range(1, size_rows - 1):
    for j in range(1, size_columns - 1):
        if label_matrix[i][j] != 0:
            label_matrix[i][j] = list_label[label_matrix[i][j]]

# counting number of objects
unique_digits = np.unique(label_matrix)
unique_digits = np.delete(unique_digits, [0])
count = len(unique_digits)

# Finding the center points of all the dots
centers_list = {}  # a dictionary which has center coordinates of all dots in form of (x,y) tuples --> {label: (x,y)}

# changes done (added 1 in len(list_label): range(1, len(list_label)) ---> range(1, len(list_label)+1)
for i in range(1, len(list_label) + 1):
    if list_label[i] == i:
        index = np.where(label_matrix == i)
        x_mid = np.ceil(sum(index[0]) / len(index[0]))
        y_mid = np.ceil(sum(index[1]) / len(index[1]))
        centers_list.update({i: (x_mid, y_mid)})

# finding the shortest distance between two dots by taking their center points
p1 = centers_list[unique_digits[0]]
p2 = centers_list[unique_digits[1]]
shortest_x = calculate_distance(p1, p2)
for i in range(1, count - 1):
    p1 = centers_list[unique_digits[i]]
    p2 = centers_list[unique_digits[i + 1]]
    dist = calculate_distance(p1, p2)
    if dist < shortest_x:
        shortest_x = dist

# Converting distance to int as it will be used to find indices
shortest_x = int(shortest_x)

final_string = ""  # initializing string that will hold the final output
dots_traversed = []  # array to keep check of all labels that have been traversed. Array is populated during traversals
space_check = 0  # used for spacing

# Traversing the entire image pixel by pixel, decoding it and in final_string
for i in range(1, size_rows - 1):
    for j in range(1, size_columns - 1):
        point1 = label_matrix[i][j]
        if point1 != 0:
            if point1 not in dots_traversed:
                clock = clockwise_traverse(point1)  # clockwise traversal function - return a tuple (bit-string, weight)
                a_clock = anticlockwise_traverse(point1)  # anticlockwise traversal

                c_weight = clock[1]  # weight of the clockwise string
                a_weight = a_clock[1]  # weight of the anticlockwise string

                # The string having the greater weight is selected
                if c_weight >= a_weight:
                    c_string = clock[0]
                    # checking dictionary for bit-string key and appending character corresponding to it in final string
                    final_string += braille_dict[c_string]
                else:
                    a_string = a_clock[0]
                    # checking dictionary for bit-string key and appending character corresponding to it in final string
                    final_string += braille_dict[a_string]

            space_check = 0  # reinitialized to zero when a dot appears
        else:
            # Adding spaces after words
            space_check += 1  # incremented everytime a white pixels appears
            if len(final_string) != 0 and space_check > 4 * shortest_x and final_string[len(final_string) - 1] != " ":
                final_string += " "

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine
myobj = gTTS(text=final_string, lang=language, slow=False)

# Saving the converted audio in a mp3 file named output
myobj.save("output.mp3")

# Playing the converted file
os.system("start output.mp3")

# Printing the output on console
print("DECODED OUTPUT:\n" + final_string)

# Writing the output in a file named "Algorithm Output"
out_file = open("Algorithm Output", "wt")
out_file.write("DECODED OUTPUT:\n" + final_string)
out_file.close()
