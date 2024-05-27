# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 13:10:20 2023

@author: tanuj
"""


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

multi_index = pd.MultiIndex.from_tuples([
    ('S No', 'S No'),
    ('Vehicle Class', 'Vehicle Class'),
    ('Month Wise', 'JAN'),
    ('Month Wise', 'FEB'),
    ('Month Wise', 'MAR'),
    ('Month Wise', 'APR'),
    ('Month Wise', 'MAY'),
    ('Month Wise', 'JUN'),
    ('Month Wise', 'JUL'),
    ('Month Wise', 'AUG'),
    ('Month Wise', 'SEP'),
    ('Month Wise', 'OCT'),
    ('Month Wise', 'NOV'),
    ('Month Wise', 'DEC'),
    ('TOTAL', 'TOTAL'),
    ('rto', ''),
    ('year', ''),
    ('state', '')
])

empty_df = pd.DataFrame(columns=multi_index)
print(empty_df)


driver = webdriver.Firefox()
driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")
time.sleep(2)

x_axis =  driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div[3]').click()
time.sleep(1)
x_axis_element =  driver.find_element(By.XPATH, '//*[@id="xaxisVar_6"]').click()
time.sleep(1)

year = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[3]/span').click()
time.sleep(1)
year_element= driver.find_element(By.XPATH, '/html/body/div[8]/div/ul/li[2]')
click_year = year_element.click()
time.sleep(1)  
label_element = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/label')
time.sleep(1)
label_value = label_element.text
print(label_value) 


# Define the range for states
for i in range(32, 33):
    try:
        state_dropdown = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/div[3]').click()
        time.sleep(2)

        li_xpath = f"/html/body/div[3]/div/ul/li[{i}]"
        state_select = driver.find_element(By.XPATH, li_xpath).click()
        time.sleep(2)
        selected_state = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[3]/div/label')
        state_value = selected_state.text
        print(state_value)


        time.sleep(1)
        div_elements = driver.find_elements(By.XPATH, "/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[2]/select")

        total_option_count = 0
        time.sleep(1)
        for div in div_elements:
            option_tags = div.find_elements(By.TAG_NAME, "option")
            total_option_count += len(option_tags)

        print("Total number of <option> tags within <div> elements:", total_option_count)

        for j in range(1, total_option_count):
            rto_dropdown = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/div[3]/span').click()
            print(j)
            time.sleep(2)

            path = f'//*[@id="selectedRto_{j}"]'
            li_xpath2 = driver.find_element(By.XPATH, path).click()
            time.sleep(2)
            selected_rto = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[2]/div[4]/div/label')
            rto_value = selected_rto.text
            print(rto_value)
            time.sleep(1)

            # Refresh
            refresh = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[1]/div[3]/div[3]/div/button').click()
            time.sleep(4)

            table = driver.find_element(By.XPATH ,'/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[3]/table')
            time.sleep(1)
            span_element = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[5]/span')  # Replace with your class name
            a_elements = span_element.find_elements(By.TAG_NAME,'a')
            a_count = len(a_elements)
            print("pagination: ", a_count)
            
            # Read the table data into a Pandas DataFrame
            df = pd.read_html(table.get_attribute('outerHTML'))[0]
            df['rto'] = ""
            df['year'] = ""
            
            df['state'] = ""
            df['pagination']= ""
            df['rto'] = rto_value
            df['year'] = int(label_value)
            df['state'] = state_value
            df['pagination']= a_count
            
            # Filter rows where 'Vehicle Class' matches any of the specified values
            row_to_append = df[
                (df['Vehicle Class']['Vehicle Class'] == 'AGRICULTURAL TRACTOR') |
                (df['Vehicle Class']['Vehicle Class'] == 'HARVESTER') |
                (df['Vehicle Class']['Vehicle Class'] == 'TRACTOR (COMMERCIAL)') |
                (df['Vehicle Class']['Vehicle Class'] == 'TRACTOR-TROLLEY(COMMERCIAL)')
            ]

            empty_df = empty_df.append(row_to_append, ignore_index=True)
            time.sleep(1)
            
            if a_count == 2:
                next_page= driver.find_element(By.XPATH, '/html/body/form/div[2]/div/div/div[3]/div/div[2]/div/div/div[1]/div[5]/a[3]/span').click()
                df_2 = pd.read_html(table.get_attribute('outerHTML'))[0]
                
                df_2['rto'] = ""
                df_2['year'] = ""
                df_2['state'] = ""
                df_2['pagination']= ""
                
                df_2['rto'] = rto_value
                df_2['year'] = int(label_value)
                df_2['state'] = state_value
                df_2['pagination']= a_count
                
                row_to_append_2 = df_2[
                    (df_2['Vehicle Class']['Vehicle Class'] == 'AGRICULTURAL TRACTOR') |
                    (df_2['Vehicle Class']['Vehicle Class'] == 'HARVESTER') |
                    (df_2['Vehicle Class']['Vehicle Class'] == 'TRACTOR (COMMERCIAL)') |
                    (df_2['Vehicle Class']['Vehicle Class'] == 'TRACTOR-TROLLEY(COMMERCIAL)')
                ]
                empty_df = empty_df.append(row_to_append_2, ignore_index=True)
                

    except NoSuchElementException as e:
        print(f"Element not found: {str(e)}")
        # Handle the exception as needed

driver.quit()
empty_df.to_excel("sample1.xlsx")
empty_df
