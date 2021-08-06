#-*- coding: utf-8 -*-
import sqlite3

def create_database(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS link_data (
                        id INTEGER PRIMARY KEY ASC,
                        adv_id varchar(20) NOT NULL,
                        url varchar(255) NOT NULL,
                        date1 varchar(50),
                        date2 varchar(50)
                        )""")

    cur.executescript("""CREATE TABLE IF NOT EXISTS seller_data (
                        id INTEGER PRIMARY KEY ASC,
                        seller_id INTEGER(15),
                        seller_dir varchar(150),
                        user_name varchar(150),
                        phone varchar(100),
                        contact varchar(150),
                        KeyId INTEGER,
                        FOREIGN KEY(KeyId) REFERENCES link_data(id)
                        )""")

    cur.executescript("""CREATE TABLE IF NOT EXISTS adv_data (
                        id INTEGER PRIMARY KEY ASC,
                        adv_title varchar(200),
                        category varchar(100),
                        text varchar,
                        price varchar(20),
                        currency varchar(5),
                        location varchar(150),
                        region varchar(100),
                        subregion varchar(100)
                        KeyId INTEGER,
                        FOREIGN KEY(KeyId) REFERENCES link_data(id)
                        )""")