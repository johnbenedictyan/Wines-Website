from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from pyuploadcare.dj.forms import FileWidget, ImageField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean_username(self):
        input_username = self.cleaned_data.get('username')
        if UserAccount.objects.filter(username=input_username).count() == 0:
            raise forms.ValidationError("This user does not exist.")
        return input_username
    
    def clean_password(self):
        input_username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password')
        if not auth.authenticate(username=input_username,password=input_password):
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
        fields = ('username','first_name','last_name','email','password1','password2','profile_picture')
        
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