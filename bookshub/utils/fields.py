from rest_framework import serializers


class PasswordField(serializers.CharField):
    """
    A password field that extends CharField to provide custom defaults.
    """
    min_length = 6
    max_length = None

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(
            min_length=self.min_length,
            max_length=self.max_length,
            *args,
            **kwargs
        )
