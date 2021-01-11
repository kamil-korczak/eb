import json
from django.contrib.auth.mixins import LoginRequiredMixin
from ebapp.classes.mixins import StaffuserRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import messages

from urllib.parse import urlencode


from .models import (
        Auctions, AuctionsDetails,
        Settings
        )
from . import forms

from ebapp.classes.auctionsebayparser import AuctionsEbayParser
from ebapp.classes.report import Report
from ebapp.classes.formsebapp import FormsEbApp
from django.db.models import Count, Max
from django.db.models import FilteredRelation, Q
from django.db.models import OuterRef, Subquery


class AuctionsView(TemplateView):
    template_name = 'auctions.html'

    def get(self, request, page=1, **kwargs):

        data = request.GET

        c_external_id      = data.get('external_id', None)
        c_title            = data.get('title', '')
        c_auction_account  = data.get('auction_account', '')
        c_auctions_display = data.get('auctions_display', '1')
        c_status         = data.get('status', '1')
        c_selected         = data.get('selected', '')

        form_auctions_search = forms.AuctionsSearchForm(
            initial={
                'external_id': c_external_id,
                'title': c_title,               
                'auction_account': c_auction_account,               
                'auctions_display': c_auctions_display, 
                'status': c_status,              
                'selected': c_selected,              
            }
        )

        filter_args = {}

        filter_args['auction__archived__exact'] = 0

        if c_external_id:
            filter_args['auction__external_id__exact'] = c_external_id

        if c_title:
            filter_args['auction__title_auction__icontains'] = c_title

        if c_auction_account:
            filter_args['auction__auction_account__exact'] = c_auction_account

        if c_auctions_display and c_auctions_display != '1':
            if c_auctions_display == '2': # Not downloaded
                display_option = True

            if c_auctions_display == '3': # Downloaded
                display_option = False

            filter_args['auction__time_downloaded__isnull'] = display_option

        if c_status:
            filter_args['auction__status__exact'] = c_status


        if c_selected:
            filter_args['auction__selected__exact'] = c_selected
        
        try:
            
            auctions = AuctionsDetails.objects \
                .filter(**filter_args) \
                .order_by('-auction', '-pk').distinct('auction').select_related('auction')

            if auctions.count() == 0:
                auctions = None
                
                if c_external_id:
                    message = c_external_id
                else:
                    message = ''
                messages.error(request, f'Auction`s {message} does not exist.')

        except AuctionsDetails.DoesNotExist:
            auctions = None

        if auctions is not None:
            paginator = Paginator(auctions, 5)
            auctions = paginator.get_page(page)

        status_field = True if c_status == '0' else None

        args = {
            'auctions': auctions,
            'status_field': status_field,
            'nbar': 'home',
            'form_auctions_search': form_auctions_search,
        }

        return render(request, self.template_name, args)

    def post(self, request, page=1, **kwargs):

        auctions = None
        search_result = None

        form_auctions_search = forms.AuctionsSearchForm(request.POST)

        url_params = {}

        if form_auctions_search.is_valid():

            c_external_id       = form_auctions_search.cleaned_data['external_id']
            c_title             = form_auctions_search.cleaned_data['title']
            c_auction_account   = form_auctions_search.cleaned_data['auction_account']
            c_auctions_display  = form_auctions_search.cleaned_data['auctions_display']
            c_status            = form_auctions_search.cleaned_data['status']
            c_selected          = form_auctions_search.cleaned_data['selected']

            if c_external_id:
                url_params['external_id'] = c_external_id

            else:
                if c_title:
                    url_params['title'] = c_title

                if c_auction_account:
                    url_params['auction_account'] = c_auction_account

                if c_auctions_display and c_auctions_display != '1':
                    url_params['auctions_display'] = c_auctions_display

                if c_status:
                    url_params['status'] = c_status
                
                if c_selected:
                    url_params['selected'] = c_selected

            QM = '?' if url_params else ''

            return redirect(f'/{QM}{urlencode(url_params)}')    

        else:
            for field in form_auctions_search.errors:
                form_auctions_search[field].field.widget.attrs['class'] += ' is-invalid'

        args = {
            'auctions': auctions,
            'nbar': 'home',
            'form_auctions_search': form_auctions_search,
            'search_result': search_result,
        }

        return render(request, self.template_name, args)

class AuctionsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'auction_page.html'

    def get(self, request, **kwargs):

        external_id = kwargs.pop('external_id')

        try:
            auction = AuctionsDetails.objects \
                .filter(auction__external_id__exact=external_id) \
                .select_related('auction') \
                .last()
            
        except AuctionsDetails.DoesNotExist:
            auction = None

        args = {
            'external_id': external_id,
            'auction': auction,
        }

        if auction:
            form_auction = forms.UpdateAuctionForm(instance=auction.auction)
            form_auction_details = forms.AuctionsDetailsForm(instance=auction) 

            args['form_auction'] = form_auction
            args['form_auction_details'] = form_auction_details

        return render(request, self.template_name, args)

    def post(self, request, external_id=None):

        try:
            auction_details = AuctionsDetails.objects \
                .filter(auction__external_id__exact=external_id) \
                .select_related('auction') \
                .last()

            auction = Auctions.objects.filter(external_id=external_id).last()
            
        except Auctions.DoesNotExist:
            auction = None

        form_auction = forms.UpdateAuctionForm(request.POST, instance=auction)
        form_auction_details = forms.AuctionsDetailsForm(request.POST, instance=auction_details)

        if form_auction.is_valid() and form_auction_details.is_valid():
            
            messages.success(request, f'#{auction.id} updated successfully')
            form_auction.save()
            form_auction_details.save()

            if auction_details.auction.status == Auctions.AUCTION_STATUS_NOTCONFIRMED:
                auction_details.auction.status = Auctions.AUCTION_STATUS_CONFIRMED
                Auctions.objects.filter(external_id=external_id).update(status=Auctions.AUCTION_STATUS_CONFIRMED)

        args = {
            'auction': auction_details,
            'form_auction': form_auction,
            'form_auction_details': form_auction_details,
        }

        return render(request, self.template_name, args)

class AuctionsAddPageView(LoginRequiredMixin, TemplateView):
    template_name = 'auctions_add.html'

    def get(self, request, add_type=None):

        initial = {}

        if add_type == str.lower(forms.AddAuctionsForm.
            ADD_AUCTIONS_TYPE_CHOICES[forms.AddAuctionsForm.ADD_AUCTIONS_TYPE_SINGLE][1]
            ):
            initial['add_auctions_type'] = forms.AddAuctionsForm.ADD_AUCTIONS_TYPE_SINGLE

        if add_type == str.lower(forms.AddAuctionsForm.
            ADD_AUCTIONS_TYPE_CHOICES[forms.AddAuctionsForm.ADD_AUCTIONS_TYPE_MULTIPLE][1]
            ):
            initial['add_auctions_type'] = forms.AddAuctionsForm.ADD_AUCTIONS_TYPE_MULTIPLE

        form_add_auctions = forms.AddAuctionsForm(initial=initial)

        args = {
            'form': form_add_auctions,
        }

        return render(request, self.template_name, args)

    def post(self, request, **kwargs):

        form_add_auctions = forms.AddAuctionsForm(request.POST)

        if form_add_auctions.is_valid():
            cd = form_add_auctions.cleaned_data
            
            if cd.get('add_auctions_type') == str(form_add_auctions.ADD_AUCTIONS_TYPE_SINGLE):

                external_id = cd.get('add_auction_single')

                auctionsebayparser = AuctionsEbayParser()

                auctionsebayparser.setDataFromEbayAuction(request=request, external_id=external_id)
                
                auction_data_raw = auctionsebayparser.getDataAuctionRaw()

                auction_data = auctionsebayparser.parseDataFromEbayAuction(ebay_data=auction_data_raw)

                request.session['auction_data'] = auction_data

                return redirect('auctions-add-single')

            elif cd.get('add_auctions_type') == str(form_add_auctions.ADD_AUCTIONS_TYPE_MULTIPLE):
                multiple_auctions = cd.get('add_auctions_multiple')

                if len(multiple_auctions) == 1:

                    external_id = multiple_auctions[0]

                    auctionsebayparser = AuctionsEbayParser()

                    auctionsebayparser.setDataFromEbayAuction(request=request, external_id=external_id)
                    
                    auction_data_raw = auctionsebayparser.getDataAuctionRaw()

                    auction_data = auctionsebayparser.parseDataFromEbayAuction(ebay_data=auction_data_raw)

                    request.session['auction_data'] = auction_data

                    return redirect('auctions-add-single')
                else:

                    a_ebapp = AuctionsEbayParser()

                    a_ebapp.getDataAndSaveMultiple(request, multiple_auctions)

                    return redirect('/auctions/?status=0')

        else:
            for field in form_add_auctions.errors:
                form_add_auctions[field].field.widget.attrs['class'] += ' is-invalid'

        # if form_add_auction.is_valid() and form_add_auction_details.is_valid():
        #     field_name = 'external_id'

        #     messages.success(request, f'#{form_add_auction.cleaned_data[field_name]}')

        #     save_form_add_auction = form_add_auction.save()
            
        #     save_form_auction_details = form_add_auction_details.save(commit=False)
        #     save_form_auction_details.auction = save_form_add_auction

        #     save_form_auction_details.save()

        #     return redirect(f'/auctions/{form_add_auction.cleaned_data[field_name]}/')
        
        args = {
            'form': form_add_auctions,
        }
        
        return render(request, self.template_name, args)

