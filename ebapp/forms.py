from django import forms
import re

import datetime

from django.forms import ModelForm
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from ebapp.models import (
    Auctions, AuctionsDetails, CompanyAccounts, EbayCategories, Settings )

from django.core.exceptions import ValidationError

from ebapp.classes import formsebapp

#from tempus_dominus.widgets import DatePicker

class SettingsForm(forms.ModelForm):
    seller_email = forms.EmailField(
        label='Company e-mail for notifications',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='This email will be used in reports.',
    )

    # company_accounts = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'class': 'form-control',
    #         'rows': 3,
    #         }),
    #     help_text='Separate accounts name by new line',
    # )
    
    target_website_for_wow_offer = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        
        # Ebay global id
        # https://developer.ebay.com/DevZone/merchandising/docs/Concepts/SiteIDToGlobalID.html
        help_text='eBay Site ID. (77 - eBay Germany - EBAY-DE)', 
        initial=77,
    )

    # ebay_category = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'class': 'form-control',
    #         'rows': 3,
    #         }),
    #     help_text='First line is showed as default option in select box.\rSeparate categories by new line.',
    # )

    class Meta:
        model = Settings
        fields = [
            'seller_email',
            # 'company_accounts',
            'target_website_for_wow_offer',
            # 'ebay_category',
        ]

class CompanyAccountsForm(forms.ModelForm):

    class Meta:
        model = CompanyAccounts
        fields = ['company_account']

class CompanyAccountsFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = CompanyAccounts.objects.filter(visible__exact=1)

CompanyAccountsFormSet = modelformset_factory(
    CompanyAccounts, 
    formset=CompanyAccountsFormSet,
    fields=['company_account'], 
    extra=1,
    can_delete=True,
    max_num=50,
    help_texts={
        'company_account': 'Some help text',
    },
    widgets={
        'company_account':
        forms.TextInput(attrs={
            'class': 'form-control m-1',
        })
    }
)

EbayCategoriesFormset = modelformset_factory(
    EbayCategories, 
    fields=['position', 'ebay_category'], 
    extra=1,
    can_delete=True,
    max_num=50,
    help_texts={
        'ebay_category': 'Some help text',
    },
    widgets={
        'position': forms.TextInput(attrs={'class': 'form-control m-1',}),
        'ebay_category': forms.TextInput(attrs={'class': 'form-control m-1',}),
    }
)

# CompanyAccountsFormSet = modelformset_factory(
#     CompanyAccounts, fields=['company_account'], extra=1,
#     widgets=forms.TextInput(
#         attrs={
#             'class': 'form-control',
#         }
#         ),
# )


class AuctionsSearchForm(forms.Form):
    error_css_class = 'error'
    
    external_id = forms.IntegerField(
        # input_formats=['\d'],
        # min_value=1, 
        # max_value=999999999999, 
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "External ID",
                }
        ),
        required=False,
        #error_messages={
        #    'invalid': 'Please let us know what to call you!'
        #    },

    )

    title = forms.CharField( 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Title",
                }
        ),
        required=False,
    )

    auction_account = forms.ModelChoiceField(
        queryset=CompanyAccounts.objects.filter(visible__exact=1).order_by('company_account'),
        empty_label='',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                }
            ),
        required=False,
        )
    
    AUCTIONS_DISPLAY_CHOICES = [
        ('1', 'All'), 
        ('2', 'Not downloaded'),
        ('3', 'Downloaded'),
    ]

    auctions_display = forms.ChoiceField(
        label='Choose download type:',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ), 
        choices=AUCTIONS_DISPLAY_CHOICES,
        initial=1,
        required=False,
        )

    AUCTION_SELECTED_CHOICES = formsebapp.FormsEbApp \
        .generateSelectModelChoicesPlusEmpty(None, Auctions.AUCTION_SELECT_CHOICES)

    selected = forms.ChoiceField(
        label='Choose if auction was selected:',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=AUCTION_SELECTED_CHOICES,
        required=False, 
        ) 

    status = forms.ChoiceField(
        label='Choose if auction was confirmed:',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=Auctions.AUCTION_STATUS_CONFIRM_CHOICES,
        required=False, 
        )

    def clean_external_id(self):
        field_name = 'external_id'

        cd = self.cleaned_data

        external_id = cd.get(field_name)

        if (len(str(external_id)) != 12 or not str(external_id).isdigit()) and external_id is not None:
            raise ValidationError('Required 12 digits in input')

        return external_id

