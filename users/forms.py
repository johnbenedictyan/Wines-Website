from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
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
                    Div(
                        HTML(
                            """
                            <h3>
                                Sign In
                            </h3>
                            """
                        )
                    )
                )
            ),
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
                        'Sign In', 
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
        'data-public-key':'c1c0ea35a4b3421770fa',
        'data-images-only':'True',
        'data-preview-step':'True',
    }))
    
    class Meta:
        model = UserAccount
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'profile_picture'
            )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Div(
                        HTML(
                            """
                            <h3>
                                Register for an Account
                            </h3>
                            """
                        )
                    )
                )
            ),
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
                    css_class='form-group col-12'
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
            return UserAccount