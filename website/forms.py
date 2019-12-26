from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from .models import Contact,Blog

class ContactForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':10,
                'cols':30
            })
    )
    
    class Meta:
        model = Contact
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'first_name',
                    css_class='col-md-6 form-group'
                ),
                Column(
                    'last_name',
                    css_class='col-md-6 form-group'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'email_address',
                    css_class='col-md-6 form-group'
                ),
                Column(
                    'phone_number',
                    css_class='col-md-6 form-group'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'message', 
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit', 
                        'Send Message', 
                        css_class="btn btn-primary py-3 px-5"
                    ),
                    css_class='col-12'
                ),
                css_class='form-row'
            ),
        )
        
class BlogCreatorFrom(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':10,
                'cols':30
            })
    )
    writer = forms.CharField(
        widget = forms.HiddenInput(
            )
        )
    
    class Meta:
        model = Blog
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].strip = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'headline',
                    css_class='form-group'
                ),
                css_class='form-row mb-2'
            ),
            Row(
                Column(
                    'body', 
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'writer', 
                    css_class='form-group col-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit(
                        'submit', 
                        'Submit Blog', 
                        css_class="btn btn-primary py-3 px-5"
                    ),
                    css_class='col-12'
                ),
                css_class='form-row'
            ),
        )