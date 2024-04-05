import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Asset, Ticker
from polygon import RESTClient
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render
from .forms import AssetSearchForm
from .serializers import AssetSerializer
from django.utils import timezone
import datetime

def home(request):
    try:
        # Perform a query to the Asset table to retrieve all objects
        assets = Asset.objects.all()

        # Check if the list of assets is empty
        if assets:
            message = "Connection and query were successful. The list of assets is not empty."
        else:
            message = "Connection and query were successful, but the list of assets is empty."

    except Exception as e:
        # If there is any database connection error, catch it and display an error message
        return render(request, 'error.html', {'error_message': f"Database connection error: {e}", 'assets': None})
    
    # If the query is successful, render the home view with the obtained objects and the message
    return render(request, 'home.html', {'assets': assets, 'message': message})

def asset_search(request):
    if request.method == 'GET':
        form = AssetSearchForm(request.GET)
        if form.is_valid():
            # Get the form parameters
            ticker = form.cleaned_data.get('ticker').upper()
            type = form.cleaned_data.get('type')
            market = form.cleaned_data.get('market')
            exchange = form.cleaned_data.get('exchange')
            cusip = form.cleaned_data.get('cusip')
            cik = form.cleaned_data.get('cik')
            date = form.cleaned_data.get('date')
            search = form.cleaned_data.get('search')
            active = form.cleaned_data.get('active')
            order = form.cleaned_data.get('order')
            limit = form.cleaned_data.get('limit')
            sort = form.cleaned_data.get('sort')

            # Check if the date is present in the form parameters
            if not date:
                # If the date is not present, assign the current date
                date = datetime.date.today().strftime('%Y-%m-%d')

            params = {
                'ticker': ticker,
                'type': type,
                'market': market,
                'exchange': exchange,
                'cusip': cusip,
                'cik': cik,
                'date': date,
                'search': search,
                'active': active,
                'order': order,
                'limit': limit,
                'sort': sort
            }

            # Remove parameters with empty values
            params = {k: v for k, v in params.items() if v}

            # Build URL with parameters for the first API
            base_url = "https://api.polygon.io/v3/reference/tickers?"
            url = f"{base_url}{urlencode(params)}&apiKey=JwJqJ4gpGp18ZSma2tlYR3D4jVVy1vLz"

            try:
                # Make GET request to the first API
                response = requests.get(url)
                data = response.json()
                if response.ok:
                    results = data.get('results', [])
                    tickers = [result['ticker'] for result in results]

                    # Filter all assets related to the obtained tickers
                    assets = Asset.objects.filter(ticker__ticker__in=tickers)

                    # Pass asset data to the template
                    context = {
                        'form': form,
                        'error_message': None,  # Optional: if no errors, set it to None
                        'assets': assets,
                    }
                    for result in results:
                        primary_exchange = result.get('primary_exchange', 'Other')

                        # Use get_or_create method to get an existing record or create a new one
                        ticker_obj, created = Ticker.objects.get_or_create(
                            ticker=result['ticker'],
                            defaults={
                                'name': result['name'],
                                'market': result['market'],
                                'locale': result['locale'],
                                'primary_exchange': primary_exchange,
                                'type': result['type'],
                                'active': True,
                                'currency_name': result['currency_name'],
                                'cik': result.get('cik'),
                                'composite_figi': result.get('composite_figi'),
                                'share_class_figi': result.get('share_class_figi'),
                                'last_updated_utc': result.get('last_updated_utc')}
                        )
                        # If the object already existed, update the fields with the new values
                        if not created:
                            ticker_obj.name = result['name']
                            ticker_obj.market = result['market']
                            ticker_obj.locale = result['locale']
                            ticker_obj.primary_exchange = primary_exchange
                            ticker_obj.type = result['type']
                            ticker_obj.active = result['active']
                            ticker_obj.currency_name = result['currency_name']
                            ticker_obj.cik = result.get('cik')
                            ticker_obj.composite_figi = result.get('composite_figi')
                            ticker_obj.share_class_figi = result.get('share_class_figi')
                            ticker_obj.last_updated_utc = result.get('last_updated_utc')
                            ticker_obj.save()

                        # Build URL for the second API
                        second_api_url = f"https://api.polygon.io/v3/reference/tickers/{result['ticker']}?apiKey=JwJqJ4gpGp18ZSma2tlYR3D4jVVy1vLz"
                        
                        # Make GET request to the second API
                        second_response = requests.get(second_api_url)
                        second_data = second_response.json()

                        
                        asset_obj = Asset.objects.create(
                            ticker=ticker_obj,
                            name=second_data.get('name', ''),
                            symbol=second_data.get('symbol', ''),
                            type=second_data.get('type', ''),
                            last_updated=second_data.get('last_updated_utc', timezone.now()),
                            address1=second_data.get('address1', ''),
                            city=second_data.get('city', ''),
                            description=second_data.get('description', ''),
                            homepage_url=second_data.get('homepage_url', ''),
                            icon_url=second_data.get('icon_url', ''),
                            list_date=second_data.get('list_date', None),
                            logo_url=second_data.get('logo_url', ''),
                            market_cap=second_data.get('market_cap', None),
                            phone_number=second_data.get('phone_number', ''),
                            postal_code=second_data.get('postal_code', ''),
                            round_lot=second_data.get('round_lot', None),
                            share_class_shares_outstanding=second_data.get('share_class_shares_outstanding', None),
                            sic_code=second_data.get('sic_code', ''),
                            sic_description=second_data.get('sic_description', ''),
                            state=second_data.get('state', ''),
                            ticker_root=second_data.get('ticker_root', ''),
                            total_employees=second_data.get('total_employees', None),
                            weighted_shares_outstanding=second_data.get('weighted_shares_outstanding', None),
                        )
                    return render(request, 'asset_search.html', context)
                else:
                    # If the response from the first API is not successful, display an error message
                    error_message = f"Error: {data['error']}"
                    return render(request, 'asset_search.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                # Catch any exception and display an error message
                error_message = f"Error: {e}"
                return render(request, 'asset_search.html', {'form': form, 'error_message': error_message})
        else:
            # If the form is not valid, display an error message
            error_message = "Invalid form input."
            return render(request, 'asset_search.html', {'form': form, 'error_message': error_message})
    else:
        # If the request method is not GET, return an error
        return HttpResponse({'error': 'Only GET requests are allowed for this endpoint.'})
    
    #return HttpResponse("Hello! This is a response because you exceeded the limit of free queries!")

class AssetListView(APIView):
    def get(self, request):
        form = AssetSearchForm(request.GET)  # Get search parameters from the GET request
        if form.is_valid():
            # Get form parameters
            ticker = form.cleaned_data.get('ticker')
            type = form.cleaned_data.get('type')
            
            # Filter assets according to parameters
            assets = Asset.objects.filter(
                ticker=ticker,
                type=type,
            )
        else:
            assets = Asset.objects.all()  # If the form is not valid, get all assets

        data = []
        try:
            with RESTClient("JwJqJ4gpGp18ZSma2tlYR3D4jVVy1vLz") as client:
                for asset in assets:
                    resp = client.stocks_equities_aggregates(asset.symbol, 1, "minute", _from="2022-01-01", to="2023-01-01")
                    if resp.ok:
                        data.append({
                            "name": asset.name,
                            "symbol": asset.symbol,
                            "type": asset.type,
                            "price": asset.price,
                            "last_updated": asset.last_updated,
                            "polygon_data": resp.results
                        })
                    else:
                        data.append({
                            "name": asset.name,
                            "symbol": asset.symbol,
                            "type": asset.type,
                            "price": asset.price,
                            "last_updated": asset.last_updated,
                            "polygon_data": None
                        })
        except Exception as e:
            # Catch any exception and print it for debugging
            print("Error:", e)
            data = {"error": str(e)}
        return Response(data)

class AssetSearchAPI(APIView):
    def get(self, request):
        # Get the search parameters from the GET request       # Get the search parameters from the GET request
        ticker = request.query_params.get('ticker')
        type = request.query_params.get('type')
        market = request.query_params.get('market')
        primary_exchange = request.query_params.get('primary_exchange')

        # Filter assets based on search parameters
        assets = Asset.objects.all()

        
        if ticker:
            assets = assets.filter(ticker__ticker=ticker)
        if type:
            assets = assets.filter(type__icontains=type)
        if market:
            assets = assets.filter(market__icontains=market)
        if primary_exchange:
            assets = assets.filter(primary_exchange__icontains=primary_exchange)

        # Serialize the results
        serializer = AssetSerializer(assets, many=True)

        # Return the response
        return Response(serializer.data, status=status.HTTP_200_OK)
