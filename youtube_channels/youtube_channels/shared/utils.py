############
## UTILS
############

## IMPORTS
import re
import locale
from datetime import date, datetime
import unicodedata

## EXTRACT NUMBER FROM STRING (until billion)
def extractNumber(caracter, text):
    value = int(re.findall(r'\d+', text.replace(caracter, '').lower())[0])
    if 'mil' in text:
        value = value * 1000
    elif 'mi' in text:
        value = value * 1000000
    elif 'bi' in text:
        value = value * 1000000000

    return value

## NORMALIZE UNICODE STRINGS
def normalizeString(text):
    return unicodedata.normalize('NFKD', text)