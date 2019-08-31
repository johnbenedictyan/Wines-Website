from django import forms

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
    email = forms.EmailField(
        blank=False
    )
    message = forms.CharField(
        widget=forms.Textarea,
        blank=False
    )