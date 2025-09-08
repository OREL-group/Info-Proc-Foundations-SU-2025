# Patterns defined in regex format
# Follow pattern 
# "NAME": REGEX,

patterns = {
    "SSN": r'[0-9]{3}-[0-9]{2}-[0-9]{4}',
    "Amex Card": r'^3[47][0-9]{13}',
    #BROKEN "Visa Card": \b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b
}
