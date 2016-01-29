# an example of the playfair cipher in python
import re
import itertools
import sys
from collections import OrderedDict


# Enter A key and message to encrypt here:
key = sys.argv[1]
source = sys.argv[2]
destination = sys.argv[3]





"""
setup_table() will take a a key, create an alphabet
from that key, than clean up any white space or
duplicate characters. Next a loop will go through
each list in table, replacing with every 5 consectutive
characters from alpha. Returns the finsihed, and ready,
table
"""

def setup_table(key):
    table = [[], [], [], [], []]
    alpha = key + 'abcdefghiklmnopqrstuvwxyz'
    alpha = ''.join(alpha.split())
    alpha = re.findall('.?', alpha)
    alpha = list(OrderedDict.fromkeys(alpha))
    counter = 0
    eggs = []
    for i in range(0, 5):
        eggs = []
        for j in range(0, 5):
            eggs.append(alpha[counter])
            counter += 1
        table[i] = eggs
    return table



"""
group_letters() will take a message and get rid of all
non-alpha characters, split them into groups of two.
Any pair that is not fully will get a 'Z' appended,
meanwhile a pair that is the same ('ee') will get
the last letter switched with an 'X' ('ex'). Lastly,
a 'j' will be switched to an 'i'
"""
def group_letters(message):
    spam = re.sub('[^a-zA-Z]', '', message) # get rid of non-alpha
    spam = re.findall('..?', spam) # split into pairs

    for i, pair in enumerate(spam): # gets rid of duplicate numbers
        # if the pair is not 2
        if len(pair) == 1:
            spam[i] = pair[0] + 'z'

        # if pair is the same
        elif pair[0] == pair[1]:
            spam[i] = pair[0] + 'x'

        # if there is a j
        elif 'j' in pair:
            spam[i] = re.sub('j', 'i', pair)

    return spam







"""
get_coordinates()  will take a pair, and loop
througheach character in the row of the table.
The function following, get_letter(), will
return the alternative letter
"""
def get_coordinates(character, table):
    for i, row in enumerate(table):
        for j, char in enumerate(row):
            if row[j] == character:
                return i, j


def get_letter(x, y):
    return table[x][y]


"""
same_row() will take two letter arguments,
it will assign new letters to them based on
their positions, both in the same row
"""
def same_row(let1, let2):
    alt_let1 = ''
    alt_let2 = ''
    if let1[1] == 4: # for letter 1
        alt_let1 = get_letter(let1[0], 0)
    else:
        alt_let1 = get_letter(let1[0], let1[1] + 1)

    if let2[1] == 4: # for letter 2
        alt_let2 = get_letter(let2[0], 0)
    else:
        alt_let1 = get_letter(let2[0], let2[1] + 1)

    return alt_let1, alt_let2


"""
same_col() will take two letter arguments,
it will assign new letters to them based on
their positions, both in the same column
"""
def same_col(let1, let2):
    alt_let1 = ''
    alt_let2 = ''
    if let1[0] == 4: # for letter 1
        alt_let1 = get_letter(0, let1[1])
    else:
        alt_let1 = get_letter(let1[0] + 1, let1[1])

    if let2[0] == 4: # for letter 2
        alt_let2 = get_letter(0, let2[1])
    else:
        alt_let2 = get_letter(let2[0] + 1, let2[1])

    return alt_let1, alt_let2

"""
opposite() will take two letter arguments,
it will assign new letters to them based on
their positions, both in the same column
"""
def opposite(let1, let2):
    alt_let1 = ''
    alt_let2 = ''

    alt_let1 = get_letter(let1[0], let2[1])
    alt_let2 = get_letter(let2[0], let1[1])

    return alt_let1, alt_let2







"""
encrypt() will take a string param, and then
encrypt each pair.
"""
def encrypt(message, table):
    encrypted_message = []
    alt_pair = ''
    alt_let1 = ''
    alt_let2 = ''
    for i, pair in enumerate(message): # get the coordinates of each letter
        for char in pair:
            x, y = get_coordinates(char, table)
            if char == pair[0]:
                let1 = [x, y]
            elif char == pair[1]:
                let2 = [x, y]

        # check if character are in the same row
        if let1[0] == let2[0]:
            alt_let1, alt_let2 = same_row(let1, let2)

        elif let1[1] == let2[1]:
            alt_let1, alt_let2 = same_col(let1, let2)

        else:
            alt_let1, alt_let2 = opposite(let1, let2)

        alt_pair = ''.join([alt_let1, alt_let2])
        encrypted_message.append(alt_pair.upper())

    return ' '.join(encrypted_message)







with open(source, 'r') as message:
    message = message.read()



table = setup_table(key)
org_message = message.strip()
message = org_message.lower()
message = ''.join(message.split())
message = group_letters(message)

encrypted_message = encrypt(message, table)



with open(destination, 'w') as dest:
    dest.write(encrypted_message)
    dest.close()




print 'key:             ', key
print 'Source:          ', source
print 'Destination:     ', destination
