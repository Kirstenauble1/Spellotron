"""
File: spellotron_helper.py
Author: Kirsten Auble
Purpose: Contains several functions that check for spelling errors due to
hitting an adjacent key, adding an extra letter, or missing a letter.
"""
import sys
KEY_ADJACENCY_FILE = 'keyboard_letters'
LEGAL_WORD_FILE = 'dictionary.txt'
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def adjacent_key_dict():
    """Creates a dictionary where the assigned values are the letters adjacent
    to the key(the letter)."""
    adjacent_dict = dict()
    f = open(KEY_ADJACENCY_FILE)
    for line in f:
        line = line.lower().split()
        adjacent_dict[line[0]] = line[1:]
    return adjacent_dict


def amer_eng_list():
    """Creates a list of words in the English dictionary."""
    amer_lst = []
    f = open(LEGAL_WORD_FILE)
    for line in f:
        fixed_line = ""
        for letter in line:
            if letter.isalpha():
                fixed_line += letter
        line = fixed_line.lower().strip()
        amer_lst.append(line)
    return amer_lst


def hit_wrong_key(word):
    lst = amer_eng_list()
    caps_word = ""
    count = 0
    punc_index = []
    upper = []
    punc = []
    for i in range(1, len(word)- 1):
        if word[i].isupper():
            return None
    if word[0].isupper():
        upper.append(word[0].lower())
    for i in range(0, len(word)):
        if word[i].isalpha() is False:
            punc.append(word[i])
            punc_index.append(count)
        count += 1
    for letter in word:
        letter = letter.lower()
        if not letter.isalpha():
            pass
        else:
            caps_word += letter
    word = caps_word
    wrong_key_dict = dict()
    i = 0
    wrong_key_dict[word] = []
    for letter in word:
        adjacent_dictionary = adjacent_key_dict()
        lst_to_try = adjacent_dictionary[letter]
        for adj_letter in lst_to_try:
            if i == 0:
                wrong_key_dict[word].append(adj_letter + word[1:])
            elif 0 < i < len(word) - 1:
                wrong_key_dict[word].append(word[0:i] + adj_letter + word[i + 1:])
            elif i == len(word) - 1:
                wrong_key_dict[word].append(word[0:i] + adj_letter)
        i += 1
    for fixed_word in wrong_key_dict[word]:
        if fixed_word in lst:
            word = fixed_word
            if punc_index != []:
                for r in range(0, len(punc_index)):
                    word = word[:punc_index[r]] + punc[r] + word[punc_index[r]:]
                if upper != []:
                    word = word[0].upper() + word[1:]
            if upper != []:
                    word = word[0].upper() + word[1:]
            return word


def extra_letter(word):
    """Checks to see if the user entered an extra letter in a word
    by removing one at a time and seeing if it is valid."""
    punc_index = []
    upper = []
    punc = []
    count = 0
    caps_word = ""
    for i in range(1, len(word) - 1):
        if word[i].isupper():
            return None
    if word[0].isupper():
        upper.append(word[0].lower())
    for i in range(0, len(word)):
        if word[i].isalpha() is False:
            punc.append(word[i])
            punc_index.append(count)
        count += 1
    for letter in word:
        letter = letter.lower()
        if letter not in ALPHABET:
            pass
        else:
            caps_word += letter
    word = caps_word
    for i in range(1, len(word)-1):
        if word[:i] + word[i+1:] in amer_eng_list():
            new_word = word[:i] + word[i+1:]
            if punc_index != []:
                for r in range(0, len(punc_index)):
                    new_word = new_word[:punc_index[r]] + punc[r] + new_word[punc_index[r]:]
                if upper != []:
                    new_word = upper[0].upper() + new_word[1:]
            elif upper != []:
                    new_word = upper[0].upper() + new_word[1:]
            return new_word


def missing_letter(word):
    """Checks to see if a word has a missing letter by adding letters a-z
    in each position and seeing if it is valid."""
    punc_index = []
    upper = []
    punc = []
    count = 0
    caps_word = ""
    for i in range(1, len(word) - 1):
        if word[i].isupper():
            return None
    if word[0].isupper():
        upper.append(word[0].lower())
    for i in range(0, len(word)):
        if word[i].isalpha() is False:
            punc.append(word[i])
            punc_index.append(count)
        count += 1
    for letter in word:
        letter = letter.lower()
        if not letter.isalpha():
            pass
        else:
            caps_word += letter
    word = caps_word
    for letter in ALPHABET:
        i = 0
        while i <= len(word):
            new_word = word[:i] + letter + word[i:]
            if new_word in amer_eng_list():
                if punc_index != []:
                    for r in range(0, len(punc_index)):
                        new_word = new_word[:punc_index[r] + 1] + punc[r] + new_word[punc_index[r] + 1:]
                        if upper != []:
                            word = new_word[0].upper() + word[1:]
                if upper != []:
                    new_word = new_word[0].upper() + new_word[1:]
                return new_word
            i += 1
        else:
            i += 1


