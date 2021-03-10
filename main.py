from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as panda
import matplotlib.pyplot as plot

web_url = 'https://finviz.com/quote.ashx?t='
companies = ['AMZN', 'GOOG','FB']

news_tables = {}

for company in companies:
    url = web_url + company

    req = Request(url=url, headers={'user-agent':'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'html.parser')
    news_table = html.find(id='news-table')
    news_tables[company] = news_table
    #break

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
        
# print(parsed_data)

# amazon_data = news_tables['AMZN']
# amazon_rows = amazon_data.findAll('tr')

# for index, row in enumerate(amazon_rows):
#     title = row.a.text
#     timestamp = row.td.text
#     print(timestamp + " " + title)

data_frame = panda.DataFrame(parsed_data, columns=['company', 'date', 'time', 'title'])

vader = SentimentIntensityAnalyzer()

compound_title = lambda title: vader.polarity_scores(str(title))['compound']

data_frame['compound'] = data_frame['title'].apply(compound_title)
data_frame['date'] = panda.to_datetime(data_frame.date).dt.date

#print(data_frame.head())

plot.figure(figsize=(10,8))

mean_dataframe = data_frame.groupby(['company','date']).mean()
mean_dataframe = mean_dataframe.unstack()
mean_dataframe = mean_dataframe.xs('compound', axis = "columns").transpose()
mean_dataframe.plot(kind='bar')
#print(mean_dataframe)

plot.show()