class AddAuctionsForm(forms.Form):
    error_css_class = 'error'

    MAX_NUMBER_OF_ADDING_MULTIPLE_AUCTIONS = 20

    ADD_AUCTIONS_TYPE_SINGLE = 0
    ADD_AUCTIONS_TYPE_MULTIPLE = 1

    ADD_AUCTIONS_TYPE_CHOICES = [
        (ADD_AUCTIONS_TYPE_SINGLE,'Single'),
        (ADD_AUCTIONS_TYPE_MULTIPLE,'Multiple'),
    ]

    add_auctions_type = forms.ChoiceField(
        label='Choose add type:',
        widget=forms.RadioSelect(attrs={
            'class': '',
        }), 
        choices=ADD_AUCTIONS_TYPE_CHOICES,
        )

    add_auction_single = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control input-auctions disabled',
            'placeholder':'Example: {https://www.ebay.de/itm/Jack-Jones-Sweat-Pullover-Hoodie/193151203742} or {193151203742}',
        }),
        help_text='',
        required=False,
        disabled=False,
        # initial='124186915408'
    )

    add_auctions_multiple = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control input-auctions disabled',
            'placeholder': '',
            'rows': 5,
            }),
        help_text=f"Separate each auctions by new line. Max {MAX_NUMBER_OF_ADDING_MULTIPLE_AUCTIONS} auctions.",
        required=False,
        disabled=False,
        # initial='124464832617',
    )

    def clean(self):
    #     """
    #     In here you can validate the two fields
    #     raise ValidationError if you see anything goes wrong. 
    #     """
        cleaned_data = super().clean()

        single_field = 'add_auction_single'
        multiple_field = 'add_auctions_multiple'
        
        add_auctions_type = cleaned_data.get('add_auctions_type')
        add_auction_single = cleaned_data.get(single_field, '')
        add_auctions_multiple = cleaned_data.get(multiple_field, '')


        if add_auctions_type == str(self.ADD_AUCTIONS_TYPE_SINGLE):

            external_id = formsebapp.FormsEbApp.checkForExternalId(None, add_auction_single)

            if external_id is not None:
                self.cleaned_data[single_field] = external_id
            else:
                self.add_error(single_field, 'Required 12 digits in input.')

        if add_auctions_type == str(self.ADD_AUCTIONS_TYPE_MULTIPLE):
            if add_auctions_multiple == '':
                self.add_error(multiple_field, 'Required. Provide auction(s).')
            else:
                new_multiple = add_auctions_multiple.splitlines()

                if len(new_multiple) <= self.MAX_NUMBER_OF_ADDING_MULTIPLE_AUCTIONS:

                    i = 0

                    while i < len(new_multiple):
                        row_data = new_multiple[i]
                        
                        external_id = formsebapp.FormsEbApp.checkForExternalId(None, row_data)
                        
                        if external_id is not None:
                            new_multiple[i] = external_id
                        else:
                            self.add_error(multiple_field, f'Required 12 digits in input row[{i+1}].')
                        
                        i +=1

                    # remove duplicates
                    new_multiple = list( dict.fromkeys(new_multiple) )

                    self.cleaned_data[multiple_field] = new_multiple

                else:
                    self.add_error(multiple_field, f"You provided too many lines. (Max {self.MAX_NUMBER_OF_ADDING_MULTIPLE_AUCTIONS}).")


        return self.cleaned_data

