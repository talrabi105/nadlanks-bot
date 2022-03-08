import time

import win32api
from selenium.common.exceptions import *
from selenium import webdriver

from whatsapp import Whatsapp
from googleSheets import GoogleSheets
from messenger import Messenger
from gui import start_msg
import os
from threading import Timer
from flask import Flask
CONSTANTS = get_constants()
from flask_cors import CORS


def a():
    driver = webdriver.Chrome('./chromedriver')
    return driver



def get_constants():
    with open('constants.txt', 'r') as f:
        data = f.read()
    return {con[:con.find(':')]: con[con.find(':') + 1:] for con in data.split('\n')}


CONSTANTS = get_constants()


def start_window(last_driver=None):
    if last_driver:
        last_driver.quit()
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=' + CONSTANTS['DEFAULTPATHFORCHROME'])
    options.add_argument('--profile-dictionary=Default')
    driver = webdriver.Chrome("./chromedriver", options=options)
    driver.maximize_window()
    wa = Whatsapp(driver)
    m = Messenger(driver)
    driver.minimize_window()
    return driver, wa, m

app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    run_click()
    return "works"


def run_click():
    print(CONSTANTS)
    gs = GoogleSheets()
    driver, wa, m = start_window()
    gc = gs.check()
    timeout = time.time() + 60 * 30 
    while gc!=1 or time.time()>timeout:
        gc = gs.check()
    # print("the status is",gc)
    time.sleep(1)
    if gc == 1:
        print("start gui")
        m.update_first_msg(gs.get_first_msg())
        try:
            driver.title
        except WebDriverException as e:
            print(e)
            print("has error with driver 1")
            driver, wa, m = start_window(last_driver=driver)
        finally:
            gs.read()
            start_msg(gs.get_names_list(), gs.get_msg(), gs.get_current_place())
            if os.environ['nadlanks-bot'] == '1':
                print('start send')
                msg = gs.get_msg()
                m_statuses, wa_statuses = None, None
                try:
                    driver.maximize_window()
                    print(wa_statuses)
                    wa_statuses = wa.send(gs.get_wa_list(), msg)
                    for i in wa_statuses:
                        gs.upload_status(i[0], i[1])
                        print("upload Whatsapp", i)
                    m_statuses = m.send(gs.get_m_list(), msg)
                    for i in m_statuses:
                        gs.upload_status(i[0], i[1])
                        print("upload Messenger", i)
                    driver.minimize_window()
                except WebDriverException as e:
                    print(e)
                    print("has error with driver!!!!!!!! 2")
                    if wa_statuses:
                        for i in wa_statuses:
                            gs.upload_status(i[0], 0)
                    if m_statuses:
                        for i in wa_statuses:
                            gs.upload_status(i[0], 0)
                    driver, wa, m = start_window(last_driver=driver)
                    win32api.MessageBox(0, "באג בלתי צפוי, בדקי ידנית אם ההודעות נשלחו ותתקשרי למספר 0538222921")

            else:
                for i in gs.get_wa_list() + gs.get_m_list():
                    gs.upload_status(i[1], 0)
            gs.end()


if __name__ == "__main__":

    app.run()