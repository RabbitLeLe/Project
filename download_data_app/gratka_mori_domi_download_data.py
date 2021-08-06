#-*- coding: utf-8 -*-
try:
    from bs4 import BeautifulSoup
    from configparser import ConfigParser
    from tqdm import tqdm
    import time
    import os
    import sqlite3
    import json
    import sys
    sys.path.append('libraries')
    from _clear import clear_tel, clear_text
    from _logFile import program_log
    from _setTime import settime_grat
    from _dataBase import create_database
except:
    print('[!][gratka_mori_domi] no required modules')
    time.sleep(5)

def download_data(link, dzisiaj, wczoraj, downloaded_date ):
    with open(link, "r", encoding='utf-8', errors='ignore') as f:
        contents = f.read()
        soup = BeautifulSoup(contents,"html.parser")

    if 'gratka.pl' in link:
        li = soup.find('ul', 'parameters__rolled').find_all('li')
        scripts = soup.find_all("script")
        try:
            for script in scripts:
                if 'PPDataLayer.push({"typ' in str(script):
                    s = str(script)
                    start = 'PPDataLayer.push({'
                    stop = '});'
                    metadata_script1 = s.split(start)[1].split(stop)[0]
                    metadata_script1 = '{' + metadata_script1 + '}'
                    break
                else: metadata_script1 = ''
            json1 = json.loads(metadata_script1)
        except:
            json1 = ''
        try:
            for script in scripts:
                if '"@type":"BreadcrumbList"' in str(script):
                    s = str(script)
                    start = '<script type="application/ld+json">'
                    stop = '</script>'
                    metadata_script2 = s.split(start)[1].split(stop)[0]
                    break
                else: metadata_script2 = ''
            json2 = json.loads(metadata_script2)
        except:
            json2 = ''

     #ADV_ID
        try:
            ADV_ID = json1["id_oferty"]
        except:
            ADV_ID = ''

        if ADV_ID == '' or ADV_ID == None:
            try:
                ADV_ID = link.split('\\')[-1].split('.')[0]
            except:
                ADV_ID = ''
        print('\n01 - ADV_ID = ' + str(ADV_ID))

     #SELLER_ID
        try:
            SELLER_ID = soup.find_all('a', 'offerOwner__link')
            if len(SELLER_ID) > 2:
                SELLER_ID = SELLER_ID[1].get('href')
            else:
                SELLER_ID = ''

            if SELLER_ID.find('dom.gratka.pl') == -1:
                SELLER_ID = ''
            else:
                SELLER_ID = SELLER_ID[-7:SELLER_ID.index('.html')]
        except:
            SELLER_ID = ''
        print('02 - SELLER_ID = ' + str(SELLER_ID))

     #PRICE
        try:
            PRICE = json1["cena"]
        except:
            PRICE = ''

        if PRICE == '' or PRICE == None:
            try:
                PRICE = clear_text(soup.find('span', 'priceInfo__value').get_text()).strip(). replace('zł/miesiąc', '')
            except:
                PRICE = ''
        print('03 - PRICE = ' + str(PRICE))

     #CURRENCY
        try:
            CURRENCY = clear_text(soup.find('span', 'priceInfo__currency').get_text()).strip(). replace('/miesiąc', '')
        except:
            CURRENCY = ''
        print('04 - CURRENCY = ' + str(CURRENCY))

     #URL
        try:
            URL = link.split('gratka.pl')[1].split('.')[0]
            URL = 'https://gratka.pl' + URL
        except:
            URL = ''
        print('05 - URL = ' + str(URL))

     #ADV_TITLE
        try:
            ADV_TITLE = clear_text(soup.title.get_text()).split('-')[0]
        except:
            ADV_TITLE = ''
        print('07 - ADV_TITLE = ' + str(ADV_TITLE))

     #DATE1
        DATE1 = ''
        print('08 - DATE1 = ' + str(DATE1))

     #DATE2
        DATE2 = ''
        print('09 - DATE2 = ' + str(DATE2))

     #CATEGORY
        try:
            CATEGORY = json2["itemListElement"][2]["item"]["name"]
        except:
            CATEGORY = ''

        if CATEGORY == '' or CATEGORY == None:
            try:
                CATEGORY = soup.find_all('a', 'breadcrumb__link')[2].get('title')
            except:
                CATEGORY = ''
        print('10 - CATEGORY = ' + str(CATEGORY))

     #LOCATION
        try:
            for LOCATION in li:
                if 'Lokalizacja' in str(LOCATION):
                    LOCATION = clear_text(LOCATION.find('b', 'parameters__value').get_text())
                    break
        except:
            LOCATION = ''
        print('11 - LOCATION = ' + str(LOCATION))

     #REGION
        try:
            REGION = LOCATION.split(',')[-1]
        except:
            REGION = ''

        if REGION == '' or REGION == None:
            try:
                REGION = json1["region"]
            except:
                REGION = ''
        print('12 - REGION = ' + str(REGION))

     #SUBREGION
        try:
            SUBREGION = LOCATION.split(',')[0]
        except:
            SUBREGION = ''

        if SUBREGION == '' or SUBREGION == None:
            try:
                SUBREGION = json1["miejscowosc"]
            except:
                SUBREGION = ''
        print('13 - SUBREGION = ' + str(SUBREGION))

     #PHONE
        try:
            PHONE = soup.find_all('a', 'phoneButton__button')
            a = ''
            for row in PHONE:
                if len(a) == 0:
                    a = clear_tel(row.get('data-full-phone-number'))
                else:
                    a += ', ' + clear_tel(row.get('data-full-phone-number'))
            PHONE = a
        except:
            PHONE = ''
        print('14 - PHONE = ' + str(PHONE))

     #USER_NAME
        try:
            USER_NAME = soup.find('h3', 'offerOwner__person').get_text()
        except:
            USER_NAME = ''
        print('15 - USER_NAME = ' + str(USER_NAME))

     #SELLER_DIR
        try:
            SELLER_DIR = soup.find('a', 'offerOwner__link').get('href')
        except:
            SELLER_DIR = ''
        print('17 - SELLER_DIR = ' + str(SELLER_DIR))

     #TEXT
        try:
            TEXT = clear_text(soup.find('div', 'description__rolled ql-container').get_text().replace('\xca', ''))
        except:
            TEXT = ''
        print('18 - TEXT = ' + str(TEXT[0:70]))

 ###---------------------------------------------------------------------###
 ###------------------------------GRATKA/MORIZON-------------------------###
 ###---------------------------------------------------------------------###

    if 'morizon.pl' in link:
        exists_offer = True
        try:
            if soup.find('div', 'exclamation').h2.get_text().find('jest już nieaktualne') > -1:
                print('Advertisment unavaible.\n')
                exists_offer = False
                pass
        except:
            pass

        if exists_offer == True:
            tr = soup.find_all('tr')
            scripts = soup.find_all("script")
            for script in scripts:
                if 'layer.push({"property":' in str(script):
                    s = str(script)
                    start = "__layer.push({"
                    stop = "});"
                    metadata_script1 = s.split(start)[1].split(stop)[0]
                    metadata_script1 = '{' + metadata_script1 + '}'
                    break
                else: metadata_script1 = ''
            try:
                json1 = json.loads(metadata_script1)
            except:
                json1 = ''

         #ADV_ID
            try:
                for ADV_ID in tr:
                    if 'Numer oferty' in str(ADV_ID):
                        ADV_ID = ADV_ID.find('td').get_text().replace('\n', '').replace(' ', '')
                        break
                    else:
                        ADV_ID = ''
            except:
                ADV_ID = ''
            print('\n01 - ADV_ID = ' + str(ADV_ID))

         #SELLER_ID
            try:
                SELLER_ID = json1["company"]["crm_id"]
            except:
                try:
                    SELLER_ID = soup.find('div', 'companyName').a.get('href').split('-')[-1]
                except:
                    SELLER_ID = ''
            print('02 - SELLER_ID = ' + str(SELLER_ID))

         #PRICE
            try:
                PRICE = json1["property"]["price"]
            except:
                PRICE = ''

            if PRICE == '' or PRICE == None:
                try:
                    PRICE = soup.find('li', 'paramIconPrice').em.text.replace('~', '')
                except:
                    PRICE = ''
            print('03 - PRICE = ' + str(PRICE))

         #CURRENCY
            try:
                CURRENCY = soup.find('li', 'paramIconPrice').em.span.text
            except:
                CURRENCY = ''
            print('04 - CURRENCY = ' + str(CURRENCY))

         #URL
            try:
                URL = link.split('www.morizon.pl')[1].split('.')[0]
                URL = 'https://www.morizon.pl' + URL
            except:
                URL = ''
            print('05 - URL = ' + str(URL))

         #ADV_TITLE
            ADV_TITLE = clear_text(soup.title.string)
            ADV_TITLE = ADV_TITLE[0:ADV_TITLE.find('|')]
            print('06 - ADV_TITLE = ' + str(ADV_TITLE))

         #DATE1
            try:
                DATE1 = soup.find('meta', {'itemprop': 'name'}).get('content')
                DATE1 = DATE1[DATE1.find(':') + 1: ].strip()
            except:
                DATE1 = ''

            if DATE1 == '' or DATE1 == None:
                try:
                    for DATE1 in tr:
                        if 'Opublikowano' in str(DATE1):
                            DATE1 = DATE1.find('td').get_text().replace('\n', '').replace('<strong>', '').replace('</strong>', '')
                            if 'wczoraj' in str(DATE1):
                                DATE1 = wczoraj
                            if 'dzisiaj' in str(DATE1):
                                DATE1 = dzisiaj
                            break
                        else:
                            DATE1 = ''
                except:
                    DATE1 = ''
            DATE1 = DATE1.replace('stycznia', '01').replace('lutego', '02').replace('marca', '03').replace('kwietnia', '04').replace('maja', '05').replace('czerwca', '06').replace('lipca', '07').replace('sierpnia', '08').replace('września', '09').replace('października', '10').replace('listopada', '11').replace('grudnia', '12').replace(' ', '-')
            print('07 - DATE1 = ' + str(DATE1))

         #DATE2
            try:
                for DATE2 in tr:
                    if 'Zaktualizowano' in str(DATE2):
                        DATE2 = DATE2.find('td').get_text().replace('\n', '').replace('<strong>', '').replace('</strong>', '')[:-1]
                        if 'wczoraj' in str(DATE2):
                            DATE2 = wczoraj
                        if 'dzisiaj' in str(DATE2):
                            DATE2 = dzisiaj
                        break
                    else:
                        DATE2 = ''
            except:
                DATE2 = ''
            DATE2 = DATE2.replace('stycznia', '01').replace('lutego', '02').replace('marca', '03').replace('kwietnia', '04').replace('maja', '05').replace('czerwca', '06').replace('lipca', '07').replace('sierpnia', '08').replace('września', '09').replace('października', '10').replace('listopada', '11').replace('grudnia', '12').replace(' ', '-')
            if len(DATE2) < 10:
                DATE2 = '0' + DATE2
            print('08 - DATE2 = ' + str(DATE2))

         #CATEGORY
            try:
                CATEGORY = soup.find('div', 'summaryTypeTransaction clearfix').get_text().strip()
            except:
                CATEGORY = ''
            print('09 - CATEGORY = ' + str(CATEGORY))

         #LOCATION
            try:
                LOCATION = clear_text(soup.find('div', 'col-xs-9').h1.strong.get_text())
            except:
                LOCATION = ''
            print('10 - LOCATION = ' + str(LOCATION))

         #REGION
            try:
                REGION = json1["property"]["province"]
            except:
                REGION = ''

            if REGION == '' or REGION == None:
                try:
                    REGION = soup.find('nav', 'breadcrumbs').get_text()
                    REGION = REGION[REGION.find('', REGION.index(' ', REGION.index(' ') + 1) + 1):REGION.find('', REGION.index(' ', REGION.index(' ', REGION.index(' ') + 1) + 1) + 1)].strip()
                except:
                    REGION = ''
            print('11 - REGION = ' + str(REGION))

         #SUBREGION
            try:
                SUBREGION = json1["property"]["city"]
            except:
                SUBREGION = ''

            if SUBREGION == '' or SUBREGION == None:
                try:
                    SUBREGION = soup.find('nav', 'breadcrumbs').get_text()
                    SUBREGION = SUBREGION[
                        SUBREGION.find('', SUBREGION.index(' ', SUBREGION.index(' ', SUBREGION.index(' ') + 1) + 1) + 1):
                        SUBREGION.find('', SUBREGION.index(' ', SUBREGION.index(' ', SUBREGION.index(' ', SUBREGION.index(' ') + 1) + 1) + 1) + 1)].strip()
                except:
                    SUBREGION = ''
            print('12 - SUBREGION = ' + str(SUBREGION))

         #PHONE
            try:
                PHONE = clear_tel(soup.find('span', 'phone hidden').get_text())
            except:
                PHONE = ''
            print('13 - PHONE = ' + str(PHONE))

         #USER_NAME
            try:
                USER_NAME = soup.find('div', 'agentName').get_text()
            except:
                try:
                    USER_NAME = soup.find('div', 'agentName').a.get_text()
                except:
                    USER_NAME = ''

            if USER_NAME == '' or USER_NAME == None:
                try:
                    USER_NAME = json1["property"]["ownership"]
                except:
                    try:
                        USER_NAME = soup.find('div', 'companyName').a.get_text()
                    except:
                        try:
                            USER_NAME = soup.find('div', 'companyName').a.get('href').split('/')[-1]
                        except:
                            USER_NAME = ''
            USER_NAME = USER_NAME.replace('\n', '')
            print('14 - USER_NAME = ' + str(USER_NAME))

         #SELLER_DIR
            try:
                SELLER_DIR = soup.find('div', 'agentName').a.get('href')
            except:
                try:
                    SELLER_DIR = soup.find('div', 'companyName').a.get('href')
                except:
                    SELLER_DIR = ''
            print('15 - SELLER_DIR = ' + str(SELLER_DIR))

         #TEXT
            try:
                TEXT = clear_text(soup.find('div', 'description').get_text())
            except: TEXT = ''
            print('16 - TEXT = ' + str(TEXT[0:70]))

 ###---------------------------------------------------------------------###
 ###------------------------------MORIZON/DOMIPORTA----------------------###
 ###---------------------------------------------------------------------###

    if 'domiporta.pl' in link:
        li = soup.find('ul', 'features__list-2').find_all('li')
        scripts = soup.find_all("script")
        for script in scripts:
            if 'var userHash' in str(script) or "(location.hostname.indexOf('localhost') === -1 && location.hostname.indexOf('test') === -1)" in str(script):
                s = str(script).replace('\n', '').replace(' ', '').replace("'mailHash':userHash!=null&&userHash!=''?userHash:'',", '').replace("'",'"')
                start = "dataLayer=[{"
                stop = "}];}</script>"
                metadata_script1 = s.split(start)[1].split(stop)[0]
                break
            else: metadata_script1 = ''
        metadata_script1 = '{' + metadata_script1 + '}'
        try:
            json1 = json.loads(metadata_script1)
        except:
            json1 = ''

     #ADV_ID
        try:
            ADV_ID = ((link.split('\\'))[-1].split('.'))[0]
        except:
            ADV_ID = ''

        if ADV_ID == '' or ADV_ID == None:
            try:
                ADV_ID = json1["advertId"]
            except:
                ADV_ID = ''
        print('\n01 - ADV_ID = ' + str(ADV_ID))

     #SELLER_ID
        try:
            SELLER_ID = json1["sadvertiserId"]
        except:
            SELLER_ID = ''

        if SELLER_ID == '' or SELLER_ID == None:
            try:
                SELLER_ID = soup.find('input', {'id': 'UserId'}).get('value')
            except:
                SELLER_ID = ''
        print('02 - SELLER_ID = ' + str(SELLER_ID))

     #PRICE
        try:
            PRICE = json1["price"]
        except:
            PRICE = ''

        if PRICE == '' or PRICE == None:
            try:
                for PRICE in li:
                    if 'Cena' in str(PRICE):
                        PRICE = clear_text(PRICE.p.get_text()).replace(' ', '').replace('zł', '')
                        break
                    else:
                        PRICE = ''
            except:
                PRICE = ''
        print('03 - PRICE = ' + str(PRICE))

     #CURRENCY
        try:
            CURRENCY = soup.find('span', {'itemprop': 'priceCurrency'}).get_text().replace(' ', '')
        except:
            CURRENCY = ''
        print('04 - CURRENCY = ' + str(CURRENCY))

     #URL
        try:
            URL = link.split('www.domiporta.pl')[1].split('.')[0]
            URL = 'www.domiporta.pl' + URL
        except:
            URL = ''
        print('05 - URL = ' + str(URL))

     #ADV_TITLE
        ADV_TITLE = clear_text(soup.title.get_text())
        ADV_TITLE = ADV_TITLE[:ADV_TITLE.find('-')]
        print('06 - ADV_TITLE = ' + str(ADV_TITLE))

     #DATE1
        DATE1 = ''
        print('07 - DATE1 = ' + str(DATE1))

     #DATE2
        DATE2 = ''
        print('08 - DATE2 = ' + str(DATE2))

     #CATEGORY
        try:
            for CATEGORY in li:
                if 'Kategoria' in str(CATEGORY):
                    CATEGORY = clear_text(CATEGORY.a.get_text())
                    break
                else:
                    CATEGORY = ''
        except:
            CATEGORY = ''
        print('09 - CATEGORY = ' + str(CATEGORY))

     #LOCATION
        try:
            LOCATION = soup.find('span', {'itemprop': 'address'}).find_all('span')
            a = ''
            for row in LOCATION:
                if len(a) == 0:
                    a += row.text
                else:
                    a += ', ' + row.text
            LOCATION = a
        except:
            LOCATION = ''
        print('10 - LOCATION = ' + str(LOCATION))

     #REGION
        try:
            REGION = json1["region"]
        except:
            REGION = ''

        if REGION == '' or REGION == None:
            try:
                REGION = soup.find('meta', {'itemprop': 'addressRegion'}).get('content')
            except:
                REGION = ''
        print('11 - REGION = ' + str(REGION))

     #SUBREGION
        try:
            SUBREGION = json1["city"]
        except:
            SUBREGION = ''

        if SUBREGION == '' or SUBREGION == None:
            try:
                SUBREGION = soup.find('span', {'itemprop': 'addressLocality'}).get_text()
            except:
                SUBREGION = ''
        print('12 - SUBREGION = ' + str(SUBREGION))

     #PHONE
        try:
            PHONE = clear_tel(soup.find('div', 'agent__phone agent__phone_normal details-databox__phone-number').a.get('data-tel'))
        except:
            PHONE = ''
        print('13 - PHONE = ' + str(PHONE))

     #USER_NAME
        try:
            USER_NAME = soup.find('p', 'details-databox__name details-databox__name--bold').get_text()
        except:
            USER_NAME = ''
        print('14 - USER_NAME = ' + str(USER_NAME))

     #SELLER_DIR
        try:
            SELLER_DIR = soup.find('span', 'agnecy__info_title agnecy__info_title--arrow agnecy__info_title--arrow-right').get("onclick").split(';')[-1].split("'")[1]
            SELLER_DIR = 'https://www.domiporta.pl' + SELLER_DIR
        except:
            SELLER_DIR = ''
        print('15 - SELLER_DIR = ' + str(SELLER_DIR))

     #TEXT
        try:
            TEXT = clear_text(soup.find('div', 'description__panel').get_text().replace('\xca', ''))
        except:
            TEXT = ''
        print('16 - TEXT = ' + str(TEXT[0:70]))

 #CONTACT
    if TEXT != '' or TEXT != None:
        phone1 = []
        try:
            phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3})', TEXT)
            for phone in phones:
                phone = clear_tel(str(phone))
                phone1.append(phone)
            if len(phone1)>1:
                phone1 = ', '.join(phone1)
            else:
                phone1 = ''.join(phone1)
        except:
            phone1 = ''

        try:
            mail = re.findall(r'[\w\.-]+@[\w\.-]+', TEXT)
            if len(mail)>1:
                mail = ', '.join(mail)
            else:
                mail = ''.join(mail)
        except:
            mail = ''

        if phone1 != '' and mail != '':
            CONTACT = phone1 + ' ' + mail
        else:
            CONTACT = phone1 + mail
    else:
        CONTACT = ''
    print('17 - CONTACT = ' + str(CONTACT))

    return [ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION]

