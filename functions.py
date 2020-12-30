#!/usr/bin/python
import re


def isLetter(string):
    match = re.match('[a-zA-Z]', string)
    if (match) or (string == '_'):
        return 1
    else:
        return 0


def isNumber(string):
    match = re.match('[0-9]', string)
    if (match):
        return 1
    else:

        return 0


def isIdentfier(string):
    match = re.match('[_a-zA-Z][_a-zA-Z0-9]?', string)
    if (match):
        return 1
    else:
        return 0


def reservedWords(string):
    if string == "if":
        return 1
    elif string == "then":
        return 1
    elif string == "else":
        return 1
    elif string == "read":
        return 1
    elif string == "end":
        return 1
    elif string == "repeat":
        return 1
    elif string == "write":
        return 1
    elif string == "until":
        return 1
    else:
        return 0


def isSpecial(string):
    match = re.match("[< > * () _ + := \- ; / ]", string)

    if string == ' ':
        return 0

    if (match):
        return 1
    else:

        return 0


def classifier(tokens):
    tokens_list = []

    for token in tokens:
        if (reservedWords(token)):
            temp = token

        elif (isSpecial(token)):
            temp = token

        elif ((isIdentfier(token))):
            temp = token

        elif ((isNumber(token))):
            temp = token

        else:
            temp = token
        tokens_list.append(temp)

    return tokens_list


'''

    type_value_list = {'ReservedWords' : [], 'SpecialSymbols' : [],'Identfier' : [],'Number' : [], 'Other' : []}

    for token in tokens:

        if(reservedWords(token)):
            type_value_list['ReservedWords'].append(token)

        elif (isSpecial(token)):
            type_value_list['SpecialSymbols'].append(token)

        elif (isIdentfier(token)):
            type_value_list['Identfier'].append(token)

        elif (isNumber(token)):
            type_value_list['Number'].append(token)


        else:
            type_value_list['SpecialSymbols'].append(token)


    return type_value_list  
'''




# isSpecial('safd')
# identfier("777")     
# isChar('?')
# isNumber('7')
# reservedWords("until")



# words = ["if" , "then" , "else" , "read" , "end" , "repeat", "write", "until"]
# print(words)
# print(len(words))
