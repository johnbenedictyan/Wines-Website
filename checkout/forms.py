from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div, Button
from crispy_forms.bootstrap import StrictButton,FieldWithButtons
from .models import Customer_Details
from django_countries.widgets import CountrySelectWidget

class CustomerDetailForm(forms.ModelForm):
    
    class Meta:
        model = Customer_Details
        fields = '__all__'
        widgets = {
            'country': CountrySelectWidget(),
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
                                        "account_password",
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
                                      font-heading-serif">Coupon Code</h2>
                                      """
                            ),
                            Div(
                                FieldWithButtons('coupon_code', StrictButton("Apply",css_class='btn btn-primary btn-sm rounded px-4 cc-apply-button',css_id='button-addon2')),
                                css_class="p-3 p-lg-5 border"
                            ),
                            css_class="col-md-12"
                        ),
                        css_class="mb-5"
                    ),
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
                                                <td class="text-black">${{user_cart.cart_total}}</td>
                                              </tr>
                                              <tr>
                                                <td class="text-black font-weight-bold"><strong>Order Total</strong></td>
                                                <td class="text-black font-weight-bold"><strong>$0</strong></td>
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


class PaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2019, 2039)]
    credit_card_number = forms.CharField(
        label='Credit Card Number',
        required=False
    )
    cvv = forms.CharField(
        label='Security Code (CVV)',
        required=False
    )
    expiry_month = forms.ChoiceField(
        label='Month',
        choices=MONTH_CHOICES,
        required=False
    )
    expiry_year = forms.ChoiceField(
        label='Year',
        choices=YEAR_CHOICES,
        required=False
    )
    stripe_id = forms.CharField(
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                "credit_card_number",
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
                    "cvv",
                    css_class="col-12 col-md"
                ),
                css_class="form-group"
            ),
            Row(
                "stripe_id",
                css_class="form-group"
            )
        )