def upload_url_list():
    source = path_to_data_now  + '\\Pages' + str(licznik) + '\\'
    lista_stron = []
    try:
        fList = os.listdir(source)
        for f in fList:
            if 'gratka' in f or 'morizon' in f or 'domiporta' in f:
                for root, dirs, files in os.walk(source + f, topdown=False):
                    for file in files:
                        lista_stron.append(root + '\\'+ file)
    except:
        pass
    return lista_stron

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
        open(fileexist_path + 'gratka_mori_domi_' + date_now[:-2] + '.txt')
    except:
        check_file = open(fileexist_path + 'gratka_mori_domi_' + date_now[:-2]+ '.txt', 'w+')

    with open(fileexist_path + 'gratka_mori_domi_' + date_now[:-2] + '.txt',"r") as check_file:
        read_data = check_file.readlines()
        check_file.close()
    data_list = list(set(read_data))
    if data_list == []:
        data_list.insert(0, 'test,test')

    try:
        with open(update_list,"r") as update_file:
            read_data = update_file.readlines()
            update_file.close()
        update_file = list(set(read_data))
        if update_file == []:
            update_file.insert(0, 'www.gratka.pl,None')
    except:
        update_file = ''

    return data_list, wait_file, con, cur, fileexist_path, update_file

def insert_data(ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, cur):
    cur.execute('INSERT INTO link_data VALUES(NULL, ?, ?, ?, ?);', (ADV_ID, URL, DATE1, DATE2))
    cur.execute("""SELECT id FROM link_data ORDER BY id DESC LIMIT 1""")
    last_elem = cur.fetchone()
    KeyId = last_elem[0]
    cur.execute('INSERT INTO seller_data VALUES(NULL, ?, ?, ?, ?, ?, ?);', (SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, KeyId))
    cur.execute('INSERT INTO adv_data VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, KeyId))

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
    program_log('[INFO*][gratka_mori_domi]: Arguments passed properly.')
except:
    licznik = ''
    program_log("[ERROR!][gratka_mori_domi]: Arguments's pass ERROR!.")

if licznik == '':
    try:
        licznik = parser.get('httrack','licznik') - 1
        program_log('[INFO*][gratka_mori_domi] No pass arguments, try except.')
    except:
        program_log('[ERROR!][gratka_mori_domi] Pass arguments error! CRITICAL')
        exit()
date_now, dzisiaj, wczoraj, downloaded_date = settime_grat()
path_to_data_now = home_path + date_now

update_list = path_to_data_now + '\\update_' + str(licznik) + '.txt'
updated_list = path_to_data_now + '\\updated_' + str(licznik) + '.txt'

try:
    fileslist = upload_url_list()
except:
    program_log('[ERROR!][gratka_mori_domi] No files to read')
    exit()

data_list, wait_file, con, cur, fileexist_path, update_file = check_files()
check_file = open(fileexist_path + 'gratka_mori_domi_' + date_now[:-2] + '.txt',"a")
try:
    with tqdm(total=len(fileslist), desc="saving data") as pbar:
        for i in range(0,len(fileslist)):
            x = i + 1
            exists = False
            link = fileslist[i]
            try:
                ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION = download_data(link, dzisiaj, wczoraj, downloaded_date )
                if 'gratka.pl' in str(URL):
                    try:
                        for data_line in update_file:
                            if str(ADV_ID) in data_line:
                                DATE2 = data_line.split(';')[2].replace('\n', '')
                                break
                    except:
                        pass
                for data_line in data_list:
                    if str(URL) in data_line:
                        if str(DATE2) in data_line:
                            exists = True
                            break
                if exists == False:
                    check_file.write(str(x) + ':' + str(URL) + ';' + str(DATE2) + '\n')
                    try:
                        insert_data(ADV_ID, URL, DATE1, DATE2, SELLER_ID, SELLER_DIR, USER_NAME, PHONE, CONTACT, ADV_TITLE, CATEGORY, TEXT, PRICE, CURRENCY, LOCATION, REGION, SUBREGION, cur)
                    except:
                        program_log('[ERROR!][gratka_mori_domi]: Insert problem: ' + str(x) + ':' + str(ADV_ID) + ';' + str(URL) + '\n')
                        pass
            except:
                program_log('[ERROR!][gratka_mori_domi]: Link problem: ' + link)
                pass
            pbar.update(1)
        os.rename(update_list, updated_list)
    try:
        check_file.close()
    except:
        pass
    try:
        con.commit()
    except:
        pass
    try:
        os.remove(fileexist_path + wait_file)
    except:
        pass
except:
    try:
        check_file.close()
    except:
        pass
    try:
        con.commit()
    except:
        pass
    try:
        os.remove(fileexist_path + wait_file)
    except:
        pass
    program_log('[ERROR!][gratka_mori_domi] Data scrap general problem.')
exit()