class AuctionsAddSinglePageView(LoginRequiredMixin, TemplateView):
    template_name = 'auction_add_single.html'

    def get(self, request, **kwargs):

        session_auction_data = request.session.get('auction_data', None)

        auction_data = {}

        if session_auction_data:

            external_id = auction_data['external_id'] = session_auction_data.get('external_id', None)
            auction_data['title_auction'] = session_auction_data.get('title_auction', None)
            auction_data['img_auction'] = session_auction_data.get('img_auction', None)
            auction_data['auction_account'] = session_auction_data.get('auction_account', None)
            
            auction_data['price_normal'] = session_auction_data.get('price_normal', None)
            auction_data['price_uvp'] = session_auction_data.get('price_uvp', None)
            
            try:
                auction = Auctions.objects.get(external_id=external_id)
            except Auctions.DoesNotExist:
                auction = None

            if auction is not None:
                auction_status = 'update'
            else:
                auction_status = 'add'


            del request.session['auction_data']
        else:
            return redirect('/auctions/add/single/')

        form_add_auction = forms.AddAuctionSingleForm(initial = auction_data)

        form_auction_details = forms.AuctionsDetailsForm(initial = auction_data)

        args = {
            'auction_status': auction_status,
            'auction_data': auction_data,
            'form_add_auction': form_add_auction,
            'form_auction_details': form_auction_details,
        }

        return render(request, self.template_name, args)

    def post(self, request, **kwargs):
        field_name = 'external_id'

        auction_data = True

        external_id = request.POST.get(field_name, 0)

        auction = Auctions.objects.filter(external_id=external_id).order_by('id').last()

        form_add_auction = forms.AddAuctionSingleForm(request.POST, instance=auction)
        form_auction_details = forms.AuctionsDetailsForm(request.POST)

        if auction is None:
                auction_status = 'add'
        else:
                auction_status = 'update'

        if form_add_auction.is_valid() and form_auction_details.is_valid():


            save_form_add_auction = form_add_auction.save()
            
            save_form_auction_details = form_auction_details.save(commit=False)
            save_form_auction_details.auction = save_form_add_auction

            save_form_auction_details.save()

            if auction is None:
                message_info = 'Added'
                
                auction = Auctions.objects.get(external_id=external_id)
                auction.status = Auctions.AUCTION_STATUS_CONFIRMED
                auction.save()
            else:
                message_info = 'Updated'

            # auction.status = Auctions.AUCTION_STATUS_CONFIRMED


            messages.success(request, f'{message_info} #{form_add_auction.cleaned_data[field_name]}')

            return redirect(f'/auctions/{form_add_auction.cleaned_data[field_name]}/')

        
        args = {
            'auction_status': auction_status,
            'auction_data': auction_data,
            'form_add_auction': form_add_auction,
            'form_auction_details': form_auction_details,
        }

        return render(request, self.template_name, args)

