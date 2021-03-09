from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

web_url = 'https://finviz.com/quote.ashx?t='
companies = ['AMZN', 'AMD','FB']

news_tables = {}

for company in companies:
    url = web_url + company

    req = Request(url=url, headers={'user-agent':'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'html')
    news_table = html.find(id='news-table')
    news_tables[company] = news_table
    break

a