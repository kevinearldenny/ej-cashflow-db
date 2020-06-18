from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from pprint import pprint
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from datetime import datetime

from .models import Company, SharesOutstanding, PublicFloat, Company10kRecord
from companies.scripts.scrape_edgar import get_edgar_data

class IndexView(generic.ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Company.objects.all().order_by('-added_on')



class DetailView(generic.DetailView):
    model = Company
    slug_field = 'ticker_symbol'
    template_name = 'companies/detail.html'

    def get_queryset(self):
        """
        Excludes companies with no 10k records
        """
        return Company.objects.all()

def make_company_record(c):
    co = Company.objects.create(
        ticker_symbol=str(c['ticker_symbol']).upper(),
        index_key=str(c['index_key']),
        tax_id=str(c['Entity Tax Identification Number']),
        phone_number=str(c['City Area Code']) + '-' + str(c['Local Phone Number']),
        exchange=str(c['Security Exchange Name'])
    )
    co.save()

    so = SharesOutstanding.objects.create(
        company=co,
        shares_outstanding=int(c['shares_outstanding']['value']),
        date=datetime.strptime(c['shares_outstanding']['date'], '%Y-%m-%d')
    )
    so.save()

    pf = PublicFloat.objects.create(
        company=co,
        public_float=int(c['public_float']['value']),
        date=datetime.strptime(c['public_float']['date'], '%Y-%m-%d')
    )
    pf.save()

    tenk = Company10kRecord.objects.create(
        company=co,
        fy_focus=str(c['Document Fiscal Year Focus']),
        annual_report=bool(c['Document Annual Report']),
        transition_report=bool(c['Document Transition Report']),
        fy_end_date=datetime.strptime(c['doc_end_date'], '%Y-%m-%d')
    )
    tenk.save()

    return co

def create_company(request):
    ticker = str(request.POST['ticker']).upper()
    comp_exists = Company.objects.filter(ticker_symbol=ticker)
    if len(comp_exists) == 0:
        data = get_edgar_data(ticker)
        if data:
            comp = make_company_record(data)
            # return HttpResponseRedirect(reverse('companies:index'))
            return HttpResponseRedirect(reverse('companies:detail', args=(comp.ticker_symbol,)))

        else:
            return HttpResponseRedirect(reverse('companies:index'))
    else:
        comp = comp_exists[0]
        return HttpResponseRedirect(reverse('companies:detail', args=(comp.ticker_symbol,)))
