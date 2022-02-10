from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import  StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
import pandas as pd
from datetime import date

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)

driver.get('https://enquiry.indianrail.gov.in/mntes/')
parent_window = driver.current_window_handle
driver.implicitly_wait(5)
#train no
train_no = '12631'
train_num = driver.find_element(By.ID, 'trainNo')
train_num.send_keys(train_no)
#Station
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jStation"]/option[2]')))
Select(driver.find_element(By.ID, 'jStation')).select_by_index('1')
#Day
prev_day = driver.find_element(By.ID, "jYesterday")
try:
    prev_day.click()
except StaleElementReferenceException as e:
    prev_day = driver.find_element(By.ID, "jYesterday").click()
#RunningStatus
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/table[2]/tbody/tr/td[1]/input[1]').click()
#Switch Window
windows = driver.window_handles
for sub_window in windows:
    if sub_window != parent_window:
        driver.switch_to.window(sub_window)

div_count = len(driver.find_elements(By.XPATH,'html/body/div/div/div/div/div/div/div'))
base = 'html/body/div/div/div/div/div/div/div[{}]/div[{}]'
data = []
for x in range(3, div_count + 1):
    row = []
    for y in range(1, 3):
        if y == 1:
            for  i in range(1, 3):
                row += [driver.find_element(By.XPATH, base.format(x,y) + '/span[{}]'.format(i)).text.strip()]
        else:
            for a in range(1,3):
                if a == 1:
                    row += [driver.find_element(By.XPATH, base.format(x,y) + '/div[{}]/span'.format(a)).text.replace('\n', ' ')]
                else:
                    for b in range(1, 3):
                        row += [driver.find_element(By.XPATH, base.format(x,y) + '/div[{}]/span[{}]'.format(a,b)).text.strip()]
                    # print(row)
    data += [row]
pd.DataFrame(
    data, columns= ["Scheduled Arrival" ,"Actual Arrival", "Station" ,"Scheduled Departure", "Actual Departure"]
    ).to_csv("{}.csv".format(train_no + '-' + '2022-02-09' + '-' + 'runningStatus' ), index = False)

# def scrape_running_status():
#     driver.get('https://enquiry.indianrail.gov.in/mntes/')
#     parent_window = driver.current_window_handle
#     driver.implicitly_wait(5)
#     #train no
#     train_no = '12631'
#     train_num = driver.find_element(By.ID, 'trainNo')
#     train_num.send_keys(train_no)
#     #Station
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jStation"]/option[2]')))
#     Select(driver.find_element(By.ID, 'jStation')).select_by_index('1')
#     #Day
#     prev_day = driver.find_element(By.ID, "jYesterday")
#     try:
#         prev_day.click()
#     except StaleElementReferenceException as e:
#         prev_day = driver.find_element(By.ID, "jYesterday").click()
#     #RunningStatus
#     driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/table[2]/tbody/tr/td[1]/input[1]').click()
#     #Switch Window
#     windows = driver.window_handles
#     for sub_window in windows:
#         if sub_window != parent_window:
#             driver.switch_to.window(sub_window)

#     div_count = len(driver.find_elements(By.XPATH,'html/body/div/div/div/div/div/div/div'))
#     base = 'html/body/div/div/div/div/div/div/div[{}]/div[{}]'
#     data = []
#     for x in range(3, div_count + 1):
#         row = []
#         for y in range(1, 3):
#             if y == 1:
#                 for  i in range(1, 3):
#                     row += [driver.find_element(By.XPATH, base.format(x,y) + '/span[{}]'.format(i)).text.strip()]
#             else:
#                 for a in range(1,3):
#                     if a == 1:
#                         row += [driver.find_element(By.XPATH, base.format(x,y) + '/div[{}]/span'.format(a)).text.replace('\n', ' ')]
#                     else:
#                         for b in range(1, 3):
#                             row += [driver.find_element(By.XPATH, base.format(x,y) + '/div[{}]/span[{}]'.format(a,b)).text.strip()]
#                         # print(row)
#         data += [row]
#     pd.DataFrame(
#         data, columns= ["Scheduled Arrival" ,"Actual Arrival", "Station" ,"Scheduled Departure", "Actual Departure"]
#         ).to_csv("{}.csv".format(train_no + '-' + '2022-02-04' + '-' + 'runningStatus' ), index = False)


driver.quit()