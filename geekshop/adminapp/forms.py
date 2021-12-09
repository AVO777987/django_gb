from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from django import forms

from mainapp.models import Products


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductEditForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

