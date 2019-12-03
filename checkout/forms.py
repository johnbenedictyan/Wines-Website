from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div, Button
from .models import Customer_Detail
from django_countries.widgets import CountrySelectWidget
from datetime import datetime
from django.contrib.auth.password_validation import validate_password
from users.models import UserAccount

class CustomerDetailForm(forms.ModelForm):
    
    class Meta:
        model = Customer_Detail
        fields = '__all__'
        widgets = {
            'country': CountrySelectWidget(),
            'account_password_1': forms.PasswordInput(),
            'account_password_2': forms.PasswordInput(),
            'address_1': forms.TextInput(
                attrs={
                    'placeholder': 'Street address'
                }
            ),
            'address_2': forms.TextInput(
                attrs={
                    'placeholder': 'Apartment, suite, unit etc. (optional)'
                }
            ),
            'alt_address_1': forms.TextInput(
                attrs={
                    'placeholder': 'Street address'
                }
            ),
            'alt_address_2': forms.TextInput(
                attrs={
                    'placeholder': 'Apartment, suite, unit etc. (optional)'
                }
            ),
            'order_notes': forms.Textarea(
                attrs={
                    "cols": "30",
                    "rows": "5"
                }
            )
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML(
                        """<h2 class="h3 mb-3 text-black font-heading-serif">Billing Details</h2>"""
                    ),
                    Div(
                        Div(
                            "country",
                            css_class="form-group"
                        ),
                        Row(
                            Column(
                                "first_name",
                                css_class="col-md-6"
                            ),
                            Column(
                                "last_name",
                                css_class="col-md-6"
                            ),
                            css_class="form-group"
                        ),
                        Row(
                            Column(
                                "address_1",
                                css_class="col-md-12"
                            ),
                            css_class="form-group"
                        ),
                        Div(
                            "address_2",
                            css_class="form-group"
                        ),
                        Row(
                            Column(
                                "state_or_country",
                                css_class="col-md-6"
                            ),
                            Column(
                                "postal_code_or_zip",
                                css_class="col-md-6"
                            ),
                            css_class="form-group"
                        ),
                        Row(
                            Column(
                                "email",
                                css_class="col-md-6"
                            ),
                            Column(
                                "phone",
                                css_class="col-md-6"
                            ),
                            css_class="form-group mb-5"
                        ),
                        Div(
                            HTML(
                                """
                                <label for="c_create_account" class="text-black" data-toggle="collapse" href="#create_an_account"
                                  role="button" aria-expanded="false" aria-controls="create_an_account"><input type="checkbox" value="1"
                                    id="c_create_account"> Create an account?</label>
                                """
                            ),
                            Div(
                                Div(
                                    HTML(
                                        """
                                        <p class="mb-3">Create an account by
                                        entering the information below.
                                        If you are a returning customer
                                        please login at the top of the page.</p>
                                        """
                                    ),
                                    Div(
                                        "account_username",
                                        css_class="form-group"
                                    ),
                                    Div(
                                        "account_password_1",
                                        css_class="form-group"
                                    ),
                                    Div(
                                        "account_password_2",
                                        css_class="form-group"
                                    ),
                                    css_class="py-2"
                                ),
                                css_class="collapse",
                                css_id="create_an_account"
                            ),
                            css_class="form-group"
                        ),
                        Div(
                            HTML(
                                """
                                <label for="c_ship_different_address" class="text-black" data-toggle="collapse"
                                  href="#ship_different_address" role="button" aria-expanded="false"
                                  aria-controls="ship_different_address"><input type="checkbox" value="1" id="c_ship_different_address">
                                  Ship To A Different Address?</label>
                                 """
                            ),
                            Div(
                                Div(
                                    Div(
                                        "alt_country",
                                        css_class="form-group"
                                    ),
                                    Row(
                                        Column(
                                            "alt_address_1",
                                            css_class="col-md-12"
                                        ),
                                        css_class="form-group"
                                    ),
                                    Div(
                                        "alt_address_2",
                                        css_class="form-group"
                                    ),
                                    Row(
                                        Column(
                                            "alt_state_or_country",
                                            css_class="col-md-6"
                                        ),
                                        Column(
                                            "alt_postal_code_or_zip",
                                            css_class="col-md-6"
                                        ),
                                        css_class="form-group"
                                    ),
                                    css_class="py-2"
                                ),
                                css_class="collapse",
                                css_id="ship_different_address"
                            ),
                            css_class="form-group"
                        ),
                        Div(
                            "order_notes",
                            css_class="form-group"
                        ),
                        css_class="p-3 p-lg-5 border"
                    ),
                    css_class='col-md-6 mb-5 mb-md-0'
                ),
                Column(
                    Row(
                        Column(
                            HTML(
                                """
                                  <h2 class="h3 mb-3 text-black
                                  font-heading-serif">Your Order</h2>
                                  """
                            ),
                            Div(
                                HTML(
                                    """
                                          <table class="table site-block-order-table mb-5">
                                            <thead>
                                              <th>Product</th>
                                              <th>Total</th>
                                            </thead>
                                            <tbody>
                                            {% for item in user_cart.cart_items %}
                                            <tr>
                                                <td>{{item.product_name|title}}<strong class="mx-2">x</strong>{{item.quantity}}</td>
                                                <td>${{item.total_price}}</td>
                                              </tr>
                                            {% endfor %}
                                              <tr>
                                                <td class="text-black font-weight-bold"><strong>Cart Subtotal</strong></td>
                                                <td class="text-black">${{user_cart.cart_subtotal}}</td>
                                              </tr>
                                              {% if user_cart.coupon_applied != 'no-coupon' %}
                                                <tr>
                                                    <td class="text-black font-weight-bold"><strong>Coupon Applied</strong></td>
                                                    <td class="text-black font-weight-bold"><strong>{{user_cart.coupon_applied}}</strong></td>
                                                </tr>
                                              {% endif %}
                                              <tr>
                                                <td class="text-black font-weight-bold"><strong>Order Total</strong></td>
                                                <td class="text-black font-weight-bold"><strong>${{user_cart.cart_total}}</strong></td>
                                                <input type="hidden" class="form-control" id="cart-total" name="cart-total" value="{{user_cart.cart_total}}">
                                              </tr>
                                            </tbody>
                                          </table>
                                          """
                                ),
                                Div(
                                    Submit('place-order','Place Order',css_class='btn btn-primary btn-lg btn-block'),
                                    css_class="form-group"
                                ),
                                css_class="p-3 p-lg-5 border"
                            ),
                            css_class="col-md-12"
                        ),
                        css_class="mb-5"
                    ),
                    css_class='col-md-6'
                )
            )
        )
        
    def clean_account_username(self):
        username = self.cleaned_data.get("account_username")
        if username != '':
            if UserAccount.objects.filter(username=username).count() > 0:
                raise forms.ValidationError(
                    "This username is already taken",
                    code='username_taken',
                )
        return username
    
    def clean_account_password_1(self):
        username = self.cleaned_data.get("account_username")
        password1 = self.cleaned_data.get("account_password_1")
        if username != '' and password1 == '':
            raise forms.ValidationError(
                ("This field is required for account creation."),
                code='required',
            )
        if username == '' and password1 != '':
            self.add_error(
                "account_username",
                forms.ValidationError(
                    ("This field is required for account creation."),
                    code='required',
                    )
                )
        if username != '' and password1:
            validate_password(
                password1,
                self.instance
            )
        return password1 
        
    def clean_account_password_2(self):
        username = self.cleaned_data.get("account_username")
        password1 = self.cleaned_data.get("account_password_1")
        password2 = self.cleaned_data.get("account_password_2")
        if username != '' and password2 == '':
            raise forms.ValidationError(
                ("This field is required for account creation."),
                code='required',
            )
        if username == '' and password2 != '':
            self.add_error(
                "account_username",
                forms.ValidationError(
                    ("This field is required for account creation."),
                    code='required',
                    )
                )
        if username != '' and password2:
            validate_password(
                password2,
                self.instance
            )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                ("Passwords don't match"),
                code='password_mismatch',
            )
        return password2
    
class PaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2017, 2039)]
    credit_card_number = forms.CharField(
        label='Credit Card Number',
        required=True
    )
    cvc = forms.CharField(
        label='Security Code (cvc)',
        required=True
    )
    expiry_month = forms.ChoiceField(
        label='Month',
        choices=MONTH_CHOICES,
        required=True
    )
    expiry_year = forms.ChoiceField(
        label='Year',
        choices=YEAR_CHOICES,
        required=True
    )
    payable_amount = forms.CharField(
        widget=forms.HiddenInput,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "credit_card_number",
                    css_class="col-12"
                ),
                css_class="form-group"
            ),
            Row(
                Column(
                    "expiry_month",
                    css_class="col-12 col-md"
                ),
                Column(
                    "expiry_year",
                    css_class="col-12 col-md"
                ),
                Column(
                    "cvc",
                    css_class="col-12 col-md"
                ),
                css_class="form-group"
            ),
            Row(
                "payable_amount",
                css_class="form-group"
            ),
            Row(
                Column(
                    Submit(
                        'place-order',
                        'Place Order',
                        css_class='btn btn-primary w-50 btn-block mx-auto'
                        ),
                    css_class="col"
                ),
                css_class="form-group"
                ),
        )
    
    def clean_credit_card_number(self):
        cc_number = self.cleaned_data.get('credit_card_number')
        len_cc_number = len(cc_number)    
        if(len_cc_number < 14 or len_cc_number > 16) or not cc_number.isdigit():
            raise forms.ValidationError(
                    "Invalid Credit Card Number",
                    code='invalid_cc_number',
                )
        
        return cc_number
        
    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc')
        if (len(cvc) != 3 and len(cvc) != 4) or not cvc.isdigit():
            raise forms.ValidationError(
                    "Invalid CVC",
                    code='invalid_cvc',
                )
            
        return cvc
    
    def clean_expiry_month(self):
        expiry_month = self.cleaned_data.get('expiry_month')
        return int(expiry_month)
    
    def clean_expiry_year(self):
        expiry_year = self.cleaned_data.get('expiry_year')
        return int(expiry_year)
            
    def clean(self):
        cleaned_data = super().clean()
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        expiry_month = self.cleaned_data.get('expiry_month')
        expiry_year = self.cleaned_data.get('expiry_year')
        
        if expiry_year:
            if currentYear == expiry_year:
                if currentMonth > expiry_month:
                    self.add_error(
                        'expiry_month',
                        forms.ValidationError(
                            ("Invalid Expiry Month."),
                            code='expired_card'
                            )
                        )
            elif currentYear > expiry_year:
                self.add_error(
                        'expiry_year',
                        forms.ValidationError(
                            ("Invalid Expiry Year."),
                            code='expired_card'
                            )
                        )
        
        return cleaned_data
        