from unicodedata import name
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from xpaths import sh_xpaths
from datetime import date
from bs4 import BeautifulSoup

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)
URL='https://www.railmitra.com/train-schedule'
trainNum = "12631"
f_name = "schedule-"+trainNum+".csv"

def getTable() :
    driver.get(URL)
    driver.find_element(By.XPATH, sh_xpaths['trainNumInput']).send_keys(trainNum,Keys.RETURN)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tables = soup.find_all('table')
    df = pd.read_html(str(tables))
    df[0].to_csv(f_name, index=False)
    driver.implicitly_wait(5)


def manipulateTable() :
    dfs = pd.read_csv(str("W:\\Coding\\reserved-trains\\"+f_name))
    dfs['STATION'] = dfs['STATION NAME'].str.upper() + ' ' + '('+ dfs['CODE'].map(str) + ')'
    del dfs['STATION NAME']
    del dfs['CODE']
    first_column = dfs.pop('STATION')
    dfs.insert(0, 'STATION', first_column)
    dfs['ARRIVAL'] = dfs['ARRIVAL'].replace(['First'],'SRC')
    dfs['ARRIVAL'] = dfs['ARRIVAL'].replace(['.'],':')
    dfs['DEPARTURE'] = dfs['DEPARTURE'].replace(['Last'],'DST')
    dfs.to_datetime('ARRIVAL')
    dfs.to_csv(f_name, index=False)


if __name__ == '__main__' :
    getTable()
    manipulateTable()
    driver.quit()
