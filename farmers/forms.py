from django import forms
from .models import FarmerAccount
from .models import FarmerProduct
from store.models import Product

class FarmerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = FarmerAccount
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(FarmerRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




class FarmerProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_available=True).order_by('product_name'),
        label="Select product",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Choose an existing product from the store catalog'
    )

    class Meta:
        model = FarmerProduct
        fields = ['product', 'price', 'stock', 'image', 'is_active']
        widgets = {
            'price': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'price': 'Price (₹)',
            'stock': 'Stock',
            'image': 'Image (optional override)',
            'is_active': 'Active listing',
        }
