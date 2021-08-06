#-*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from _logFile import program_log

def _myOptions(option):
    option.add_argument("--no-sandbox");
    option.add_argument("--disable-dev-shm-usage");
    option.add_argument("--aggressive-cache-discard");
    option.add_argument("--disable-cache");
    option.add_argument("--disable-application-cache");
    option.add_argument("--disable-offline-load-stale-cache");
    option.add_argument("--disk-cache-size=0");
    option.add_argument("--headless");
    option.add_argument("--disable-gpu");
    option.add_argument("--dns-prefetch-disable");
    option.add_argument("--no-proxy-server");
    option.add_argument("--log-level=3");
    option.add_argument("--silent");
    option.add_argument("--disable-browser-side-navigation");
    return option

def _myChromeDriver():
    try:
        option = webdriver.ChromeOptions()
        options = _myOptions(option)
        #driver = webdriver.Chrome(chrome_driver_path, options=option)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        driver.set_page_load_timeout(10)
        return driver
    except:
        program_log('[ERROR!][_driver] Cannot load ChromeDriver')

def _myFirefoxDriver():
    try:
        option = webdriver.FirefoxOptions()
        options = _myOptions(option)
        #driver = webdriver.Firefox(executable_path=firefox_driver_path, options=option)
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=option)
        driver.set_page_load_timeout(10)
        return driver
    except:
        program_log('[ERROR!][_driver] Cannot load FirefoxDriver')