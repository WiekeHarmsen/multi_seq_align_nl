from unidecode import unidecode
import re

''''
# String manipulations from preprocessing
'''
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str


def removeAccents(s):
    return unidecode(s)


def removePunctuation(s):
    return "".join([letter for letter in s if letter not in punc])


def removeDigits(s):
    return re.sub('([0-9]+)', ' ', s)


def trimSpaces(s):
    return re.sub('\s+', ' ', s).strip()


def normalizeText(s):
    # Remove puntuation, accents and to lowercase
    return trimSpaces(removeDigits(removePunctuation(removeAccents(s.lower()))))


''''
# String manipulations for postprocessing
'''


def removeInsertions(s):
    return s.replace("*", "")


def trimPipesAndSpaces(s):
    return s.replace("|", " ").strip()
