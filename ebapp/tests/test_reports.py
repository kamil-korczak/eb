import datetime

import pytest

from django.core.management import call_command

from ebapp.tests.helper.auction_helper import AuctionExpected

from ebapp.classes.report import Report
from ebapp.models import Auctions, AuctionsDetails, Settings

TEST_SETTINGS_JSON_DIR = 'ebapp/tests/test_files/json/'

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', f'{TEST_SETTINGS_JSON_DIR}settings_data.json')
        call_command('loaddata', f'{TEST_SETTINGS_JSON_DIR}auctions_data.json')
        call_command('loaddata', f'{TEST_SETTINGS_JSON_DIR}auctionsdetails_data.json')

# pytestmark = pytest.mark.django_db
@pytest.mark.django_db
class TestAuctions:
  
    def test_report(self, django_db_setup):
        company_account = 'redox-fashion'
        promotion_date_start = datetime.date.today()
        settings = Settings.objects.last()

        # initiate report 
        report = Report(company_account, promotion_date_start, settings)

        filter_args = {
            'auction__auction_account__exact': company_account,
            'auction__status__exact': 1,
            'auction__archived__exact': 0,
        }

        auctions_details = AuctionsDetails.objects.filter(**filter_args) \
            .order_by('-auction', '-pk').distinct('auction').select_related('auction')

        report_response = report.generate(auctions_details)

        assert report_response.status_code == 200 and report_response['content-type'] == 'application/ms-excel' 