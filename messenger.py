import os

import win32api
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *


class Messenger:
    def __init__(self, driver):
        self.driver = driver
        driver.execute_script("window.open()")
        self.first_msg = []

    def send(self, contacts, original_msg):
        statuses = []
        self.driver.switch_to.window(self.driver.window_handles[1])
        for contact in contacts:
            self.driver.get('https://www.facebook.com/messages/t/{}'.format(self.get_user_id(contact[1])))
            if self.is_first() and win32api.MessageBox(0, "האם לשלוח first_msg", "bot", 1) == 1:
                print('first')
                print(self.first_msg)
                msg_box = self.find_by_xpath('//*[@aria-label="Message"]', '//*[@aria-label="הודעה"]')
                for one_line in self.first_msg[0].replace('$', contact[0]).split("\n"):
                    msg_box.send_keys(one_line)
                    msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                msg_box.send_keys(Keys.ENTER)

                for one_line in self.first_msg[1].replace('$', contact[0]).split("\n"):
                    msg_box.send_keys(one_line)
                    msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                msg_box.send_keys(Keys.ENTER)
                statuses.append([contacts[1], 2])

            elif win32api.MessageBox(0, "האם לשלוח הודעה", "bot", 1) == 1:
                print('not first')
                if os.path.exists('img/image1.jpg'):
                    file_box = self.find_by_xpath('//*[@type="file"]')
                    file_box.send_keys('C:/users/user/desktop/b/img/image1.jpg')
                msg = original_msg.replace('$', contact[0])
                msg_box = self.find_by_xpath('//*[@aria-label="Message"]', '//*[@aria-label="הודעה"]')
                print('aaa')
                for one_line in msg.split("\n"):
                    msg_box.send_keys(one_line)
                    msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
                msg_box.send_keys(Keys.ENTER)
                print('d')
                statuses.append([contacts[1], 1])
            else:
                statuses.append([contacts[1], 1])
        return statuses

    def find_by_xpath(self, xpath):
        obj = None
        while obj is None:
            try:
                obj = self.driver.find_element_by_xpath(xpath)
            except WebDriverException:
                pass
        return obj

    def find_by_xpath(self, xpath1, xpath2):
        obj = None
        while obj is None:
            try:
                obj = self.driver.find_element_by_xpath(xpath1)
            except WebDriverException:
                try:
                    obj = self.driver.find_element_by_xpath(xpath2)
                except WebDriverException:
                    pass
        return obj

    def is_first(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML;")
        while 'aria-label="Message"' not in html and 'aria-label="הודעה"' not in html:
            html = self.driver.execute_script("return document.documentElement.outerHTML;")
        return 'mw_message_list' not in html

    def update_first_msg(self, first_msg):
        self.first_msg = first_msg

    @staticmethod
    def get_user_id(st):
        if st[-1] == '/':
            st = st[:-1]
        if '?id=' in st:
            return st.split('id=')[-1].split('&')[0]
        elif '?' in st:
            return st.split('?')[0].split('/')[-1]
        else:
            return st.split('/')[-1]
