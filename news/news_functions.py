from config import API_KEY
import requests
def most_popular_news():
    country='us'
    url=f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        news=[]
        if 'articles' in json_response:
            for article in json_response['articles']:
                title = article.get('title')
                link=article.get('url')
                if title and link:
                    news.append({'title':title,'link':link})
    return news