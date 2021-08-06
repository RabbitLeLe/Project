#-*- coding: utf-8 -*-
try:
    from selenium import webdriver
    from configparser import ConfigParser
    import time, datetime
    import subprocess
    import os, sys
    sys.path.append('libraries')
    from _driver import _myChromeDriver
    from _logFile import program_log
    from _setTime import settime_get
except:
    sys.exit('[!] no required modules')

def file_structure(date):
    licznik1 = int(licznik_httrack)
    fileexist_path = home_path + date

    fileexist = os.path.exists(fileexist_path)
    if fileexist:
        pass
    else:
        os.mkdir(home_path + date)
        licznik1 = 1

    fileexist = os.path.exists(fileexist_path + '\\Pages' + str(licznik1))
    licznik2 = licznik1
    if fileexist:
        pass
    else:
        os.mkdir(fileexist_path + '\\Pages' + str(licznik1))
        licznik1 += 1
        parser['httrack']['licznik'] = str(licznik1)
        with open('settings//config_file.ini', 'w') as configfile:
            parser.write(configfile)
            configfile.close()
        pass
    return licznik2, fileexist_path

def downloadURLs(licznik, fileexist_path, site):

    def pages():
        if site == '1': #OLX
            olx_number_page = int(parser.get('page_number', 'olx_number_page')) + 1
            olx_page = ',https://www.olx.pl/nieruchomosci/?page='
            lista = olx_page.join(str(page) for page in range(0, olx_number_page))
            lista = lista[2:]
            lista = lista.split(',')
        if site == '2': #OTODOM
            otodom_number_page = int(parser.get('page_number', 'otodom_number_page')) + 1
            otodom_page = ',https://www.otodom.pl/wynajem/?search%5Border%5D=created_at_first%3Adesc&page='
            lista = otodom_page.join(str(page) for page in range(0, otodom_number_page))
            lista = lista[2:]
            lista = lista.split(',')
        if site == '3': #GRATKA #MORIZON #DOMIPORTA
            gratka_number_page = int(parser.get('page_number', 'gratka_number_page')) + 1
            gratka_page = ',https://www.gratka.pl/nieruchomosci/wynajem?sort=newest&page='

            morizon_number_page = int(parser.get('page_number', 'morizon_number_page')) + 1
            morizon_page = ',https://www.morizon.pl/do-wynajecia/nieruchomosci/najnowsze/?page='

            domiporta_number_page = int(parser.get('page_number', 'domiporta_number_page')) + 1
            domiporta_page = ',https://www.domiporta.pl/nieruchomosci/wynajme?SortingOrder=InsertionDate&PageNumber='
            lista = gratka_page.join(str(page) for page in range(0, gratka_number_page)) + morizon_page.join(str(page) for page in range(0, morizon_number_page)) + domiporta_page.join(str(page) for page in range(0, domiporta_number_page))
            lista = lista[2:].replace('500', '50')
            lista = lista.split(',')
        return lista

    lista_www = pages()
    driver = _myChromeDriver()
    output  = open(fileexist_path + '//linki_' + str(licznik) + '.txt', 'a')

    if site == '3': #GRATKA #MORIZON #DOMIPORTA
        fileupdate = os.path.exists(fileexist_path + '\\update_' + str(licznik) + '.txt')
        if fileupdate:
            pass
        else:
            update_file = open(fileexist_path + '\\update_' + str(licznik) + '.txt',"a")

    try:
        x = 0
        for item in range(0,len(lista_www)):
            link_enable = False
            y = 0
            while link_enable == False and y < 2:
                if y > 0:
                    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
                    time.sleep(1)
                try:
                    try:
                        driver.get(lista_www[item])
                    except:
                        try:
                            driver.execute_script("window.stop();")
                        except:
                            pass
                    try:
                        link = driver.find_element_by_css_selector('#onetrust-accept-btn-handler')
                        link.click()
                    except:
                        pass
                    time.sleep(1)
                    print(str(item + 1) + '/' + str(len(lista_www)) + ': ' + str(lista_www[item]))
                    if site == '1': #OLX
                        lista_ofert = driver.find_element_by_xpath('//table[@id="offers_table"]')
                        for i in lista_ofert.find_elements_by_xpath('.//tr[@class="wrap"]'):
                            try:
                                url = i.find_element_by_xpath('.//h3[@class="lheight22 margintop5"]')
                                url = url.find_element_by_xpath('a').get_attribute('href')
                                url_split = url.split('.html')
                                url = url_split[0] + '.html' + '\n'
                                output.write(url)
                            except:
                                pass
                    if site == '2': #OTODOM
                        lista_ofert = driver.find_element_by_xpath('//div[@class="listing"]')
                        for i in lista_ofert.find_elements_by_xpath('.//article[starts-with(@id, "offer-item-ad")]'):
                            try:
                                url = i.get_attribute('data-url')
                                url_split = url.split('.html')
                                url = url_split[0] + '.html' + '\n'
                                output.write(url)
                            except:
                                pass
                    if site == '3': #GRATKA #MORIZON #DOMIPORTA
                        if 'gratka' in lista_www[item]:
                            lista_ofert = driver.find_element_by_xpath('//div[@class="listing__content"]')
                            for i in lista_ofert.find_elements_by_xpath('.//article[starts-with(@class, "teaserUnified")]'):
                                try:
                                    url = i.get_attribute('data-href')
                                    try:
                                        info = i.find_element_by_xpath('.//ul[@class="teaserUnified__details"]')
                                        for data in info.find_elements_by_xpath('//li[@class="teaserUnified__info"]'):
                                            data = data.text
                                            if 'Aktualizacja' in data:
                                                update = data.replace('Aktualizacja: ', '').replace('.', '-')
                                                break
                                            else:
                                                update = 'None'
                                    except:
                                        update = 'None'
                                    x = x + 1
                                    update_file.write(str(x) + ';' + url + ';' + update + '\n')
                                    output.write(url + '\n')
                                except:
                                    pass
                        if 'morizon' in lista_www[item]:
                            try:
                                link =driver.find_element_by_xpath('//button[@class=" css-1hbsq6m"]')
                                link.click()
                            except:
                                pass
                            lista_ofert = driver.find_element_by_xpath('//div[@class="listingBox mainBox propertyListingBox content-box-main col-xs-9"]')
                            for i in lista_ofert.find_elements_by_xpath('.//div[@class="row row--property-list"]'):
                                try:
                                    x = i.find_element_by_xpath('.//section[@class="single-result__content single-result__content--height"]')
                                    y = x.find_element_by_xpath('.//a')
                                    url = y.get_attribute('href')
                                    if 'morizon.pl/oferta' in url:
                                        url = url + '\n'
                                        output.write(url)
                                except:
                                    pass
                        if 'domiporta' in lista_www[item]:
                            lista_ofert = driver.find_element_by_xpath('//ul[@class="grid"]')
                            for i in lista_ofert.find_elements_by_xpath('.//li[starts-with(@class, "grid-item grid-item--cover")]'):
                                try:
                                    x = i.find_element_by_xpath('.//figure[@class="sneakpeak__picture sneakpeak__picture--home"]')
                                    y = x.find_element_by_xpath('.//a[@class="sneakpeak__picture_container"]')
                                    url = y.get_attribute('href')
                                    url = url + '\n'
                                    output.write(url)
                                except:
                                    pass
                    link_enable = True
                except:
                    y = y + 1
                    time.sleep(2)
                    link_enable = False
                    program_log('[*] links download error:' + lista_www[item])
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
        try:
            update_file.close()
        except:
            pass
        try:
            driver.close()
            driver.quit()
        except:
            pass
        output.close()
        with open(fileexist_path + '//linki_' + str(licznik) + '.txt', 'r') as output:
            lines = sorted(output.readlines())
            output.close()
        with open(fileexist_path + '//linki_' + str(licznik) + '.txt', 'w') as output:
            for i in lines:
                output.write(i)
            output.close()
        program_log('[INFO*][get_download_offers] urls saved')
    except:
        try:
            driver.close()
            driver.quit()
        except:
            pass

