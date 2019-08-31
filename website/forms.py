from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div

class contact_form(forms.Form):
    first_name = forms.CharField(
        blank=False,
        max_length = 255
    )
    last_name = forms.CharField(
        blank=False,
        max_length = 255
    )
    phone_number = forms.IntegerField(
        blank=False
    )
    email_address = forms.EmailField(
        blank=False
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows':10, 'cols':30}),
        blank=False
    )
    
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