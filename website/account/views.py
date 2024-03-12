import requests
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import BitGetAPIForm, ByBitAPIForm
import time
import hashlib
import hmac
import base64
from .utilities import generate_signature
from .models import BitGetAPI, BybitAPI

# Create your views here.


@login_required
def profile(request):
    user = request.user
    bybit_connected = False
    bitget_connected = False

    bitget_api_info = BitGetAPI.objects.filter(user=request.user)
    bybit_api_info = BybitAPI.objects.filter(user=request.user)

    if bitget_api_info:
        bitget_connected = True
    
    if bybit_api_info:
        bybit_connected = True

    context = {
        'user': user,
        'bitget_connected': bitget_connected,
        'bybit_connected': bybit_connected,
    }
    return render(request, 'profile.html', context)


def bitget_access(request):
    if request.method == 'POST':
        form = BitGetAPIForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = BitGetAPIForm()
    return render(request, 'access.html', {'bitget_form': form})


def bybit_access(request):
    if request.method == 'POST':
        form = ByBitAPIForm(request.POST)
        if form.is_valid():
            api = form.save(commit=False)
            api.user = request.user
            api.api_key = form.cleaned_data['access_key']
            api.save()
            return redirect('all_data')
    else:
        form = ByBitAPIForm()
    return render(request, 'access.html', {'bybit_form': form})


def delete_bitget_api(request):
    api_info = BitGetAPI.objects.filter(user=request.user)
    api_info.delete()
    return redirect('profile')


def delete_bybit_api(request):
    api_info = BybitAPI.objects.filter(user=request.user)
    api_info.delete()
    return redirect('profile')


def bitget(request):
    try:
        api_info = BitGetAPI.objects.filter(user=request.user)
        timestamp = str(int(time.time_ns() / 1000000))
        user = request.user
        context = {}

        for api in api_info:
            access_key = api.api_key
            access_passphrase = api.access_passphrase
            secret_key = api.secret_key
        
        api_endpoints = {
            'account': '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt',
            'personal_info': '/api/v2/spot/account/info',
            'account_assets': '/api/v2/spot/account/assets?assetType=all',
        }

        headers = {
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-KEY': access_key,
            'ACCESS-PASSPHRASE': access_passphrase,
        }

        for endpoint_name, endpoint_path in api_endpoints.items():
            message = timestamp + 'GET' + endpoint_path
            signature = generate_signature(secret_key, message)
            headers['ACCESS-SIGN'] = signature
            response = requests.get('https://api.bitget.com' + endpoint_path, headers=headers)
            context[endpoint_name] = response.json()
        
            
        coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
        context['coins'] = coin_response.json()

        context['user'] = user

        return render(request, 'sites/bitget.html', context)
    except:
        return render(request, 'sites/bitget.html')






















def get_big_data(request):
    if request.method == 'POST':
        form = BitGetAPIForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            access_passphrase = form.cleaned_data['access_passphrase']
            secret_key = form.cleaned_data['secret_key']
            timestamp = str(int(time.time_ns() / 1000000))


            # API request URI
            account_endpoint = '/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt'
            personal_info_endpoint = '/api/v2/spot/account/info'
            account_assets = '/api/v2/spot/account/assets?assetType=all'


            # Sigmature Message
            account_message = timestamp + 'GET' + account_endpoint + ''
            personal_info_message = timestamp + 'GET' + personal_info_endpoint + ''
            account_assets_message = timestamp + 'GET' + account_assets + ''


            # Signature Encode
            account_signature = hmac.new(secret_key.encode(), account_message.encode(), hashlib.sha256).digest()
            info_signature = hmac.new(secret_key.encode(), personal_info_message.encode(), hashlib.sha256).digest()
            assets_signature = hmac.new(secret_key.encode(), account_assets_message.encode(), hashlib.sha256).digest()


            # Signature Decode
            account_signature_b64 = base64.b64encode(account_signature).decode()
            info_signature_b64 = base64.b64encode(info_signature).decode()
            assets_signature_b64 = base64.b64encode(assets_signature).decode()


            # API Headers
            personal_info_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': info_signature_b64,
            }
            account_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': account_signature_b64,
            }
            assets_headers = {
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-KEY': access_key,
                'ACCESS-PASSPHRASE': access_passphrase,
                'ACCESS-SIGN': assets_signature_b64,
            }


            # API Requests
            personal_info = requests.get('https://api.bitget.com/api/v2/spot/account/info', headers=personal_info_headers)
            account_response = requests.get('https://api.bitget.com/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt', headers=account_headers)
            coin_response  = requests.get('https://api.bitget.com/api/v2/spot/market/tickers')
            assets_response  = requests.get('https://api.bitget.com/api/v2/spot/account/assets?assetType=all', headers=assets_headers)


            info = account_response.json()
            coin = coin_response.json()
            user = request.user
            account = personal_info.json()
            assets = assets_response.json()
            context = {
                    'info': info,
                    'coins': coin,
                    'user': user,
                    'account': account,
                    'assets': assets
                }
            return render(request, 'home.html', context)
    else:
        form = BitGetAPIForm()
    return render(request, 'access.html', {'bitget_form': form})
            
