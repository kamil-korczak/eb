from django.contrib import admin

from ebapp.models import (
    CompanyAccounts,
    EbayCategories
)

# Register your models here.

admin.site.register(CompanyAccounts)
admin.site.register(EbayCategories)