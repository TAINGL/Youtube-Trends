import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import random
import pandas as pd
import datetime

def _getToday():
    return datetime.date.today().strftime("%Y%m%d")

def scrapping():
    browser = webdriver.Chrome()

    # URL needed
    browser.get("https://www.noxinfluencer.com/youtube-channel-rank/top-1000-all-all-youtuber-sorted-by-subs-weekly")

    # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.
    # It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    # Now that the page is fully scrolled, grab the source code.
    source_data = browser.page_source

    # Throw your source into BeautifulSoup and start parsing!
    soup = bs(source_data, 'html.parser')

    tables = soup.find_all("table")

    # Get rows and columns 
    table = tables[0]
    tab_data = [[cell.text for cell in row.find_all(["th","td"])]
                            for row in table.find_all("tr")]

    # convert tab_data list to dataframe
    df = pd.DataFrame(tab_data)
    
    # Replace column names with second row
    df.columns = df.iloc[0,:]
    df.drop(index=0,inplace=True)

    # Remove extra spaces from column names
    df.columns = df.columns.str.replace(' ', '')

    # Save to csv file
    filename = "%s_%s.%s" % ("data/youtuber_list", _getToday() ,".csv")
    df.to_csv(filename)

    youtuber_name = df['ChannelInfo']

    # Convert column to list
    list_of_youtubers = youtuber_name.to_list()

    # Remove spaces from list_of_youtubers
    youtubers = []
    for i in list_of_youtubers:
        j = i.strip()
        #Remove empty string
        if (j != ''):
            youtubers.append(j)

    # Select Random 250 youtuber names
    sampling = random.choices(youtubers, k=250)

    return sampling
    

sample = scrapping()
print(sample)