############
## UTILS
############

## IMPORTS
import re
import locale
from datetime import date, datetime

## EXTRACT NUMBER FROM STRING
def extractNumber(text):
    return int(re.findall(r'\d+', text.replace('.', ''))[0])

## EXTRACT UPLOAD DATE VIDEO
def extractDate(text, dt_fmt):
    # SET BRAZILIAN LOCALE
    locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')
    return datetime.strptime(text, dt_fmt).date()

def getDateNow():
    # SET BRAZILIAN LOCALE
    locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')
    return date.today()

def checkRanking(text):
    if (re.search(r'#\d{,2}$', text)):
        return text