class AuctionsDetailsForm(forms.ModelForm):

    FORM_AUCTION_FORMAT_CHOICES = formsebapp.FormsEbApp.generateSelectModelChoicesPlusEmpty(
        None, AuctionsDetails.AUCTION_FORMAT_CHOICES)

    items_stock = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    price_normal = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': '0,00',}), localize=True)
    price_uvp = forms.DecimalField(label='UVP', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'class': "form-control form-control-sm", 'placeholder': '0,00', 'readonly': False}), localize=True)
    auction_format = forms.CharField(
        widget=forms.Select(
            choices=FORM_AUCTION_FORMAT_CHOICES,
            attrs={'class':'form-control'})
        )

    def clean_items_stock(self):
        cd = self.cleaned_data

        items_stock = cd.get('items_stock')

        if items_stock == 0:
            raise ValidationError('Required stock to be more than 0.')

        return items_stock

    class Meta:
        model = AuctionsDetails
        fields = [
            'items_stock',
            'price_normal',
            'price_uvp',
            'auction_format',
        ]

class UpdateAuctionForm(forms.ModelForm):
    title_auction = forms.CharField(
        max_length=Auctions._meta.get_field('title_auction').max_length, 
        widget=forms.TextInput(attrs={'class': "form-control"}))
    seller_comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control','rows': 1,}),)

    selected = forms.CharField(widget=forms.Select(
        choices=Auctions.AUCTION_SELECT_CHOICES,
        attrs={'class': 'form-control'}))

    #TODO
    # ! WORKING - but not refresh data on website without restarting server
    # ! not working during tests

    #ebay_category_query = Settings.objects.all().values('ebay_category').last()
    # EBAY_CATEGORY_CHOICES = formsebapp.FormsEbApp.generateSelectChoices(
    # None, query_result=ebay_category_query, query_result_columnname='ebay_category',empty_firstline=False)
    # ebay_category = forms.CharField(widget=forms.Select(
    #     # choices=EBAY_CATEGORY_CHOICES,
    #     attrs={'class': 'form-control'}))

    ebay_category = forms.ModelChoiceField(
        queryset=EbayCategories.objects.all().order_by('position', 'ebay_category'),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                }
            )
        )

    class Meta:
        model = Auctions
        fields = [
            'selected',
            'title_auction',
            'seller_comment',
            'ebay_category',
        ]


class AddAuctionSingleForm(UpdateAuctionForm):
    external_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': "form-control form-control-sm", 'readonly': True}))
    img_auction = forms.URLField(max_length=150, widget=forms.TextInput(attrs={'class': "form-control form-control-sm", 'readonly': True}))
    auction_account = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': "form-control form-control-sm", 'readonly': True}))

    class Meta:
        model = Auctions
        fields = [
            'selected',
            'title_auction',
            'seller_comment',
            'ebay_category',
            'external_id', 
            # 'private_id',
            'img_auction',
            'auction_account',
        ]



# AuctionsFormSet = inlineformset_factory(
#     Auctions, AuctionsDetails, form=AddAuctionForm,
#     fields=[
#         'price_normal',
#         'price_uvp',
#         'items_stock',
#         'auction_format'

#     ], extra=1
# )

class ReportsForm(forms.Form):
    # start_date = forms.DateField(
    #     input_formats=['%d/%m/%Y'],
    #     widget=forms.DateInput(
    #         attrs={
    #             'class': 'form-control datetimepicker-input',
    #             'data-target': '#id_start_date',
    #             'data-toggle': 'datetimepicker',
    #         }
    #     )
    # )

    # end_date = forms.DateField(
    #     input_formats=['%d/%m/%Y'],
    #     widget=forms.DateInput(
    #         attrs={
    #             'class': 'form-control datetimepicker-input',
    #             'data-target': '#id_end_date',
    #             'data-toggle': 'datetimepicker',
    #         }
    #     )
    # )

    company_accounts = forms.ModelChoiceField(
        queryset=CompanyAccounts.objects.filter(visible__exact=1).order_by('company_account'),
        # empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                }
            )
        )

    reports_type = forms.ChoiceField(
        label='Choose download type:',
        widget=forms.RadioSelect, 
        choices=Auctions.AUCTION_DOWNLOAD_CHOICES,
        # initial=1
        )

    promotion_date_start = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-control',
                'placeholder':'DD/MM/YYYY'
            }
        ),
        help_text = 'Select a date in format (DD/MM/YYYY).',
        initial=datetime.date.today
        )
