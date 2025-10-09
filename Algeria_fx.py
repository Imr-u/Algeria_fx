#!/usr/bin/env python
# coding: utf-8

# In[36]:


import requests
import pandas as pd
from bs4 import BeautifulSoup 
import datetime
import os
import urllib3

urllib3.disable_warnings()


# In[37]:


# API endpoint (replace with the exact URL you found)
URL = "https://www.bank-of-algeria.dz/taux-de-change-journalier/"

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
response = requests.get(URL, headers=Headers, verify=False)
soup = BeautifulSoup(response.content , "html.parser")
div = soup.find("div", class_= "elementor-element elementor-element-730fc1b elementor-widget elementor-widget-shortcode" )
table = div.find("table")
scrape_time = datetime.date.today()

latest_date = table.find("thead").find_all("th")[1].get_text(strip=True)  # skip first blank


# Extract rows
rows = []
for tr in table.find("tbody").find_all("tr"):
    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
    currency = cells[0]
    rate = cells[1]  # assume the rate is in the first column after currency
    rows.append({
        "Date": latest_date,
        "Currency": currency,
        "Rate": float(rate),
        "Scrape time": scrape_time
    })

# Create DataFrame
df = pd.DataFrame(rows)

# Save to Parquet
file_path = "Algeria_fx.csv"
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    df = pd.concat([existing_df, df]).drop_duplicates(subset=["Scrape time", "Currency"], keep="last")

df.to_csv(file_path, index=False, encoding="utf-8")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[25]:






# In[ ]:




