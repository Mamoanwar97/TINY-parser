from functions import *
import re
import os


def vaild_next_char(i, n):
    if (i == n - 1):
        return 0
    else:
        return 1


def classify(list_of_okens):
    return type


def get_tokens(line):
    state = "start"
    tokens = []
    token = ""
    i = 0
    char = line[i]

    no_valid_token = 0

    while (1):
        if (state == "start"):
            if (char == ' '):
                i = i + 1
                char = line[i]
                continue
            if isLetter(char):
                state = "letter"
            elif isNumber(char):
                state = "number"
            elif isSpecial(char):
                state = "special"
            elif char == '{':
                state = "comment"
            else:
                no_valid_token = 1
        # print(state)
        if state == "letter":
            while isLetter(char) or isNumber(char):
                token += char
                if (vaild_next_char(i, len(line))):
                    i = i + 1
                    char = line[i]
                    # no_valid_token = 0
                else:
                    no_valid_token = 1
                    break
            state = "acceptance"
        if state == "number":
            while isNumber(char):
                token += char
                if (vaild_next_char(i, len(line))):
                    i = i + 1
                    char = line[i]
                    # no_valid_token = 0
                else:
                    no_valid_token = 1
                    break
            state = "acceptance"

        if state == "special":
            if char == ':':
                while isSpecial(char):
                    token += char
                    if (vaild_next_char(i, len(line))):
                        i = i + 1
                        char = line[i]
                        # no_valid_token = 0
                    else:
                        no_valid_token = 1
                        break
                state = "acceptance"
            else:
                token += char
                if (vaild_next_char(i, len(line))):
                    i = i + 1
                    char = line[i]
                else:
                    if char == ';' or char == ')' :
                        tokens.append(char)
                    no_valid_token = 1
                    break
                state = "acceptance"

        if state == "comment":
            while (char != '}'):
                if (vaild_next_char(i, len(line))):
                    i = i + 1
                    char = line[i]
                else:
                    no_valid_token = 1
                    break
            state = "start"
            if (vaild_next_char(i, len(line))):
                i = i + 1
                char = line[i]

        if (state == "acceptance"):
            state = "start"
            tokens.append(token)
            token = ""

        if (no_valid_token and (not (vaild_next_char(i, len(line))))):
            break
    return tokens


def read_lines(filename):
    tokens = []
    in_file = open(filename, "r")
    lines = in_file.readlines()

    for line in lines:
        # print(line)
        tokens += get_tokens(line)

    in_file.close()
    return tokens


def read_from_editor(text):
    lines = text.split('\n')
    tokens = []
    for line in lines:
        tokens += get_tokens(line.strip())
    return tokens


def main():
    list = read_lines('testCase.txt')

    text_file = open("Output.txt", "w")
    for item in list:
        print(item)
        text_file.write(item)
        text_file.write("\n")

    text_file.close()


if __name__ == "__main__":
    main()
