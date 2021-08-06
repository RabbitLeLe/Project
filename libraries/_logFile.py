#-*- coding: utf-8 -*-
import datetime

def program_log(log_text):
    event_time = str(datetime.datetime.now().replace(microsecond=0))
    log_file = open('log_file.log', "a")
    log_file.write(event_time + '>' + log_text + '\n')
    log_file.close()