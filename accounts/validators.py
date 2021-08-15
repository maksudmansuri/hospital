
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', ]
    if not extension.lower() in valid_extensions:
        raise ValidationError(u'Format is not supported, '
                              u'allowed formats: {}'.format(', '.join(valid_extensions)))

