"""
File: spellotron.py
Author: Kirsten Auble
Purpose: Takes python terminal input and either reads from an input file
or user input, spell checks the content based on certain errors that can occur.
"""
import sys
import spellotron_helper


def spell_check():
    """Spell checks input, determines whether user would like to go over their input or read from
    a text file. Presents correct output depending on whether the user selects the words or lines
    format."""
    if len(sys.argv) == 3:
        if sys.argv[1] == "words":
            spellotron_helper.leng_three_words()
        elif sys.argv[1] == "lines":
            spellotron_helper.leng_three_lines()
        else:
            print("Usage: python3.7 spellotron.py words/lines [filename]", file=sys.stderr)
            quit()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "words":
            spellotron_helper.leng_two_words()
        if sys.argv[1] == "lines":
            spellotron_helper.leng_two_lines()
    else:
        print("Usage: python3.7 spellotron.py words/lines [filename]", file=sys.stderr)
        quit()


def main():
    spell_check()


if __name__ == '__main__':
    main()

