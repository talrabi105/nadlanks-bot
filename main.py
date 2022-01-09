import time
from selenium.common.exceptions import *
from selenium import webdriver
from whatsapp import Whatsapp
from googleSheets import GoogleSheets
from messenger import Messenger
from gui import start_msg
import os


def get_constants():
    with open('constants.txt', 'r') as f:
        data = f.read()
    return {con[:con.find(':')]: con[con.find(':') + 1:] for con in data.split('\n')}


CONSTANTS = get_constants()


def start_window():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=' + CONSTANTS['DEFAULTPATHFORCHROME'])
    options.add_argument('--profile-dictionary=Default')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '\chromedriver.exe', options=options)
    driver.maximize_window()
    wa = Whatsapp(driver)
    m = Messenger(driver)
    driver.minimize_window()
    return driver, wa, m


def mainloop():
    print(CONSTANTS)
    gs = GoogleSheets()
    driver, wa, m = start_window()
    while True:
        gc = gs.check()
        time.sleep(1)
        if gc == 1:
            m.update_first_msg(gs.get_first_msg())
            try:
                driver.title
            except WebDriverException:
                driver, wa, m = start_window()
            gs.read()
            start_msg(gs.get_names_list(), gs.get_msg(), gs.get_current_place())
            if os.environ['nadlanks-bot'] == '1':
                msg = gs.get_msg()
                try:
                    driver.maximize_window()
                    wa_statuses = wa.send(gs.get_wa_list(), msg)
                    for i in wa_statuses:
                        gs.upload_status(i[0], i[1])
                    m_statuses = m.send(gs.get_m_list(), msg)
                    for i in m_statuses:
                        gs.upload_status(i[0],i[1])
                    driver.minimize_window()
                except WebDriverException:
                    return True
            else:
                for i in gs.get_wa_list()+gs.get_m_list():
                    gs.upload_status(i[1], 0)
            gs.end()

        elif gc == 2:
            driver.close()


if __name__ == '__main__':
    mainloop()
