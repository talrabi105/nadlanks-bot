from selenium.webdriver.common.keys import Keys
import os
from selenium.common.exceptions import *


class Whatsapp:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('https://web.whatsapp.com/')

    def send(self, contacts, msg):
        statuses = []
        self.driver.switch_to.window(self.driver.window_handles[0])
        for contact in contacts:
            new_chat = self.find_by_xpath('//*[@data-testid="chat"]')
            new_chat.click()
            if self.get_contact(contact[1]):
                self.write(msg.replace('$', contact[0]))
                statuses.append((contact[1], 1))
            else:
                statuses.append((contact[1], 0))
        return statuses

    def get_contact(self, contact_phone_number):
        if contact_phone_number[0] == "0":
            contact_phone_number = "+972" + contact_phone_number[1:]
        new_user = self.find_by_xpath('//*[@class="_13NKt copyable-text selectable-text"]')
        new_user.send_keys(contact_phone_number)
        if self.check_results():
            user = self.find_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/span/span')
            user.click()
            return True
        else:
            back_btn = self.find_by_xpath('//*[@aria-label="Back"]')
            back_btn.click()
            return False

    def write(self, msg):
        if os.path.exists('img/image1.jpg'):
            attach_box = self.find_by_xpath('//*[@aria-label="Attach"]')
            attach_box.click()

            file_box = self.find_by_xpath('//*[@type="file"]')
            file_box.send_keys(os.getcwd() + '/img/image1.jpg')


            msg_box = self.find_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')

        else:
            msg_box = self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]")

        for one_line in msg.split("\n"):
            msg_box.send_keys(one_line)
            msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
        msg_box.send_keys(Keys.ENTER)

    def send_msg(self):
        send_msg_btn = self.driver.find_element_by_xpath('//*[@data-testid="send"]')
        send_msg_btn.click()

    def find_by_xpath(self, xpath):
        obj = None
        while obj is None:
            try:
                obj = self.driver.find_element_by_xpath(xpath)
            except WebDriverException:
                pass
        return obj

    def check_results(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML;")
        while True:
            html = self.driver.execute_script("return document.documentElement.outerHTML;")
            if 'No results found for' in html:
                return False
            elif 'Contact' in html and 'New group' not in html:
                return True
