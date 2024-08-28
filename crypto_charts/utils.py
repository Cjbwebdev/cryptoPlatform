# utils.py
import requests

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def fetch_crypto_chart_data(crypto_id, interval, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": interval
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        labels = [item[0] for item in json_data.get('prices', [])]
        prices = [item[1] for item in json_data.get('prices', [])]
        volumes = [item[1] for item in json_data.get('total_volumes', [])]
        return {
            "labels": labels,
            "prices": prices,
            "volumes": volumes
        }
    else:
        print(f"Error fetching chart data: {response.status_code}, {response.text}")
        return {"labels": [], "prices": [], "volumes": []}