def leng_three_lines():
    text_file = str(sys.argv[2])
    f = open(text_file)
    words_read = 0
    no_correction = 0
    words_corrected = []
    word_after_corrected = []
    unknown_words = []
    original = ""
    proper_newline = ""
    num_words_corrected = 0
    for line in f:
        corrected_string = ""
        line = line.strip()
        original += line + "\n"
        line = line.split()
        for word in line:
            stringy = ""
            if word.isdigit():
                words_read += 1
                corrected_string += " " + word
                break
            for letter in word:
                if letter.isalpha():
                    stringy += letter.lower()
            if stringy not in amer_eng_list():
                if hit_wrong_key(word) is None:
                    if extra_letter(word) is None:
                        if missing_letter(word) is None:
                            words_read += 1
                            no_correction += 1
                            unknown_words.append(word)
                            if corrected_string == "":
                                corrected_string += word
                            else:
                                corrected_string += " " + word
                        else:
                            words_corrected.append(word)
                            word_after_corrected.append(missing_letter(word))
                            num_words_corrected += 1
                            words_read += 1
                            if corrected_string == "":
                                corrected_string += missing_letter(word)
                            else:
                                corrected_string += " " + missing_letter(word)
                    else:
                        words_corrected.append(word)
                        word_after_corrected.append(extra_letter(word))
                        num_words_corrected += 1
                        words_read += 1
                        if corrected_string == "":
                            corrected_string += extra_letter(word)
                        else:
                            corrected_string += " " + extra_letter(word)
                else:
                    words_corrected.append(word)
                    word_after_corrected.append(hit_wrong_key(word))
                    num_words_corrected += 1
                    words_read += 1
                    if corrected_string == "":
                        corrected_string += hit_wrong_key(word)
                    else:
                        corrected_string += " " + hit_wrong_key(word)
            else:
                words_read += 1
                if corrected_string == "":
                    corrected_string += word
                else:
                    corrected_string += " " + word
        proper_newline += corrected_string + "\n"
    f.close()
    print(original)
    print(proper_newline)
    print(str(words_read) + " Words read from file.")
    print(str(no_correction) + " Unknown Words.")
    print(unknown_words)
    print(str(num_words_corrected) + " Corrected words.")
    print(str(words_corrected))


def leng_three_words():
    text_file = str(sys.argv[2])
    f = open(text_file)
    words_read = 0
    no_correction = 0
    words_corrected = []
    word_after_corrected = []
    unknown_words = []
    original = ""
    num_words_corrected = 0
    corrected_string = ""
    for line in f:
        line = line.split()
        for word in line:
            if original == "":
                original += word
            else:
                original += " " + word
            if word.isdigit():
                words_read += 1
                corrected_string += " " + word
                break
        for word in line:
            stringy = ""
            for letter in word:
                if letter.isalpha():
                    stringy += letter.lower()
            if stringy not in amer_eng_list():
                if hit_wrong_key(word) is None:
                    if extra_letter(word) is None:
                        if missing_letter(word) is None:
                            words_read += 1
                            no_correction += 1
                            unknown_words.append(word)
                            if corrected_string == "":
                                corrected_string += word
                            else:
                                corrected_string += " " + word
                        else:
                            words_corrected.append(word)
                            word_after_corrected.append(missing_letter(word))
                            num_words_corrected += 1
                            words_read += 1
                            if corrected_string == "":
                                corrected_string += missing_letter(word)
                            else:
                                corrected_string += " " + missing_letter(word)
                    else:
                        words_corrected.append(word)
                        word_after_corrected.append(extra_letter(word))
                        num_words_corrected += 1
                        words_read += 1
                        if corrected_string == "":
                            corrected_string += extra_letter(word)
                        else:
                            corrected_string += " " + extra_letter(word)
                else:
                    words_corrected.append(word)
                    word_after_corrected.append(hit_wrong_key(word))
                    num_words_corrected += 1
                    words_read += 1
                    if corrected_string == "":
                        corrected_string += hit_wrong_key(word)
                    else:
                        corrected_string += " " + hit_wrong_key(word)
            else:
                words_read += 1
                if corrected_string == "":
                    corrected_string += word
                else:
                    corrected_string += " " + word
    f.close()
    print(original)
    for i in range(0, num_words_corrected):
        print(words_corrected[i] + " -> " + word_after_corrected[i])
    print(str(words_read) + " Words read from file.")
    print(str(no_correction) + " Unknown Words.")
    print(unknown_words)
    print(str(num_words_corrected) + " Corrected words.")
    print(str(words_corrected))


