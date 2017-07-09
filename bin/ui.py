#!/usr/bin/env python

import numpy as np
import scipy
from selenium import webdriver
from selenium.webdriver.commonkeys import Keys
url = 'www.wallstreetsurvivor.com'

class UI(object):

    def __init__():
        self.driver = webdriver.Firefox()

    def navigate_to(url):
        self.driver.get(url)

if __name__ == 'main':
    ui = UI()
    ui.navigate_to(url)
