# crypto_charts/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
import requests

def fetch_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': '100', 'page': '1'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_crypto_chart_data(crypto_id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {'vs_currency': 'usd', 'days': days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'labels': [item[0] for item in data.get('prices', [])],
            'prices': [item[1] for item in data.get('prices', [])],
            'volumes': [item[1] for item in data.get('total_volumes', [])]
        }
    return {}

def crypto_list(request):
    data = fetch_crypto_data()
    if data is None:
        data = []  # Handle error case
    paginator = Paginator(data, 25)  # Show 25 cryptocurrencies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'crypto/crypto_list.html', {'page_obj': page_obj})

def crypto_chart_data(request, crypto_id, time_frame):
    time_frame_mapping = {
        '1m': '1',
        '5m': '1',
        '15m': '1',
        '1h': '1',
        '4h': '1',
        '12h': '1',
        '1d': '1',
        '7d': '7',
        '30d': '30',
        '90d': '90',
        '365d': '365'
    }
    days = time_frame_mapping.get(time_frame, '30')
    data = fetch_crypto_chart_data(crypto_id, days)
    return JsonResponse(data)
