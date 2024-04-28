import requests
import sqlite3 as sql
import matplotlib.pyplot as plt
import json
from ratelimit import limits

'2013 Population Data Estimates from API'

# Insert into city_names table and associate with PRIMARY KEY id
def insert_city_name(curr, name):
    insert_query = 'INSERT OR IGNORE INTO city_names (name) VALUES (?)'
    curr.execute(insert_query, (name,))
    return curr.lastrowid

def insert_city_details(curr, name_id, latitude, longitude, population):
    insert_query = '''
    INSERT INTO city_details (name_id, latitude, longitude, population)
    VALUES (?, ?, ?, ?)
    '''
    curr.execute(insert_query, (name_id, latitude, longitude, population))

def insert_city(curr, name, lat, long, pop):
    name_id = insert_city_name(curr, f'{name}')
    insert_city_details(curr, name_id, lat, long, pop)

'-----------------------------------------------------------------------------'

# Using Function Decorator from ratelimit to limit the calls to 1 per second.
@limits(calls=1, period=1)
def get_data(num_rows) -> list:

    # Setup
    min_population = 10_000
    max_population = float('inf')
    url = f'https://api.api-ninjas.com/v1/city'
    api_key = 'f9ioqwD3isDTUd4smIvCQQ==F8pNPZYkeyZi7G1q'
    rows_per_call = 25
    headers = {'min_population': min_population, 'country': 'US', 'X-Api-Key': api_key, 'limit': rows_per_call}

    # Get first 25 rows from API
    resp = requests.get(url, headers)
    if resp.status_code == requests.codes.ok:
        # print(f"Type: {type(resp.text)}")
        # print(resp.text)
        # print("Got data from url")
        pass
    else:
        print("Error:", resp.status_code, resp.text)

    data = resp.json()
    # print(f"Type: {type(data)}")
    # print(data)


    # Loop to get 25 rows of data at a time
    while len(data) < num_rows:
        max_population = data[-1]['population']
        headers = {'min_population': min_population, 'max_population': max_population, 'country': 'US', 'X-Api-Key': api_key, 'limit': rows_per_call}
        resp = requests.get(url, headers)

        if resp.status_code == requests.codes.ok:
            # print(f"Type: {type(resp.text)}")
            # print(resp.text)
            # print("Got data from url")
            pass
        else:
            print("Error:", resp.status_code, resp.text)
        
        for d in resp.json():
            data.append(d)
    
    # Chop it so there's only a certain number that will be stored
    data = data[:num_rows]

    # print(f"Type: {type(data)}")
    # print(f"Num Cities: {len(data)}")
    # print(data)
    # for row in data:
    #     print(row)

    return data



'-----------------------------------------------------------------------------'

def main():

    conn = sql.connect('us_cities.db')
    curr = conn.cursor()

    # Create a table for city names
    create_city_names_table_query = '''
    CREATE TABLE IF NOT EXISTS city_names (
        name_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    '''
    curr.execute(create_city_names_table_query)

    # Create a table for city details
    create_city_details_table_query = '''
    CREATE TABLE IF NOT EXISTS city_details (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_id INTEGER,
        latitude REAL,
        longitude REAL,
        population INTEGER,
        FOREIGN KEY(name_id) REFERENCES city_names(name_id)
    );
    '''
    curr.execute(create_city_details_table_query)

    # Commit the changes
    conn.commit()

    cities_data: list = get_data(100)

    for d in cities_data:
        insert_city(curr, d['name'], d['latitude'], d['longitude'], d['population'])

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()