from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from pyuploadcare.dj.forms import FileWidget, ImageField
from .models import Product


class ProductForm(forms.ModelForm):
    product_picture = ImageField(
        widget=FileWidget(
            attrs={
                'data-public-key': '47e54d77c7a9f66c3f0c',
                'data-images-only': 'True',
                'data-preview-step': 'True',
                'data-image-shrink': '500x500',
                'data-crop': '1:1',
            }
        )
    )

    seller_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'readonly': 'readonly'
            }
        )
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('views',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'product_picture',
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    Row(
                        Column(
                            'name',
                            css_class="form-group col mb-0"
                        ),
                        css_class="form-row"),
                    Row(
                        Column(
                            'price',
                            css_class="form-group col mb-0"
                        ),
                        Column(
                            'year',
                            css_class="form-group col mb-0"
                        ),
                        css_class="form-row"
                    ),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'quantity_in_stock',
                    css_class="col"
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'description',
                    css_class="col"
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'seller_id',
                    css_class="col"
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    'region',
                    css_class='form-group col-md-4 mb-0'
                ),
                Column(
                    'body',
                    css_class='form-group col-md-4 mb-0'
                ),
                Column(
                    'nodes',
                    css_class='form-group col-md-4 mb-0'
                ),
                css_class='form-row'
            ),
            Submit('submit', 'Save Listing', css_class="btn")
        )
