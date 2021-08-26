from django.contrib.auth.forms import UserCreationForm
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import User, Product

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone','address', 'state','is_individual', 'is_corporate')


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model= Product
        fields = '__all__'