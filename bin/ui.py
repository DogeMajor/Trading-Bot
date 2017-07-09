#!/usr/bin/env python


import numpy as np
import scipy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import user_name, password
wall_str_url = 'https://www.wallstreetsurvivor.com/login'
import tensorflow as tf
print('test0!')


class UI(object):
    def __init__(self):
        print('test!')
        self.driver = webdriver.Firefox()

    def login(self, url):
        self.driver.get(url)
        elem = self.driver.find_element_by_id('LoginModel_User_Name').click()





#if __name__=='main':

#print(tf.__dict__)
ui = UI()
ui.login(wall_str_url)
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
