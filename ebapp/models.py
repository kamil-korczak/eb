from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class Auctions(models.Model):
    AUCTION_DOWNLOAD_ALL = 1
    AUCTION_DOWNLOAD_SELECTED = 2
    AUCTION_DOWNLOAD_NEWLY_ADDED = 3

    AUCTION_DOWNLOAD_CHOICES = [
        (AUCTION_DOWNLOAD_SELECTED, 'Selected auctions'), 
        (AUCTION_DOWNLOAD_NEWLY_ADDED, 'Newly added auctions'),
        (AUCTION_DOWNLOAD_ALL, 'All auctions'), 
    ]

    AUCTION_STATUS_NOTCONFIRMED = 0
    AUCTION_STATUS_CONFIRMED = 1

    AUCTION_STATUS_CONFIRM_CHOICES = [
        (AUCTION_STATUS_CONFIRMED, 'Confirmed'),
        (AUCTION_STATUS_NOTCONFIRMED, 'Not Confirmed'),
    ]

    AUCTION_NOT_SELECTED = 0
    AUCTION_SELECTED = 1

    AUCTION_SELECT_CHOICES = (
        (AUCTION_NOT_SELECTED, 'Not selected'), 
        (AUCTION_SELECTED, 'Selected')
    )

    """ Auctions model """
    external_id = models.BigIntegerField(validators=[MinValueValidator(100000000000), MaxValueValidator(999999999999)], unique=True) #12 digits #, unique=True
    private_id = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999999999)], default=0) #6
    title_auction = models.CharField(max_length=80)
    img_auction = models.URLField(max_length=150)
    seller_comment = models.TextField(max_length=250, default='', blank=True, null=True)
    auction_account = models.CharField(max_length=20)
    ebay_category = models.CharField(max_length=150)
    selected = models.IntegerField(choices=AUCTION_SELECT_CHOICES, default=0)
    archived = models.IntegerField(choices=AUCTION_SELECT_CHOICES, default=0)
    status = models.IntegerField(choices=[(0, 'Not archived'), (1, 'Archived')], default=0)
    time_added = models.DateTimeField(auto_now_add=True, editable=False)
    time_downloaded = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.external_id)

    #is_in_buffor

class AuctionsDetails(models.Model):
    AUCTION_DAILY = 0
    AUCTION_WEEKLY = 1
    AUCTION_BOTH = 2

    AUCTION_FORMAT_CHOICES = (
        (AUCTION_DAILY, 'wow! angebot des tages'),
        (AUCTION_WEEKLY, 'wow! angebot der woche'),
        (AUCTION_BOTH, 'BOTH')
    )

    auction = models.ForeignKey(Auctions,related_name='details', on_delete=models.CASCADE)
    items_stock = models.IntegerField(default=0) #stock
    price_normal = models.DecimalField(max_digits=5, decimal_places=2)
    price_uvp = models.DecimalField(max_digits=5, decimal_places=2)
    # auction_format = models.IntegerField(choices=[(AUCTION_DAILY, 'wow! angebot des tages'), (AUCTION_WEEKLY, 'wow! angebot der woche'), (AUCTION_BOTH, 'daily & weekly')], default=None, blank=True, null=True) #weekly/daily
    auction_format = models.IntegerField(choices=AUCTION_FORMAT_CHOICES, default=None, blank=True, null=True) #weekly/daily
    #data modyfikacji
    #data dodania
    #data sciagniecia



class Settings(models.Model):
    seller_email = models.EmailField(max_length=254)
    company_accounts = models.TextField() # TODO to delete
    target_website_for_wow_offer = models.IntegerField()
    ebay_category = models.TextField() # TODO to delete
    
class CompanyAccounts(models.Model):
    company_account = models.CharField(max_length=150, unique=True)
    visible = models.IntegerField(choices=[(0, 'Hidden'), (1, "Visible")], default=1)

    def __str__(self):
        return self.company_account

class EbayCategories(models.Model):
    position = models.IntegerField(default=0)
    ebay_category = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.ebay_category
