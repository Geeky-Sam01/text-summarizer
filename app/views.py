from flask import render_template, request
from news.text_summ2 import generate_summary
import requests
from config import API_KEY
from news.news_functions import most_popular_news
from app import app


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':        
        popular_news = most_popular_news()
        return render_template('index.html', popular_news=popular_news)
    elif request.method == 'POST':
        search_topic = request.form.get('searchtopic')
        url = f'https://newsapi.org/v2/everything?q={search_topic}&apiKey={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            titles, links = [], []
            if 'articles' in json_response:
                for article in json_response['articles']:
                    title = article.get('title')
                    link = article.get('url')
                    if title and link:
                        titles.append(title)
                        links.append(link)
            return render_template('index.html', titles=titles, links=links)

# Other routes and views can stay in this file

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        if rawtext.strip() == "":
            error_message = 'Please enter some text to summarize.'
            return render_template('index.html', error_message=error_message)
        final_summary, original_text, len_original, len_summary = generate_summary(rawtext)
        return render_template('summary.html', final_summary=final_summary, original_text=original_text, len_original=len_original, len_summary=len_summary)

@app.route('/about')
def about():
    return render_template('about.html')
