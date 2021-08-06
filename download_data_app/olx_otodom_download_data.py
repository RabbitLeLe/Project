#-*- coding: utf-8 -*-
try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    from configparser import ConfigParser
    from tqdm import tqdm
    import time
    import re, os
    import sqlite3
    import json
    import sys
    sys.path.append('libraries')
    from _driver import _myFirefoxDriver
    from _logFile import program_log
    from _clear import clear_tel, clear_text
    from _setTime import settime_olx_oto
    from _dataBase import create_database
except:
    print('[!][olx_otodom] no required modules')
    time.sleep(5)

def download_data(link, downloaded_date):
    with open(link,"r", encoding='utf-8', errors='ignore') as f:
        contents = f.read()
        soup = BeautifulSoup(contents,"html.parser")

    if 'olx.pl' in link:
        print(link)
        scripts = soup.find_all("script")
        try:
            for script in scripts:
                if 'PRERENDERED_STATE' in str(script):
                    s = str(script)
                    start = "PRERENDERED_STATE__= {"
                    stop = "};"
                    metadata_script1 = s.split(start)[1].split(stop)[0]
                    metadata_script1 = '{' + metadata_script1 + '}'
                    break
                else: metadata_script1 = ''
            json1 = json.loads(metadata_script1)
        except:
            json1 = ''

        try:
            li = json1["ad"]["ad"]["params"]
        except:
            li = ''

     #ADV_ID
        try:
            ADV_ID = json1["ad"]["ad"]["id"]
        except :
            ADV_ID = ''
        print('\n01 - ADV_ID = ' + str(ADV_ID))

     #SELLER_ID
        try:
            SELLER_ID = json1["ad"]["ad"]["user"]["id"]
        except :
            SELLER_ID = ''
        print('02 - seller_id = ' + str(SELLER_ID))

     #URL
        try:
            URL = json1["ad"]["ad"]["url"]
        except :
            URL = ''
        print('03 - URL = ' + str(URL))

     #SELLER_DIR
        try:
            SELLER_DIR = ADRES_OFERTY.split('-')
            SELLER_DIR = SELLER_DIR[-1].split('.')[0]
            SELLER_DIR = SELLER_DIR[2:]
        except:
            SELLER_DIR = ''
        print('04 - seller_dir = ' + str(SELLER_DIR))

     #PRICE
        try:
            PRICE = json1["ad"]["ad"]["price"]["regularPrice"]["value"]
        except :
            PRICE = ''
        print('05 - PRICE = ' + str(PRICE))

     #CURRENCY
        try:
            CURRENCY = json1["ad"]["ad"]["price"]["regularPrice"]["currencyCode"]
        except :
            CURRENCY = ''
        print('06 - CURRENCY = ' + str(CURRENCY))

     #ADV_TITLE
        try:
            ADV_TITLE = json1["ad"]["ad"]["title"]
        except:
            ADV_TITLE = ''
        print('07 - ADV_TITLE = ' + str(ADV_TITLE))

     #DATE1
        try:
            DATE1 = soup.find('span', {'data-cy': 'ad-posted-at'}).get_text()
        except:
            DATE1 = ''
        print('08 - DATE1 = ' + str(DATE1))

     #DATE2
        try:
            DATE2 = json1["ad"]["ad"]["lastRefreshTime"][:19].replace('T',' ')
        except:
            DATE2 = ''
        print('09 - DATE2 = ' + str(DATE2))

     #CATEGORY
        try:
            CATEGORY = json1["ad"]["breadcrumbs"][-1]["href"]
            if 'nieruchomosci' in CATEGORY:
                try:
                    CATEGORY = CATEGORY.replace('/nieruchomosci/','')
                except:
                    pass
            if 'search' in CATEGORY:
                try:
                    CATEGORY = CATEGORY.split('/')
                    CATEGORY = CATEGORY[0]
                except:
                    pass
        except :
            CATEGORY = ''
        print('10 - CATEGORY = ' + str(CATEGORY))

     #LOCATION
        try:
            LOCATION = json1["ad"]["ad"]["location"]["pathName"]
        except:
            LOCATION = ''
        print('11 - LOCATION = ' + str(LOCATION))

     #REGION
        try:
            REGION = json1["ad"]["ad"]["location"]["regionName"]
        except :
            REGION = ''
        print('12 - region = ' + str(REGION))

     #SUBREGION
        try:
            SUBREGION = json1["ad"]["ad"]["location"]["cityName"]
        except:
            SUBREGION = ''
        print('13 - subregion = ' + str(SUBREGION))

     #PHONE
        PHONE = ''
        print('14 - PHONE = ' + str(PHONE))

     #USER_NAME
        try:
            USER_NAME = json1["ad"]["ad"]["user"]["name"]
        except:
            USER_NAME = ''
        print('15 - USER_NAME = ' + str(USER_NAME))

     #TEXT
        try:
            TEXT = clear_text(soup.find('div', 'css-g5mtbi-Text').get_text())
        except:
            TEXT = ''
        print('16 - TEXT = ' + str(TEXT[:70]))
 ###---------------------------------------------------------------------###
 ###------------------------------OLX/OTODOM-----------------------------###
 ###---------------------------------------------------------------------###

    if 'otodom.pl' in link:
        try:
            script = str(soup.find("script", {"id": "__NEXT_DATA__"}))
            start = '<script id="__NEXT_DATA__" type="application/json">'
            stop = '</script>'
            metadata_script = script.split(start)[1].split(stop)[0]
            json1 = json.loads(metadata_script)
        except:
            json1 = ''
        try:
            characteristics = json1["props"]["pageProps"]["ad"]["characteristics"]
        except:
            characteristics = ''

     #ADV_ID
        try:
            ADV_ID = json1["props"]["pageProps"]["ad"]["id"]
        except :
            ADV_ID = ''

        if ADV_ID == '' or ADV_ID == None:
            try:
                ADV_ID = json1["props"]["pageProps"]["adTrackingData"]["ad_id"]
            except:
                ADV_ID = ''
        print('\n01 - ADV_ID = ' + str(ADV_ID))

     #SELLER_ID
        try:
            SELLER_ID = json1["props"]["pageProps"]["ad"]["target"]["seller_id"]
        except:
            SELLER_ID = ''

        if SELLER_ID == '' or SELLER_ID == None:
            try:
                SELLER_ID = json1["props"]["pageProps"]["adTrackingData"]["seller_id"]
            except:
                SELLER_ID = ''
        print('02 - seller_id = ' + str(SELLER_ID))

     #SELLER_DIR
        try:
            SELLER_DIR = json1["props"]["pageProps"]["ad"]["publicId"]
        except:
            SELLER_DIR = ''
        print('03 - seller_dir = ' + str(SELLER_DIR))

     #PRICE
        try:
            PRICE = json1["props"]["pageProps"]["ad"]["target"]["Price"]
        except:
            PRICE = ''

        if PRICE == '' or PRICE == None:
            try:
                PRICE = json1["props"]["pageProps"]["adTrackingData"]["ad_price"]
            except:
                PRICE = ''

        if PRICE == '' or PRICE == None:
            try:
                for l in characteristics:
                    if 'Cena' in str(l):
                        PRICE = l["value"]
                        break
                    else: PRICE = ''
            except:
                PRICE = ''
        print('04 - PRICE = ' + str(PRICE))

     #CURRENCY
        try:
            CURRENCY = json1["props"]["pageProps"]["adTrackingData"]["price_currency"]
        except:
            CURRENCY = ''

        if CURRENCY == '' or CURRENCY == None:
            try:
                for l in characteristics:
                    if 'Cena' in str(l):
                        CURRENCY = l["currency"]
                        break
                    else: CURRENCY = ''
            except:
                CURRENCY = ''
        print('05 - CURRENCY = ' + str(CURRENCY))

     #URL
        try:
            URL = json1["props"]["pageProps"]["ad"]["url"]
        except:
            URL = ''
        print('07 - URL = ' + str(URL))

     #ADV_TITLE
        try:
            ADV_TITLE = clear_text(json1["props"]["pageProps"]["ad"]["title"])
        except:
            ADV_TITLE = ''
        print('09 - ADV_TITLE = ' + str(ADV_TITLE))

     #DATE1
        try:
            DATE1 = json1["props"]["pageProps"]["ad"]["dateCreated"]
        except:
            DATE1 = ''
        print('10 - DATE1 = ' + str(DATE1))

     #DATE2
        try:
            DATE2 = json1["props"]["pageProps"]["ad"]["dateModified"]
        except:
            DATE2 = ''
        print('11 - DATE2 = ' + str(DATE2))

     #CATEGORY
        try:
            CATEGORY = json1["props"]["pageProps"]["ad"]["category"]["name"][0]["value"]
        except:
            CATEGORY = ''
        print('12 - CATEGORY = ' + str(CATEGORY))

     #LOCATION
        try:
            LOCATION = json1["props"]["pageProps"]["ad"]["location"]["address"][0]["value"]
        except:
            LOCATION = ''
        print('13 - LOCATION = ' + str(LOCATION))

     #REGION
        try:
            REGION = json1["props"]["pageProps"]["ad"]["target"]["Province"]
        except:
            REGION = ''

        if REGION == '' or REGION == None:
            try:
                REGION = json1["props"]["pageProps"]["adTrackingData"]["region_name"]
            except:
                REGION = ''
        print('14 - region = ' + str(REGION))

     #SUBREGION
        try:
            SUBREGION = json1["props"]["pageProps"]["ad"]["target"]["Province"]
        except:
            SUBREGION = ''

        if SUBREGION == '' or SUBREGION == None:
            try:
                SUBREGION = json1["props"]["pageProps"]["adTrackingData"]["region_name"]
            except:
                SUBREGION = ''
        print('15 - subregion = ' + str(SUBREGION))

     #PHONE
        try:
            PHONE = clear_tel(json1["props"]["pageProps"]["ad"]["owner"]["phones"][0])
        except:
            PHONE = ''
        print('16 - PHONE = ' + str(PHONE))

     #USER_NAME
        try:
            USER_NAME = json1["props"]["pageProps"]["ad"]["owner"]["name"]
        except:
            USER_NAME = ''
        print('17 - USER_NAME = ' + str(USER_NAME))

     #TEXT
        try:
            TEXT = json1["props"]["pageProps"]["ad"]["description"]
            TEXT = clear_text(TEXT)
        except:
            TEXT = ''
        print('33 - TEXT = ' + str(TEXT[:70]))

 #CONTACT
    if TEXT != '' or TEXT != None:
        start = 'data-phone="'
        stop = '"'
        phone2 = []
        try:
            data_ = soup.find('div', 'css-g5mtbi-Text')
            phones = data_.find_all('span', 'spoilerHidden')
            for phone in phones:
                phone = str(phone)
                phone = phone.split(start)[1].split(stop)[0]
                phone = clear_tel(phone)
                phone2.append(phone)
            if len(phone2)>1:
                phone2 = ', '.join(phone2)
            else:
                phone2 = ''.join(phone2)
        except:
            phone2 = ''

        phone3 = []
        try:
            phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3})', TEXT)
            for phone in phones:
                phone = clear_tel(str(phone))
                phone3.append(phone)
            if len(phone3)>1:
                phone3 = ', '.join(phone3)
            else:
                phone3 = ''.join(phone3)
        except:
            phone3 = ''

        try:
            mail = re.findall(r'[\w\.-]+@[\w\.-]+', TEXT)
            if len(mail)>1:
                mail = ', '.join(mail)
            else:
                mail = ''.join(mail)
        except:
            mail = ''

        if phone2 != '' and phone3 != '':
            phone1 = phone2 + ', ' + phone3
        else:
            phone1 = phone2 + phone3

        if phone1 != '' and mail != '':
            CONTACT = phone1 + ' ' + mail
        else:
            CONTACT = phone1 + mail
    else:
        CONTACT = ''
    print('34 - CONTACT = ' + str(CONTACT))

    return [ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION]

