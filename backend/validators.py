from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(number):
    number_length = len(number)
    validator_regex = r"0[0-9]{2,}[0-9]{7,}$"
    if number == "":
        return
    if number_length != 11:
        raise ValidationError(
            _('%(value)s is not a valid number, mismatch length'),
            params={'value': number}
        )
    
    if not re.match(validator_regex, number):
        raise ValidationError(
            _('%(value)s is not a valid number'),
            params={'value': number}
        )