def leng_two_words():
    text_block = sys.stdin.read()
    words_read = 0
    no_correction = 0
    words_corrected = []
    word_after_corrected = []
    unknown_words = []
    num_words_corrected = 0
    corrected_string = ""
    text = text_block.split()
    for word in text:
        stringy = ""
        if word.isdigit():
            words_read += 1
            corrected_string += " " + word
            break
        for letter in word:
            if letter.isalpha():
                stringy += letter.lower()
        if stringy not in amer_eng_list():
            if hit_wrong_key(word) is None:
                if extra_letter(word) is None:
                    if missing_letter(word) is None:
                        words_read += 1
                        no_correction += 1
                        unknown_words.append(word)
                        if corrected_string == "":
                            corrected_string += word
                        else:
                            corrected_string += " " + word
                    else:
                        words_corrected.append(word)
                        word_after_corrected.append(missing_letter(word))
                        num_words_corrected += 1
                        words_read += 1
                        if corrected_string == "":
                            corrected_string += missing_letter(word)
                        else:
                            corrected_string += " " + missing_letter(word)
                else:
                    words_corrected.append(word)
                    word_after_corrected.append(extra_letter(word))
                    num_words_corrected += 1
                    words_read += 1
                    if corrected_string == "":
                        corrected_string += extra_letter(word)
                    else:
                        corrected_string += " " + extra_letter(word)
            else:
                words_corrected.append(word)
                word_after_corrected.append(hit_wrong_key(word))
                num_words_corrected += 1
                words_read += 1
                if corrected_string == "":
                    corrected_string += hit_wrong_key(word)
                else:
                    corrected_string += " " + hit_wrong_key(word)
        else:
            words_read += 1
            if corrected_string == "":
                corrected_string += word
            else:
                corrected_string += " " + word
    for i in range(0, num_words_corrected):
        print(words_corrected[i] + " -> " + word_after_corrected[i])
    print(str(words_read) + " Words read from file.")
    print(str(no_correction) + " Unknown Words.")
    print(unknown_words)
    print(str(num_words_corrected) + " Corrected words.")
    print(str(words_corrected))


def leng_two_lines():
    text_block = sys.stdin.read()
    words_read = 0
    no_correction = 0
    words_corrected = []
    word_after_corrected = []
    unknown_words = []
    num_words_corrected = 0
    corrected_string = ""
    text = text_block
    newline_lst = []
    i = 0
    for character in text:
        if character == " ":
            pass
        if character == "\n":
            newline_lst.append(i)
        else:
            pass
        i += 1
    text = text_block.split()
    for word in text:
        stringy = ""
        if word.isdigit():
            words_read += 1
            corrected_string += " " + word
            break
        for letter in word:
            if letter.isalpha():
                stringy += letter.lower()
        if stringy not in amer_eng_list():
            if hit_wrong_key(word) is None:
                if extra_letter(word) is None:
                    if missing_letter(word) is None:
                        words_read += 1
                        no_correction += 1
                        unknown_words.append(word)
                        if corrected_string == "":
                            corrected_string += word
                        else:
                            corrected_string += " " + word
                    else:
                        words_corrected.append(word)
                        word_after_corrected.append(missing_letter(word))
                        num_words_corrected += 1
                        words_read += 1
                        if corrected_string == "":
                            corrected_string += missing_letter(word)
                        else:
                            corrected_string += " " + missing_letter(word)
                else:
                    words_corrected.append(word)
                    word_after_corrected.append(extra_letter(word))
                    num_words_corrected += 1
                    words_read += 1
                    if corrected_string == "":
                        corrected_string += extra_letter(word)
                    else:
                        corrected_string += " " + extra_letter(word)
            else:
                words_corrected.append(word)
                word_after_corrected.append(hit_wrong_key(word))
                num_words_corrected += 1
                words_read += 1
                if corrected_string == "":
                    corrected_string += hit_wrong_key(word)
                else:
                    corrected_string += " " + hit_wrong_key(word)
        else:
            words_read += 1
            if corrected_string == "":
                corrected_string += word
            else:
                corrected_string += " " + word
    for index in newline_lst:
        corrected_string = corrected_string[:index] + "\n" + corrected_string[index:]
    print(corrected_string)
    print(str(words_read) + " Words read from file.")
    print(str(no_correction) + " Unknown Words.")
    print(unknown_words)
    print(str(num_words_corrected) + " Corrected words.")
    print(str(words_corrected))