def upload_url_list():
    source = path_to_data_now  + '\\Pages' + str(licznik) + '\\'
    lista_stron = []
    try:
        fList = os.listdir(source)
        for f in fList:
            if 'olx.pl' in f or 'otodom.pl' in f:
                for root, dirs, files in os.walk(source + f, topdown=False):
                    for file in files:
                        lista_stron.append(root + '\\'+ file)
    except:
        pass
    return lista_stron

def take_phone(URL, ADV_ID, DATE2, driver, tele_list, x):
    def download_phones():
        try:
            time.sleep(1)
            try:
                link_phone = driver.find_element_by_xpath('//button[@data-testid="show-phone"]')
                driver.execute_script("arguments[0].click();", link_phone)
                time.sleep(0.5)
            except:
                pass
            try:
                phone = driver.find_element_by_xpath('//li[@class="css-1petlhy-Text eu5v0x0"]').text
                phone = clear_tel(phone)
            except:
                phone = ''
        except:
            phone = ''
            pass
        return phone
    try:
        driver.set_page_load_timeout(30)
        driver.get(ADRES_OFERTY)
    except:
        driver.refresh()
        driver.get(ADRES_OFERTY)
    try:
        link = driver.find_element_by_css_selector('#onetrust-accept-btn-handler')
        link.click()
    except:
        pass
    phone = download_phones()
    print(phone)
    with open(tele_list, 'a') as phones_file:
        phones_file.write(str(x) + ';' + str(ADV_ID) + ';' + DATE2 + ';' + phone + '\n')
    return phone, phones_file

