from django import forms

class AssetSearchForm(forms.Form):
    ticker = forms.CharField(label='Ticker', required=False)
    type_choices = [
        ("", "Select Type"),  
        ("CS", "Common Stock"),
        ("PFD", "Preferred Stock"),
        ("WARRANT", "Warrant"),
        ("RIGHT", "Rights"),
        ("BOND", "Corporate Bond"),
        ("ETF", "Exchange Traded Fund"),
        ("ETN", "Exchange Traded Note"),
        ("ETV", "Exchange Traded Vehicle"),
        ("SP", "Structured Product"),
        ("ADRC", "American Depository Receipt Common"),
        ("ADRP", "American Depository Receipt Preferred"),
        ("ADRW", "American Depository Receipt Warrants"),
        ("ADRR", "American Depository Receipt Rights"),
        ("FUND", "Fund"),
        ("BASKET", "Basket"),
        ("UNIT", "Unit"),
        ("LT", "Liquidating Trust"),
        ("OS", "Ordinary Shares"),
        ("GDR", "Global Depository Receipts"),
        ("OTHER", "Other Security Type"),
        ("NYRS", "New York Registry Shares"),
        ("AGEN", "Agency Bond"),
        ("EQLK", "Equity Linked Bond"),
        ("ETS", "Single-security ETF"),
    ]
    type = forms.ChoiceField(choices=type_choices, required=False)
    market_choices = [
        ("", "Select Market"), 
        ("stocks", "Stocks"),
        ("crypto", "Cryptocurrency"),
        ("fx", "Forex"),
        ("otc", "Over-the-counter"),
        ("indices", "Indices"),
    ]
    market = forms.ChoiceField(choices=market_choices, required=False)
    exchange = forms.CharField(label='Exchange', required=False)
    cusip = forms.CharField(label='CUSIP', required=False)
    cik = forms.CharField(label='CIK', required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    search = forms.CharField(label='Search', required=False)
    active_choices = [
        ("", "Select Active"),  
        (True, "True"),
        (False, "False"),
    ]
    active = forms.ChoiceField(choices=active_choices, required=False)
    order_choices = [
        ("", "Select Order"),  
        ("asc", "Ascending"),
        ("desc", "Descending"),
    ]
    order = forms.ChoiceField(choices=order_choices, required=False)
    limit = forms.IntegerField(label='Limit', required=False)
    sort_choices = [
    ("", "Select Sort"), 
    ("ticker", "Ticker"),
    ("name", "Name"),
    ("market", "Market"),
    ("locale", "Locale"),
    ("primary_exchange", "Primary Exchange"),
    ("type", "Type"),
    ("currency_symbol", "Currency Symbol"),
    ("currency_name", "Currency Name"),
    ("base_currency_symbol", "Base Currency Symbol"),
    ("base_currency_name", "Base Currency Name"),
    ("cik", "CIK"),
    ("composite_figi", "Composite FIGI"),
    ("share_class_figi", "Share Class FIGI"),
    ("last_updated_utc", "Last Updated (UTC)"),
    ("delisted_utc", "Delisted (UTC)"),
    ]
    sort = forms.ChoiceField(choices=sort_choices, required=False)
