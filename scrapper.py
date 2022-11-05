import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time 
import re

#Creating Movie Dataframe
df = pd.DataFrame()

def add_data(meta_data, title, reviews, rate):
    global df
    meta_text = meta_data[0].text
    meta_text = re.sub(r'Aspect Ratio: Scope \([0-9]*\.[0-9]+:1\)\n',"",meta_text)
    meta_text = re.sub(r'Aspect Ratio: Flat \([0-9]*\.[0-9]+:1\)\n',"",meta_text)
    meta_text = re.sub(r'Aspect Ratio: Academy \([0-9]*\.[0-9]+:1\)\n',"",meta_text)
    meta_text = re.sub(r'Aspect Ratio: Scope \([0-9]*\.[0-9]+:1\)',"",meta_text)
    meta_text = re.sub(r'Aspect Ratio: Flat \([0-9]*\.[0-9]+:1\)',"",meta_text)
    my_dict = dict(item.split(':') for item in meta_text.splitlines())
    my_dict["Tile"] = title
    my_dict["Rate"] = rate
    my_dict["Reviews"] = reviews
    
    #Append dictionary to dataframe
    df = df.append(my_dict, ignore_index=True, sort=False)

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver')
driver.get("https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=5")

#Scrapping Data 
n = int(input("Enter the number of movies to be scrapped: "))
for i in range(n):
    title = driver.find_elements(By.XPATH,"//span[@data-qa='discovery-media-list-item-title']")[i].text
    rate=driver.find_elements(By.XPATH,"//score-pairs")[0].text
    rate=re.sub(r'\n',",",rate)
    driver.find_elements(By.XPATH, "//span[@data-qa='discovery-media-list-item-title']")[i].click()
    time.sleep(3)
    meta_data = driver.find_elements(By.XPATH,"//ul[@class='content-meta info']")
    reviews = driver.find_elements(By.XPATH,"//div[@class='reviews-wrap']")[0].text
    add_data(meta_data, title, reviews, rate)
    print("Scrapped Movie: "+ str(i))
    driver.back()
    time.sleep(3)

#Convert DataFrame to CSV file.
df.to_csv('filename.csv')





