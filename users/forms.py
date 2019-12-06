from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import Group
from pyuploadcare.dj.forms import FileWidget, ImageField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True
        )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'username', 
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password', 
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit', 
                        'Log In', 
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            ),
        )
        
    def clean_username(self):
        input_username = self.cleaned_data.get('username')
        if UserAccount.objects.filter(username=input_username).count() == 0:
            raise forms.ValidationError("This user does not exist.")
        return input_username
    
    def clean_password(self):
        input_username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password')
        if auth.authenticate(username=input_username,password=input_password):
            pass
        else:
            raise forms.ValidationError("Incorrect Password.")
        return input_password
        
class RegisterForm(UserCreationForm):
    profile_picture = ImageField(widget=FileWidget(attrs={
        'data-public-key':'47e54d77c7a9f66c3f0c',
        'data-images-only':'True',
        'data-preview-step':'True',
        'data-image-shrink': '500x500',
        'data-crop': '500x500 upscale',
    }))
    TRUE_FALSE_CHOICES = (
        (False, 'Buyer'),
        (True, 'Seller')
    )
    seller = forms.ChoiceField(
        choices = TRUE_FALSE_CHOICES,
        label="Account Type",
        widget=forms.Select(),
        required=True
        )
    
    class Meta:
        model = UserAccount
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'profile_picture',
            'seller'
            )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'profile_picture', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'username', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'email', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'seller', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'first_name', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'last_name', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password1', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'password2', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit', 
                        'Register', 
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            ),
        )
        
    def clean_username(self):
        requested_username = self.cleaned_data.get('username')
        if UserAccount.objects.filter(username=requested_username).count() > 0:
            raise forms.ValidationError("This username is already taken.")
        return requested_username
            
    def save(self, commit=True):
        UserAccount = super(RegisterForm, self).save(commit=False)
        UserAccount.email = self.cleaned_data["email"]
        UserAccount.first_name = self.cleaned_data["first_name"]
        UserAccount.last_name = self.cleaned_data["last_name"]
        
        if commit:
            UserAccount.save()
            # This checks if the user has opted for a seller account
            # If so, the account will be added to the seller group 
            # and be given additional permissions.
            if UserAccount.seller == True:
                if not UserAccount.groups.filter(name='sellers').exists():
                    seller_group = Group.objects.get(name='sellers') 
                    seller_group.user_set.add(UserAccount)
        
            return UserAccount
            
class AccountDetailForm(RegisterForm):
    
    class Meta(RegisterForm.Meta):
        exclude = ('first_name','last_name',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'New Username'
        self.fields['email'].label = 'New Email'
        self.fields['password1'].label = 'New Password'
        self.fields['password2'].label = 'Confirm Password'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'profile_picture', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'username', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'email', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'seller', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password1', 
                    css_class='form-group col-md-6'
                ),
                Column(
                    'password2', 
                    css_class='form-group col-md-6'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit', 
                        'Update', 
                        css_class="btn btn-primary w-50"
                    ),
                    css_class='form-group col-12 text-center'
                ),
                css_class='form-row'
            ),
        )