def check_files():
    wait_file = '_wait.txt'
    check_wait_file = False
    fileexist_path = home_path + 'check_duplicate' + '//'
    while check_wait_file == False:
        if os.path.exists(fileexist_path + wait_file):
            check_wait_file = False
            with tqdm(total=600, desc="waiting") as pbar:
                    for i in range(0,600):
                        time.sleep(1)
                        pbar.update(1)
                    pbar.close()
        else:
            check_wait_file = True
    open(fileexist_path + wait_file, 'w+')

    con = sqlite3.connect(home_path + date_now[:4] + '_project.db')
    con.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    cur = con.cursor()
    create_database(cur)

    try:
        open(fileexist_path + 'olx_otodom_' + date_now[:-2] + '.txt')
    except:
        check_file = open(fileexist_path + 'olx_otodom_' + date_now[:-2] + '.txt', 'w+')

    with open(fileexist_path + 'olx_otodom_' + date_now[:-2] + '.txt',"r") as check_file:
        read_data = check_file.readlines()
        check_file.close()
    data_list = list(set(read_data))
    if data_list == []:
        data_list.insert(0, 'test,test')
    return data_list, wait_file, con, cur, fileexist_path

def insert_data(ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, cur):
    cur.execute('INSERT INTO link_data VALUES(NULL, ?, ?, ?, ?);', (ADV_ID, URL, DATE1, DATE2))
    cur.execute("""SELECT id FROM link_data ORDER BY id DESC LIMIT 1""")
    last_elem = cur.fetchone()
    KeyId = last_elem[0]
    cur.execute('INSERT INTO seller_data VALUES(NULL, ?, ?, ?, ?, ?, ?);', (SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, KeyId))
    cur.execute('INSERT INTO adv_data VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, KeyId))

def internet_on():
    try:
        http = urllib3.PoolManager()
        status = False
        driver = ''
        while status == False:
            r = http.request('GET', 'http://216.58.192.142', timeout=1)
            if r.status == 200:
                status = True
            else:
                status = False
                try:
                    driver.quit()
                except:
                    pass
                time.sleep(60)
                driver = chrome_config()
    except:
        pass
    return True, driver

parser = ConfigParser()
try:
    parser.read('settings\\config_file.ini')
    home_path = parser.get('directories','home')
except:
    parser.read('..\\settings\\config_file.ini')
    home_path = parser.get('directories','home')

try:
    arg = sys.argv[1]
    licznik = arg
    program_log('[INFO*][olx_otodom]: Arguments passed properly.')
except:
    licznik = ''
    program_log("[ERROR!][olx_otodom]: Arguments's pass ERROR!.")

if licznik == '':
    try:
        licznik = str(int(parser.get('httrack','licznik')) - 1)
        program_log('[INFO*][olx_otodom] no pass arguments, try except.')
    except:
        program_log('[ERROR!][olx_otodom] pass arguments error! CRITICAL')
        exit()
date_now, downloaded_date = settime_olx_oto()
path_to_data_now = home_path + date_now

link_list = path_to_data_now + '\\linki_' + str(licznik) + '.txt'
tele_list = path_to_data_now + '\\tele_' + str(licznik) + '.txt'

try:
    fileslist = upload_url_list()
except:
    program_log('[ERROR!][olx_otodom] No files to read')
    exit()

data_list, wait_file, con, cur, fileexist_path = check_files()
driver = _myFirefoxDriver()
check_file = open(fileexist_path + 'olx_otodom_' + date_now[:-2] + '.txt',"a")
try:
    with tqdm(total=len(fileslist), desc="saving data") as pbar:
        for i in range(0,len(fileslist)):
            x = i + 1
            exists = False
            link = fileslist[i]
            try:
                ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION = download_data(link, downloaded_date)
                for data_line in data_list:
                    if str(ADV_ID) in data_line:
                        if str(DATE2) in data_line:
                            exists = True
                            break
                if exists == False:
                    check_file.write(str(x) + ':' + str(ADV_ID) + ';' + str(DATE2) + '\n')
                    if 'olx' in str(ADRES_OFERTY):
                        try:
                            PHONE, phones_file = take_phone(URL, ADV_ID, DATE2, driver, tele_list, str(x))
                        except:
                            pass
                    try:
                        insert_data(ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, cur)
                    except:
                        program_log('[ERROR!][olx_otodom]:' + str(x) + ':' + str(ADV_ID) + ';' + str(URL) + '\n')
                        pass
            except:
                program_log('[ERROR!][olx_otodom]: Link error: ' + link)
                pass
            pbar.update(1)
    try:
        phones_file.close()
    except:
        pass
    try:
        check_file.close()
    except:
        pass
    try:
        con.commit()
    except:
        pass
    try:
        driver.quit()
    except:
        pass
    try:
        os.remove(fileexist_path + wait_file)
    except:
        pass
except:
    try:
        phones_file.close()
    except:
        pass
    try:
        check_file.close()
    except:
        pass
    try:
        con.commit()
    except:
        pass
    try:
        driver.quit()
    except:
        pass
    try:
        os.remove(fileexist_path + wait_file)
    except:
        pass
    program_log('[ERROR!][olx_otodom] Data scrap error.')
exit()
