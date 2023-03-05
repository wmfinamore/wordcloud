import os
from django.core.exceptions import ValidationError
from django.forms import FileField, Form


class DataForm(Form):
    file = FileField()

    def clean_file(self) -> str:
        """upload file"""
        data = self.cleaned_data["file"]
        extension = os.path.splitext(data.name)[1]
        valid_extensions: list[str] = [".xlsx", ".csv"]
        if extension not in valid_extensions:
            raise ValidationError("File type no supported")
        return data
