import sqlite3
import requests
import json
import os
from secrets import GAODE_API_KEY

DBNAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'main.db'
)

def create_relative_tb():
    con = sqlite3.connect(DBNAME)
    c=con.cursor()
    c.execute("DROP TABLE IF EXISTS 'relative_side_info'")
    c.execute('''
        CREATE TABLE relative_side_info(
            tb_idx Integer primary key AUTOINCREMENT,
            ID TEXT,
            NAME TEXT,
            AGE Integer,
            GENDER TEXT,
            HEIGHT FLOAT,
            WEIGHT FLOAT,
            LOCATION TEXT,
            CONTACT TEXT,
            HEALTH_COND TEXT,
            PHOTO TEXT,
            FOREIGN KEY (LOCATION) REFERENCES coordinate_info);
        ''')
    con.commit()
    con.close()

def create_rescue_tb():
    con = sqlite3.connect(DBNAME)
    c=con.cursor()
    c.execute("DROP TABLE IF EXISTS 'rescue_side_info'")
    c.execute('''
        CREATE TABLE rescue_side_info(
            tb_idx Integer primary key AUTOINCREMENT,
            ID TEXT,
            NAME TEXT,
            AGE Integer,
            GENDER TEXT,
            HEIGHT FLOAT,
            LOCATION TEXT,
            CONTACT TEXT,
            CONDITION TEXT,
            PHOTO TEXT,
            FOREIGN KEY (LOCATION) REFERENCES coordinate_info);
        ''')
    con.commit()
    con.close()

def create_coordinate_tb():
    con = sqlite3.connect(DBNAME)
    c=con.cursor()
    c.execute("DROP TABLE IF EXISTS 'coordinate_info'")
    c.execute('''
        CREATE TABLE coordinate_info(
            LOCATION TEXT,
            LATITUDE FLOAT,
            LONGITUDE FLOAT);
        ''')
    contents = get_places_dict()
    provinces = contents['districts'][0]['districts']
    for province in provinces:
        province_name = province['name']
        province_center = province['center']
        latitude, altitude = province_center.split(',')
        latitude = float(latitude)
        altitude = float(altitude)
        insertion = (province_name, latitude, altitude)
        statement = 'INSERT INTO "coordinate_info"'
        statement += 'VALUES(?, ?, ?)'
        c.execute(statement, insertion)

        # getting info for cities
        province_cities = province['districts']
        for city in province_cities:
            city_name = city['name']
            city_center = city['center']
            latitude, altitude = city_center.split(',')
            latitude = float(latitude)
            altitude = float(altitude)

            insertion = (city_name, latitude, altitude)
            statement = 'INSERT INTO "coordinate_info"'
            statement += 'VALUES(?, ?, ?)'
            c.execute(statement, insertion)

            # getting info for counties
            city_counties = city['districts']
            for county in city_counties:
                county_name = county['name']
                county_center = county['center']
                latitude, altitude = county_center.split(',')
                latitude = float(latitude)
                altitude = float(altitude)

                insertion = (county_name, latitude, altitude)
                statement = 'INSERT INTO "coordinate_info"'
                statement += 'VALUES(?, ?, ?)'
                c.execute(statement, insertion)

    con.commit()
    con.close()

def get_places_dict():
    params = {'keywords':'中国', 'key': GAODE_API_KEY, 'subdistrict': 3, 'extensions':"base"}
    url = "https://restapi.amap.com/v3/config/district?"
    resp = requests.get(url, params=params)
    resp.encoding='utf-8'
    text = resp.text  # dictionary
    content = json.loads(text)
    return content

if __name__=='__main__':
    create_relative_tb()
    create_rescue_tb()
    create_coordinate_tb()
