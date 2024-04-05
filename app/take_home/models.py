from django.db import models
from django.utils import timezone

class Ticker(models.Model):
    ticker = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    market = models.CharField(max_length=50)
    locale = models.CharField(max_length=50)
    primary_exchange = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50)
    active = models.BooleanField()
    currency_name = models.CharField(max_length=50)
    cik = models.CharField(max_length=50, null=True)
    composite_figi = models.CharField(max_length=200, blank=True, null=True)
    share_class_figi = models.CharField(max_length=200, blank=True, null=True)
    last_updated_utc = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.ticker


class Asset(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    last_updated = models.DateTimeField()
    market_cap = models.BigIntegerField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    address1 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    sic_code = models.CharField(max_length=10, null=True)
    sic_description = models.CharField(max_length=200, null=True)
    ticker_root = models.CharField(max_length=50, null=True)
    homepage_url = models.URLField(null=True)
    total_employees = models.IntegerField(null=True)
    list_date = models.DateField(null=True)
    logo_url = models.URLField(null=True)
    icon_url = models.URLField(null=True)
    share_class_shares_outstanding = models.BigIntegerField(null=True)
    weighted_shares_outstanding = models.BigIntegerField(null=True)
    round_lot = models.IntegerField(null=True)

    @classmethod
    def update_or_create_from_api(cls, api_data):
        ticker_data = api_data.get('results', {})
        ticker, _ = Ticker.objects.update_or_create(
            ticker=ticker_data.get('ticker'),
            defaults={
                'name': ticker_data.get('name'),
                'market': ticker_data.get('market'),
                'locale': ticker_data.get('locale'),
                'primary_exchange': ticker_data.get('primary_exchange'),
                'type': ticker_data.get('type'),
                'active': ticker_data.get('active'),
                'currency_name': ticker_data.get('currency_name'),
                'cik': ticker_data.get('cik'),
                'composite_figi': ticker_data.get('composite_figi'),
                'share_class_figi': ticker_data.get('share_class_figi'),
                'last_updated_utc': ticker_data.get('last_updated_utc'),
            }
        )

        asset_data = api_data.get('results', {})
        return cls.objects.create(
            ticker=ticker,
            name=asset_data.get('name'),
            symbol=asset_data.get('ticker'),
            type=asset_data.get('type'),
            last_updated=timezone.now(),
            market_cap=asset_data.get('market_cap'),
            phone_number=asset_data.get('phone_number'),
            address1=asset_data.get('address', {}).get('address1'),
            city=asset_data.get('address', {}).get('city'),
            state=asset_data.get('address', {}).get('state'),
            postal_code=asset_data.get('address', {}).get('postal_code'),
            description=asset_data.get('description'),
            sic_code=asset_data.get('sic_code'),
            sic_description=asset_data.get('sic_description'),
            ticker_root=asset_data.get('ticker_root'),
            homepage_url=asset_data.get('homepage_url'),
            total_employees=asset_data.get('total_employees'),
            list_date=asset_data.get('list_date'),
            logo_url=asset_data.get('branding', {}).get('logo_url'),
            icon_url=asset_data.get('branding', {}).get('icon_url'),
            share_class_shares_outstanding=asset_data.get('share_class_shares_outstanding'),
            weighted_shares_outstanding=asset_data.get('weighted_shares_outstanding'),
            round_lot=asset_data.get('round_lot'),
        )

    def __str__(self):
        return self.name
