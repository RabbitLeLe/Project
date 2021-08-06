#-*- coding: utf-8 -*-
import datetime

def settime_get():
    teraz = datetime.datetime.now().replace(microsecond=0)
    now = str(teraz)
    ROK = now[:4]
    MIESIAC = now[5:7]
    DZIEN = now[8:10]
    GODZINA = now[11:19]
    GODZINA = GODZINA[0:2] + "_" + GODZINA[3:5] + "_" + GODZINA[6:8]
    DATE_NOW = ROK  + MIESIAC + DZIEN
    return DATE_NOW

def settime_olx_oto():
    teraz = datetime.datetime.now().replace(microsecond=0)
    now = str(teraz)
    ROK = now[:4]
    MIESIAC = now[5:7]
    DZIEN = now[8:10]
    DATE_NOW = ROK  + MIESIAC + DZIEN

    month = MIESIAC.replace('01', 'Sty').replace('02', 'Lut').replace('03', 'Mar').replace('04', 'Kwi').replace('05', 'Maj').replace('06', 'Cze').replace('07', 'Lip').replace('08', 'Sie').replace('09', 'Wrz').replace('10', 'Paź').replace('11', 'Lis').replace('12', 'Gru')
    downloaded_date = DZIEN + ' ' + month + ' ' + ROK

    return DATE_NOW, downloaded_date

def settime_grat():
    teraz = datetime.datetime.now().replace(microsecond=0)
    now = str(teraz)
    ROK = now[:4]
    MIESIAC = now[5:7]
    DZIEN = now[8:10]
    DATE_NOW = ROK  + MIESIAC + DZIEN
    dzisiaj = DZIEN + '-' + MIESIAC + '-' + ROK

    month = MIESIAC.replace('01', 'Sty').replace('02', 'Lut').replace('03', 'Mar').replace('04', 'Kwi').replace('05', 'Maj').replace('06', 'Cze').replace('07', 'Lip').replace('08', 'Sie').replace('09', 'Wrz').replace('10', 'Paź').replace('11', 'Lis').replace('12', 'Gru')
    downloaded_date = DZIEN + ' ' + month + ' ' + ROK

    wczoraj = datetime.date.today() - datetime.timedelta(days=1)
    wczoraj = str(wczoraj)
    ROK = wczoraj[:4]
    MIESIAC = wczoraj[5:7]
    DZIEN = wczoraj[8:10]
    wczoraj = DZIEN + '-' + MIESIAC + '-' + ROK
    return DATE_NOW, dzisiaj, wczoraj, downloaded_date