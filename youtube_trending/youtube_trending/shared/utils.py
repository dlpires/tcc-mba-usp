############
## UTILS
############

## IMPORTS
import re
from datetime import datetime

## EXTRACT NUMBER FROM STRING
def extractNumber(text):
    return int(re.findall(r'\d+', text.replace('.', ''))[0])

## EXTRACT UPLOAD DATE VIDEO
def extractDate(text, dt_fmt):
    return datetime.strptime(text, dt_fmt).date()