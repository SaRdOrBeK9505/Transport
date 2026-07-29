import re
from django.core.exceptions import ValidationError


def validate_phone(value):
    """
    Telefon raqamni validatsiya qilish.
    Qabul qilinadigan formatlar: +998901234567, 998901234567, 0901234567
    """
    pattern = r'^(\+?998|0)[0-9]{9}$'
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    if not re.match(pattern, cleaned):
        raise ValidationError(
            'Telefon raqam noto\'g\'ri formatda. Masalan: +998901234567'
        )
