from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def is_valid_email(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        pass

    return False