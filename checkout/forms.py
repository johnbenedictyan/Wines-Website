from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
        
class PaymentForm(forms.Form):
    # cc, cvc, expiry date
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2019, 2039)]
    COUNTRY_CHOICES = []
    
    country = forms.ChoiceField(label="Country",
                                choices=COUNTRY_CHOICES,
                                required=True)
    first_name = forms.CharField(label="First Name",
                                 required=True)
    last_name = forms.CharField(label="Last Name",
                                required=True)
    address_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street address'}),
                                required=True)
    address_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apartment, suite, unit etc. (optional)'}),
                                required=False)
    state_or_country = forms.CharField(label="State / Country",
                                       required=True)
    postal_code_or_zip = forms.CharField(label="Postal Code / Zip",
                                         required=True)
    email = forms.CharField(label="",
                            required=True)
    phone = forms.CharField(label="",
                            required=True)
                            
    account_password = forms.CharField(label="",
                                       required=False)
                                       
    alt_country = forms.ChoiceField(label="Country",
                                choices=COUNTRY_CHOICES,
                                required=True)
    alt_address_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street address'}),
                                    required=True)
    alt_address_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apartment, suite, unit etc. (optional)'}),
                                    required=False)
    alt_state_or_country = forms.CharField(label="State / Country",
                                           required=True)
    alt_postal_code_or_zip = forms.CharField(label="Postal Code / Zip",
                                             required=True)
    
    coupon_code = forms.CharField(label="Coupon Code",
                                  required=False)
    credit_card_number = forms.CharField(label='Credit Card Number',
                                         required=False)
    cvv = forms.CharField(label='Security Code (CVV)',
                          required=False)
    expiry_month = forms.ChoiceField(label='Month',
                                     choices=MONTH_CHOICES,
                                     required=False)
    expiry_year = forms.ChoiceField(label='Year',
                                    choices=YEAR_CHOICES,
                                    required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    