def runhttrack(date_now, licznik):
    httName = home_path + date_now + '\\linki_' + str(licznik) + '.txt'
    outName = home_path + date_now + '\\Pages' + str(licznik)
    try:
        subprocess.run([httrack_path, '-%L', httName, '-O', outName, '-%v1 -r1 -%e0'])
        program_log('[INFO*][get_download_offers] offers downloaded')
    except:
        program_log('[ERROR!][get_download_offers] running httrack error')

def what_site():
    try:
        param = sys.argv[1]
    except:
        param = ''
    if 'olx' in param:
        site = '1'
    if 'otodom' in param:
        site = '2'
    if 'gratka' in param and 'morizon' in param and 'domiporta' in param:
        site = '3'
    if 'olx' not in param and 'otodom' not in param and 'gratka' not in param and 'morizon' not in param and 'domiporta' not in param:
        print(param)
        site = input('Set site param [1] - olx; [2] - otodom; [3] - gratka/morizon/domiporta\n')
    return site

def choose_download_data_app(site,  licznik):
    if site == '1' or site == '2':
        try:
            os.system(olx_otodom + ' ' + str(licznik))
        except:
            program_log('[ERROR!][get_download_offers] pass arguments error!')
            exit()
    if site == '3':
        try:
            os.system(gratka_mori_domi + ' ' + str(licznik))
        except:
            program_log('[ERROR!][get_download_offers] pass arguments error!')
            exit()
    if site != '1' and site != '2' and site != '3':
        program_log('[ERROR!][get_download_offers] choose app error!')
        exit()

parser = ConfigParser()
parser.read('settings\\config_file.ini')

home_path = parser.get('directories','home')
licznik_httrack = parser.get('httrack','licznik')
httrack_path = parser.get('httrack','httrack_path')
olx_otodom = parser.get('directories','olx_otodom')
gratka_mori_domi = parser.get('directories','gratka_mori_domi')

site = what_site()
date_now = settime_get()
licznik, fileexist_path = file_structure(date_now)
downloadURLs(licznik, fileexist_path, site)
runhttrack(date_now, licznik)
os.system('cls')
choose_download_data_app(site, licznik)