from django import forms
from django.core.validators import FileExtensionValidator
from .models import StoreImage


class ImageForm(forms.ModelForm):
    licenseImage=forms.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    class Meta:
        model = StoreImage
        fields = '__all__'
