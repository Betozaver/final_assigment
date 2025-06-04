import yfinance as yf
import pandas as pd
pd.set_option('display.max_columns', 10)
import json
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# TESLA TICKER
tsla = yf.Ticker("TSLA")
tsla_data = tsla.history(period='max')
tsla_data.reset_index(inplace = True)
print(tsla_data.head()[:])

#question 2
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text


#parse the HTML content
soup = BeautifulSoup(html_data, 'html.parser')


#print(soup.find_all('table'))

# FIND THE RELEVANT TABLE
tbls = soup.find_all('table', class_="historical_data_table table")

tsla_quart = None

for table in tbls:
    ths = table.find_all('th')
    for th in ths:
        if th.get_text().startswith('Tesla Quarterly Revenue'):
            #print(' WE FOUND THE TABLE YAAY')
            tsla_quart = table
            break

    if tsla_quart:
        break


#print(tsla_quart)
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
# EXTRCT DATA FROM THE COLUMNS and add it to dataframe
rows = tsla_quart.find_all('td')
new_row = {'Date': None, "Revenue": None}
for row in rows:
    if '$' in row.get_text():
        #print(f'REV:{row.get_text()}')
        new_row['Revenue'] = float(row.get_text()[1:].replace(",",""))

    else:
        if not row.get_text():
            new_row = {'Date': None, "Revenue": None}
        else:
            #print(f'DAT:{row.get_text()}')
            new_row['Date'] = row.get_text()
    if new_row['Date'] and new_row['Revenue']:
        tesla_revenue.loc[len(tesla_revenue)] = new_row
        new_row = {'Date': None, "Revenue": None}
    #Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe
# named tesla_revenue. The dataframe should have columns Date and Revenue.

#tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
print(tesla_revenue.tail(5))
make_graph(tsla_data, tesla_revenue, "TESLA")


#GME alll the same
# GAMESTOP TICKER
gme = yf.Ticker("GME")
gme_data = gme.history(period='max')
gme_data.reset_index(inplace = True)
print(gme_data.head(5))

#question 2
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text


#parse the HTML content
soup = BeautifulSoup(html_data, 'html.parser')


#print(soup.find_all('table'))

# FIND THE RELEVANT TABLE
tbls = soup.find_all('table', class_="historical_data_table table")

gme_quart = None

for table in tbls:
    ths = table.find_all('th')
    for th in ths:
        if th.get_text().startswith('GameStop Quarterly Revenue'):
            #print(' WE FOUND THE TABLE YAAY')
            gme_quart = table
            break

    if gme_quart:
        break

tbls = soup.find_all('table', class_="historical_data_table table")

gme_quart = None

for table in tbls:
    ths = table.find_all('th')
    for th in ths:
        if th.get_text().startswith('GameStop Quarterly Revenue'):
            #print(' WE FOUND THE TABLE YAAY')
            gme_quart = table
#print(tsla_quart)
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
# EXTRCT DATA FROM THE COLUMNS and add it to dataframe
rows = gme_quart.find_all('td')
new_row = {'Date': None, "Revenue": None}
for row in rows:
    if '$' in row.get_text():
        #print(f'REV:{row.get_text()}')
        new_row['Revenue'] = float(row.get_text()[1:].replace(",",""))

    else:
        if not row.get_text():
            new_row = {'Date': None, "Revenue": None}
        else:
            #print(f'DAT:{row.get_text()}')
            new_row['Date'] = row.get_text()
    if new_row['Date'] and new_row['Revenue']:
        gme_revenue.loc[len(gme_revenue)] = new_row
        new_row = {'Date': None, "Revenue": None}
    #Using BeautifulSoup or the read_html function extract the table with Tesla Revenue and store it into a dataframe
# named tesla_revenue. The dataframe should have columns Date and Revenue.

#tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
print(gme_revenue.tail(5))
make_graph(gme_data, gme_revenue, "GAMESTOP")

