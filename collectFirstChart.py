from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from xpaths import xpaths
from datetime import date

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)


def journeyDetails(trainNum, stationName, jDate) -> None:
    driver.find_element(By.XPATH, xpaths['trainNoInput']).send_keys(trainNum, Keys.RETURN)
    station = driver.find_element(By.XPATH, xpaths['boardingStationInput'])
    station.send_keys(stationName)
    station.send_keys(Keys.RETURN)
    select_date(jDate)
    driver.find_element(By.XPATH, xpaths['trainChartButton']).click()
    
def select_date(journey_date) -> None:
    journey_day = journey_date[8:10]
    if journey_day[0] == '0':
        journey_day = journey_day[1]
    driver.find_element(By.XPATH, xpaths['journeyDateInput']).click()
    dates = driver.find_elements(By.XPATH, xpaths['dateButtons'])
    for d_elem in dates:
        if d_elem.text == journey_day and d_elem.get_attribute('tabindex') == '0':
            d_elem.click()
            break

def getHeaders() -> list:
    headers = []
    for i in range(1, 6):
        th = driver.find_element(By.XPATH, xpaths['headersData'].format(i))
        headers.append(th.text)
    return headers

def pagesAndRows() -> tuple:
    n = int(driver.find_element(By.XPATH, xpaths['pageDetails']).text.split(" ")[-1])
    if (n / 10 <= 1):
        totalPages = 1
        lastPageRows = n
    else:
        if n / 10 > n // 10:
            totalPages = (n // 10) + 1
            lastPageRows = n % 10
        else:
            totalPages = n // 10
            lastPageRows = 10
    return (totalPages, lastPageRows)
        
def collectPage(noOfRows) -> list:
    PageData = []
    for j in range(2, noOfRows + 2):
        row = []
        for k in range(1,6):
            td = driver.find_element(By.XPATH, xpaths['tableData'].format(j, k))
            row.append(td.text)
        PageData.append(row)
    return PageData

def collectCoachData(coachName) -> None:
    driver.find_element(By.XPATH, xpaths['coachSortButton']).click()
    # driver.find_element(By.XPATH, xpaths['noOfRowsOptionDiv']).click()
    # driver.find_element(By.XPATH, xpaths['select50Rows']).click()
    totalPages, lastPageRows = pagesAndRows()
    print((totalPages, lastPageRows, coachName))
    coachData = []
    currentPage = 1
    for i in range(totalPages):
        if (currentPage == totalPages):
            coachData += collectPage(lastPageRows)
        else:
            coachData += collectPage(10)    
            nextPage = driver.find_element(By.XPATH, xpaths['nextPageButton'])
            driver.execute_script('arguments[0].click()', nextPage)
        currentPage += 1
    pd.DataFrame(coachData, columns= getHeaders()).to_csv("{}.csv".format(coachName), index = False)

def collectVacantBerthDetails() -> None:
    coach_names_elements = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/table/thead/tr[2]/th')
    coaches = []
    for coach_name_WebElem in coach_names_elements:
        coaches.append(coach_name_WebElem.text)
    print(coaches)
    
    vacany_details = [str(date.today())]
    for i in range(len(coaches)):
        coach_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/table/tbody/tr/td[{}]'.format(i + 1))
        vacany_details.append(coach_button.text)
        coach_button.click()
        collectCoachData(coaches[i])
        driver.find_element(By.XPATH, xpaths['backButton']).click()
    print(vacany_details)
    # pd.DataFrame([vacany_details]).to_csv('12632fcv.csv', mode = 'a', index= False, header=False)


def main():
    driver.get("https://www.irctc.co.in/online-charts/")
    driver.implicitly_wait(5)
    journeyDetails("12632", "TIRUNELVELI (TEN)", str(date.today()))
    collectVacantBerthDetails()
    driver.quit()

if __name__ == '__main__':
    main()
