import sqlite3
import requests

def create_db_and_table(db_name):
    # establish connection to db
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    # make unique columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AirQuality (
        location TEXT,
        parameter TEXT,
        value REAL,
        date_utc TEXT,
        date_local TEXT,
        unit TEXT,
        latitude REAL,
        longitude REAL,
        country TEXT,
        UNIQUE(location, parameter, date_utc, value)
    )
    ''')
    connection.commit()
    return connection

def fetch_air_quality_data(api_url):
    #get data from api
    response = requests.get(api_url)
    data = response.json()
    return data

def insert_data(connection, data, max_insertions):
    #insert data into db
    cursor = connection.cursor()

    insert_stmt = '''
    INSERT OR IGNORE INTO AirQuality (
        location,
        parameter,
        value,
        date_utc,
        date_local,
        unit,
        latitude,
        longitude,
        country
    ) VALUES (?,?,?,?,?,?,?,?,?)
    '''
    
    insertion_counter = 0

    for entry in data['results']:
        if insertion_counter >= max_insertions:
            break
        
        cursor.execute(insert_stmt, (
            entry['location'],
            entry['parameter'],
            entry['value'],
            entry['date']['utc'],
            entry['date']['local'],
            entry['unit'],
            entry['coordinates']['latitude'],
            entry['coordinates']['longitude'],
            entry['country']
        ))
        #insertion checker
        if cursor.rowcount > 0:
            insertion_counter += 1

    connection.commit()

def main():
    #max inserts
    max_insertions_per_run = 25
    #db name
    database_name = 'FinalProject_v2.db'
    #api link
    api_url = "https://api.openaq.org/v1/measurements?date_from=2024-04-22T00%3A00%3A00Z&date_to=2024-04-29T17%3A47%3A00Z&limit=100&page=1&sort=desc&parameter_id=2&country=US&sensor_type=low-cost%20sensor"

    connection = create_db_and_table(database_name)
    data = fetch_air_quality_data(api_url)
    insert_data(connection, data, max_insertions_per_run)
    connection.close()

if __name__ == "__main__":
    main()