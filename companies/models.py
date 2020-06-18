from django.db import models
from datetime import datetime

# Create your models here.

class Company(models.Model):
    ticker_symbol = models.CharField(max_length=20, primary_key=True)
    registered_name = models.CharField(max_length=1000, blank=True, null=True)
    index_key = models.CharField(max_length=50, blank=True, null=True)
    added_on = models.DateField(auto_now_add=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    exchange = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.ticker_symbol

class Company10kRecord(models.Model):
    company = models.ForeignKey(Company, related_name='records_10k', on_delete=models.CASCADE)
    fy_focus = models.CharField(max_length=4)
    annual_report = models.BooleanField(default=False)
    transition_report = models.BooleanField(default=False)
    fy_end_date = models.DateField()


    def __str__(self):
        return self.company.ticker_symbol

class SharesOutstanding(models.Model):
    company = models.ForeignKey(Company, related_name='shares_outstanding', on_delete=models.CASCADE)
    date = models.DateField()
    shares_outstanding = models.IntegerField()

    def __str__(self):
        return self.company.ticker_symbol + ' shares outstanding on {0}'.format(self.date.strftime('%Y-%m-%d'))

class PublicFloat(models.Model):
    company = models.ForeignKey(Company, related_name='public_float', on_delete=models.CASCADE)
    date = models.DateField()
    public_float = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.company.ticker_symbol + ' public float on {0}'.format(self.date.strftime('%Y-%m-%d'))