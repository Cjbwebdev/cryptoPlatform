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
        '365d': '365',
        'all': 'max',
        
    }
    days = time_frame_mapping.get(time_frame, '30')
    data = fetch_crypto_chart_data(crypto_id, days)
    return JsonResponse(data)

def fetch_full_crypto_history(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {'vs_currency': 'usd', 'days': 'max'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'labels': [item[0] for item in data.get('prices', [])],
            'prices': [item[1] for item in data.get('prices', [])],
            'volumes': [item[1] for item in data.get('total_volumes', [])]
        }
    else:
        return {"error": "Failed to fetch full historical data"}

def fetch_crypto_news(crypto_name):
    """ Fetch top 5 news articles related to the cryptocurrency using NewsData.io API. """
    api_key = 'pub_5202571ec2f7a093cbd2304c4c8981bf7f1a2'  # Use your actual API key here
    url = f'https://newsdata.io/api/1/news'
    params = {
        'apikey': api_key,
        'q': crypto_name,
        'language': 'en',
        'category': 'business',
        'country': 'us',
        'page': 1,
        'page_size': 5
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = [
            {
                'title': article['title'],
                'description': article['description'],
                'url': article['link'],
                'image': article.get('image_url', '')  # Default to empty string if no image
            } for article in data.get('results', [])
        ]
        return articles
    else:
        return []
    
def article_detail(request, article_id):
    # Assuming you have a method to get the article details by its ID
    # For now, we'll simulate this by using the API key and fetching details from the API
    api_key = 'pub_5202571ec2f7a093cbd2304c4c8981bf7f1a2'
    url = f'https://newsdata.io/api/1/news?apikey={api_key}&q=crypto'
    
    response = requests.get(url)
    data = response.json()
    
    # Find the article by ID in the fetched data
    article = next((item for item in data['results'] if item['article_id'] == article_id), None)
    
    if not article:
        return render(request, '404.html', status=404)  # Handle article not found

    return render(request, 'article_detail.html', {'article': article})