class SettingsView(StaffuserRequiredMixin, LoginRequiredMixin, TemplateView): #LoginRequiredMixin
    # raise_exception = True
    template_name = 'settings.html'

    def get(self, request, **kwargs):
        
        settings_objects = Settings.objects.last()
        
        form_settings = forms.SettingsForm(instance=settings_objects)

        formset_company_accounts = forms.CompanyAccountsFormSet(prefix='account')


        formset_ebay_categories = forms.EbayCategoriesFormset(prefix='ebay-category')

        args = {
            'settings': settings_objects,
            'form_settings': form_settings,
            'formset_company_accounts': formset_company_accounts,
            'formset_ebay_categories': formset_ebay_categories,
        }

        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        settings_objects = Settings.objects.last()


        form_settings = forms.SettingsForm(request.POST or None, 
            instance=settings_objects)

        formset_company_accounts = forms.CompanyAccountsFormSet(request.POST, prefix='account')

        formset_ebay_categories = forms.EbayCategoriesFormset(request.POST, prefix='ebay-category')

        if form_settings.is_valid() and \
            formset_company_accounts.is_valid() and \
            formset_ebay_categories.is_valid():

            form_settings.save()
            formset_company_accounts.save()
            formset_ebay_categories.save()

            messages.success(request, 'Settings updated successfully')

            return redirect('settings')
        else: 
            
            for form in formset_company_accounts:
                for field in form.errors:
                    form[field].field.widget.attrs['class'] += ' is-invalid'

            for form in formset_ebay_categories:
                for field in form.errors:
                    form[field].field.widget.attrs['class'] += ' is-invalid'

            for field in form_settings.errors:
                form_settings[field].field.widget.attrs['class'] += ' is-invalid'



            messages.error(request, form_settings.errors)

        args = {
            'settings': settings_objects,
            'form_settings': form_settings,
            'formset_company_accounts': formset_company_accounts,
            'formset_ebay_categories': formset_ebay_categories,
        }

        return render(request, self.template_name, args)

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports.html'

    def get(self, request, **kwargs):

        form_reports = forms.ReportsForm()

        args = {
            'form_reports': form_reports,
            'nbar': 'reports',
        }

        return render(request, self.template_name, args)

    def post(self, request, **kwargs):


        form_reports = forms.ReportsForm(request.POST)

        args = {
            'form_reports': form_reports,
            'nbar': 'reports',
        }


        if form_reports.is_valid():

            c_company_accounts = form_reports.cleaned_data['company_accounts']
            c_reports_type = form_reports.cleaned_data['reports_type']
            c_promotion_date_start = form_reports.cleaned_data['promotion_date_start']
            

            filter_args = {
                'auction__auction_account__exact': c_company_accounts,
                'auction__status__exact': 1,
                'auction__archived__exact': 0,
            }

            if c_reports_type == str(Auctions.AUCTION_DOWNLOAD_SELECTED):
                filter_args['auction__selected__exact'] = 1

            if c_reports_type == str(Auctions.AUCTION_DOWNLOAD_NEWLY_ADDED):
                filter_args['auction__time_downloaded__isnull'] = True

            auctions_details = AuctionsDetails.objects   \
            .filter(**filter_args) \
            .order_by('-auction', '-pk')    \
                .distinct('auction')    \
                .select_related('auction')

            settings = Settings.objects.all().last()

            report_response = Report.generate(Report(c_company_accounts, c_promotion_date_start, settings), auctions_details)

            # print(report_response)


            return report_response

        else:

            return render(request, self.template_name, args)

def error_404_view(request, *args, **kwarg):
    template_name = '404.html'

    return render(request, template_name, '')