import bpy

bpy.ops.object.editmode_toggle()
bpy.ops.font.move(type='LINE_BEGIN')
bpy.ops.font.move(type='LINE_END')
bpy.ops.font.move(type='PREVIOUS_CHARACTER')
bpy.ops.font.move(type='PREVIOUS_CHARACTER')
bpy.ops.font.move(type='PREVIOUS_CHARACTER')
bpy.ops.font.move(type='PREVIOUS_CHARACTER')
bpy.ops.font.text_insert(text="g", accent=False)
bpy.ops.font.move(type='LINE_END')



# Link Arabic letters
import bpy


text_buffer = []

current_char_index = 0


# Arabic letters list

arabic_chars = ['ا', 'أ', 'إ', 'آ', 'ء', 'ب', 'ت', 'ث', 'ج',
                'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص',
                'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                'م', 'ن', 'ه', 'ة', 'و', 'ؤ', 'ي', 'ى', 'ئ', 'ـ']


# Arabic letters that need to be connected to the letter preceding them

right_connectable_chars = ['ا', 'أ', 'إ', 'آ', 'ب', 'ت', 'ث', 'ج', 'ح',
                           'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض',
                           'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م',
                           'ن', 'ه', 'ة', 'و', 'ؤ', 'ي', 'ى', 'ئ', 'ـ']


# Arabic letters that need to be connected to the letter next to them

left_connectable_chars = ['ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'س', 'ش', 'ص',
                          'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                          'م', 'ن', 'ه', 'ي', 'ى', 'ئ', 'ـ']


# Locations (unicode) of Arabic letters shapes (when they are connected to other letters)

#                          ا       أ       إ       آ       ء       ب       ت       ث       ج
chars_variants_bases = [0xFE8D, 0xFE83, 0xFE87, 0xFE81, 0xFE80, 0xFE8F, 0xFE95, 0xFE99, 0xFE9D,
#                          ح       خ       د       ذ       ر       ز       س       ش       ص
                        0xFEA1, 0xFEA5, 0xFEA9, 0xFEAB, 0xFEAD, 0xFEAF, 0xFEB1, 0xFEB5, 0xFEB9,
#                          ض       ط       ظ       ع       غ       ف       ق       ك       ل
                        0xFEBD, 0xFEC1, 0xFEC1, 0xFEC9, 0xFECD, 0xFED1, 0xFED5, 0xFED9, 0xFEDD,
#                          م       ن       ه       ة       و       ؤ       ي       ى       ئ
                        0xFEE1, 0xFEE5, 0xFEE9, 0xFE93, 0xFEED, 0xFE85, 0xFEF1, 0xFEEF, 0xFE89]

chars_arabic_symbols = ['ـ', '،', '؟', '×', '÷']
chars_common = [' ', '.', ',', ':', '|', '(', ')', '[', ']', '{', '}', '!', '+', '-', '*', '/', '\\', '%', '"', '\'', '>', '<', '=', '~', '_']
chars_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def is_right_connectable(c):

    if c in right_connectable_chars:

        return True

    return False


# Check if a letter should be connected to the letter next to it

def is_left_connectable(c):

    if c in left_connectable_chars:

        return True

    return False


# Index of an Arabic letter in the list above

def get_char_index(c):

    if c not in arabic_chars:   # not an arabic char

        return -1

    return arabic_chars.index(c)


# Get the location (unicode id) of an Arabic letter shapes (when connected)

def get_char_variants_base(c):

    char_index = get_char_index(c)

    if char_index == -1:   # It's not an arabic char

        return -1

    return chars_variants_bases[char_index]


#

def is_arabic_char(c):

    if c in arabic_chars:

        return True

    return False


# Arabic char variants are located at 0xFE70 to  0xFEFE on unicode fonts.

def is_arabic_char_variant(c):

    if ord(c) >= 0xFE70 and ord(c) <= 0xFEFE:
        return True

    return False


# Get the previous character from a buffer or text array

def get_previous_alphabet(index, text):

    index -= 1

    while index > 0 and (text[index] in chars_common or text[index] in chars_digits or text[index] in chars_arabic_symbols):
        index -= 1

    if index >= 0:
        return text[index]
    else:
        return None


# Get the next character from a buffer or text array

def get_next_alphabet(index, text):

    index += 1

    while index < len(text) and (text[index] in chars_common or text[index] in chars_digits or text[index] in chars_arabic_symbols):
        index += 1

    if index < len(text):
        return text[index]
    else:
        return None


def link_text(unlinked_text):

    #

    linked_text = []

    previous_char = ""

    next_char = ""

    char_code = 0

    skip_char = False

    # When the letter "Alef" is connected to the letter "Lem" they become one letter
    # but the buffer still contains the two

    uncounted_chars = 0

    #

    for current_char in unlinked_text:

        #

        if skip_char:
            skip_char = False
            continue

        #

        previous_char = ""
        next_char = ""

        #

        chars_count = len(linked_text) + uncounted_chars

        if chars_count > 0:
            previous_char = unlinked_text[chars_count - 1]

        if chars_count < len(unlinked_text) - 1:
            next_char = unlinked_text[chars_count + 1]

        # Lem-Alef
        # Teher are four forms of this letter

        if current_char == 'ل':

            if next_char == 'ا':

                char_code = 0xFEFB

            elif next_char == 'أ':

                char_code = 0xFEF7

            elif next_char == 'إ':

                char_code = 0xFEF9

            elif next_char == 'آ':

                char_code = 0xFEF5

            else:

                char_code = 0

            if char_code != 0:

                if is_left_connectable(previous_char):

                    char_code += 1

                linked_text.insert(0, chr(char_code))

                uncounted_chars += 1

                skip_char = True

                continue
        
        #

        if current_char in chars_arabic_symbols:

            linked_text.insert(0, current_char)

            continue

        if current_char == '\n':

            linked_text.insert(0, current_char)

            continue

        # Common characters follows the direction of the previous text (RTL or LTR)

        if current_char in chars_common:
            
            previous_alpha = get_previous_alphabet(chars_count, unlinked_text)
            next_alpha = get_next_alphabet(chars_count, unlinked_text)
            
            char_pos = 0

            if not is_arabic_char(previous_alpha) and not is_arabic_char(next_alpha) and previous_alpha != '\n':
                
                while char_pos < len(linked_text) and not is_arabic_char_variant(linked_text[char_pos]) and linked_text[char_pos] != '\n':
                    char_pos += 1
            
            linked_text.insert(char_pos, current_char)

            continue

        # Other letters

        char_code = get_char_variants_base(current_char)
        
        if char_code == -1:   # = Not an arabic character

            # Do not reverse non-arabic characters

            previous_alpha = get_previous_alphabet(chars_count, unlinked_text)
            next_alpha = get_next_alphabet(chars_count, unlinked_text)

            char_pos = 0

            # Numbers

            if len(linked_text) > 0 and linked_text[0] in chars_digits:

                while char_pos < len(linked_text) and linked_text[char_pos] in chars_digits:
                    char_pos +=1
            
            # Non-Arabic alhpabet

            elif not is_arabic_char(previous_alpha):

                c = chars_count - 1

                while not is_arabic_char(previous_alpha) and char_pos < len(linked_text) and linked_text[char_pos] != '\n':

                    previous_alpha = get_previous_alphabet(c, unlinked_text)
                    char_pos += 1
                    c -= 1

            linked_text.insert(char_pos, current_char)

            continue

        # It's an Arabic alhpabet

        if is_left_connectable(previous_char) and is_right_connectable(current_char):

            if is_left_connectable(current_char) and is_right_connectable(next_char):

                char_code += 3

            else:

                char_code += 1
        else:

            if is_left_connectable(current_char) and is_right_connectable(next_char):

                char_code += 2
            
            else:
                char_code = ord(current_char)

        linked_text.insert(0, chr(char_code))

    text = ''.join(linked_text)

    return text

def compteur3():
    return link_text("السلام عليكم")

bpy.data.node_groups["NodeTree"].nodes["Data Input"].inputs[0].value = compteur3()


print("bonjour")
compteur3()
compteur3()

