from bs4 import BeautifulSoup
import requests
import json
import secrets  # file that contains your API key
import final_project_code
import time
import sqlite3

DB_NAME = 'umich_library_restaurant.sqlite'

# Part 1: Create a dictionary to save all the needed information

library_url_dict = final_project_code.build_library_url_dict()
# print(library_url_dict)
library_info_dict = {}

for key, value in library_url_dict.items():
    library_info = final_project_code.get_library_instance(value)
    library_info_dict[key] = {'name': library_info.name, 
                              'location': library_info.location, 
                              'intro': library_info.intro, 
                              'nearby_restaurants': final_project_code.get_nearby_restaurants(library_info)['businesses']
                              }
    # print(library_info_dict[key])

# Part 2: Create databse with two tables

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_library_sql = 'DROP TABLE IF EXISTS "Libraries"'
    drop_restaurant_sql = 'DROP TABLE IF EXISTS "Restaurants"'
    
    create_libraries_sql = '''
        CREATE TABLE IF NOT EXISTS "Libraries" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT, 
            "Name" TEXT NOT NULL,
            "Location" TEXT NOT NULL, 
            "Intro" TEXT NOT NULL
        )
    '''
    create_restaurants_sql = '''
        CREATE TABLE IF NOT EXISTS 'Restaurants'(
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Nearby_library_Id' INTEGER NOT NULL,
            'Address' TEXT NOT NULL,
            'Rating' TEXT NOT NULL,
            'Phone' TEXT NOT NULL,
            'URL' TEXT NOT NULL
        )
    '''
    cur.execute(drop_library_sql)
    
    cur.execute(drop_restaurant_sql)
    
    cur.execute(create_libraries_sql)
    
    cur.execute(create_restaurants_sql)
    
    conn.commit()
    conn.close()


def load_libraries():

    insert_library_sql = '''
        INSERT INTO Libraries
        VALUES (NULL, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
        
    for key, value in library_info_dict.items():
        cur.execute(insert_library_sql,
            [
                value['name'],
                value['location'],
                value['intro']
            ]
        )

    conn.commit()
    conn.close()


def load_restaurants(): 

    select_library_id_sql = '''
        SELECT Id FROM Libraries
        WHERE Name = ?
    '''

    insert_restaurant_sql = '''
        INSERT INTO Restaurants
        VALUES (NULL, ?, ?, ?, ?, ?, ?)
    '''

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for k, v in library_info_dict.items():

        cur.execute(select_library_id_sql, [v['name']])
        res = cur.fetchone()
        Nearby_library_Id = None
        if res is not None:
            Nearby_library_Id = res[0]
        
        for item in v['nearby_restaurants']:
            cur.execute(insert_restaurant_sql,
                [
                    item['name'],
                    Nearby_library_Id,
                    item['location']['display_address'][0],
                    item['rating'],
                    item['display_phone'],
                    item['url']
                ]
            )
    conn.commit()
    conn.close()

create_db()
load_libraries()
load_restaurants()
