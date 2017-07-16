#!/usr/bin/env python

import numpy as np
import scipy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import username, password
wall_str_url = 'https://www.wallstreetsurvivor.com/login'
import tensorflow as tf
print('test0!')

class UI(object):
    def __init__(self):
        print('test!')
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.quit()
        print("Webdriver destroyed!")

    def login(self, url):
        self.driver.get(url)
        self.driver.get_screenshot_as_file('../data/login_before.png')
        self._submit_username(username)
        self._submit_password(password)
        self.driver.find_element_by_id('login_btn').click()
        #element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//section[@id='my_trade']")))
        self.driver.get_screenshot_as_file('../data/login_after.png')

    def _submit_username(self, name):
        elem = self.driver.find_element_by_xpath("//input[@id='LoginModel_UserName']")
        elem.send_keys(name)
        elem.submit()

    def _submit_password(self, pwd):
        elem = self.driver.find_element_by_xpath("//input[@id='LoginModel_Password']")
        elem.send_keys(pwd)
        elem.submit()



    def logout(self):
        self.driver.get(wall_str_url+'/logout')

#if __name__ == "main":
ui = UI()
ui.login(wall_str_url)
ui.logout()
print("The End!")
#hello = tf.constant('Hello, TensorFlow!')
#sess = tf.Session()
#print(sess.run(hello))
