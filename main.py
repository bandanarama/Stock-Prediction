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

parsed_data = []

for company, news_table in news_tables.items():
    for row in news_table.findAll('tr'):

        title = row.a.get_text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([company, date, time, title])
        
print(parsed_data)

# amazon_data = news_tables['AMZN']
# amazon_rows = amazon_data.findAll('tr')

# for index, row in enumerate(amazon_rows):
#     title = row.a.text
#     timestamp = row.td.text
#     print(timestamp + " " + title)