import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import time
import random
from selenium.common.exceptions import NoSuchElementException
import  pandas as pd


def get_phone(url=""):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1100,1000")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    time.sleep(2)

    elem=driver.find_element(By.CLASS_NAME,"phone-orange-btn")
    if elem==None:
        return None
    
    elem.click()
    time.sleep(2)
    WebDriverWait(driver, 2).until(ec.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
    time.sleep(2)
    driver.switch_to.default_content()
    WebDriverWait(driver, 2).until(ec.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title~='recaptcha']")))
    if len(driver.find_elements(By.CSS_SELECTOR,"#rc-imageselect > div.rc-imageselect-payload > div.rc-imageselect-instructions > div.rc-imageselect-desc-wrapper > div > strong"))>0:
        print("solving captcha is needed ")
        input("press enter when solved")
    driver.switch_to.default_content()
    time.sleep(2)
    if elem.text.strip()=="הסתר מספרים":
        return [phone_elem.text for phone_elem in driver.find_elements(By.CLASS_NAME,"phone-item")]

    return (elem.text,)
        


def get_data_from_rec(row):

    new_row=row
    phone=get_phone(row["link"])
    print(phone)
    if phone==None:
       return False
    if len(phone)==1:
        new_row["phone1"]=phone[0]
        new_row["phone2"]=""
    else:
        new_row["phone1"]=phone[0]
        new_row["phone2"]=phone[1]
    new_row=new_row.reindex(["name","address","link","phone1","phone2"])
    outpt_path = "new_data.csv"
    new_row=new_row.to_frame().T
    new_row.to_csv("%s" % outpt_path, mode="a", header=not os.path.exists("%s" % outpt_path),encoding = 'utf-8-sig',index=False)



df=pd.read_csv("out.csv")
last_index=pd.read_csv("new_data.csv").index[-1]
print(last_index)
nedded_df=df.iloc[last_index:last_index+10]
for index, row in nedded_df.iterrows():

    get_data_from_rec(row)

