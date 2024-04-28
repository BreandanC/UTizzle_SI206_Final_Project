'SI206 Final Project'
"Emma's Portion"

import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
import re


        
def get_walk_data(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, 'html.parser')
    cities = soup.find_all('td', class_="city")
    walk = soup.find_all('td', class_="score")
    ret = {}
    for city, score in zip(cities, walk):
        city_name = city.get_text(strip=True)
        score_value = float(score.get_text(strip=True))
        ret[city_name] = score_value
    return ret

def create_tables():
    with sqlite3.connect('walkability_scores.db') as con:
        curr = con.cursor()
        curr.execute('''CREATE TABLE IF NOT EXISTS Cities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT UNIQUE
                        )''')
        curr.execute('''CREATE TABLE IF NOT EXISTS WalkabilityScores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city_id INTEGER,
                        score FLOAT,
                        FOREIGN KEY (city_id) REFERENCES Cities(id)
                        )''')

def make_data_base(data):
    with sqlite3.connect('walkability_scores.db') as con:
        curr = con.cursor()
        for city, score in data.items():
            # Insert or ignore new city
            curr.execute("INSERT OR IGNORE INTO Cities (city) VALUES (?)", (city,))
            # Get the city_id for the city
            curr.execute("SELECT id FROM Cities WHERE city = ?", (city,))
            city_id = curr.fetchone()[0]
            
            # Check if there's already a score for the city_id
            curr.execute("SELECT score FROM WalkabilityScores WHERE city_id = ?", (city_id,))
            existing_score = curr.fetchone()
            
            # If there's no existing score for the city_id, insert the new score
            if existing_score is None:
                curr.execute("INSERT INTO WalkabilityScores (city_id, score) VALUES (?, ?)", (city_id, score))
            else:
                # Update the score if it already exists
                curr.execute("UPDATE WalkabilityScores SET score = ? WHERE city_id = ?", (score, city_id))

# def drop_tables():
#     with sqlite3.connect('walkability_scores.db') as con:
#         curr = con.cursor()
#         curr.execute('DROP TABLE IF EXISTS WalkabilityScores')
#         curr.execute('DROP TABLE IF EXISTS Cities')

def main():
    # drop_tables()  # This will remove the existing tables
    create_tables()
    walk_data = get_walk_data('https://www.walkscore.com/cities-and-neighborhoods/')
    make_data_base(walk_data)

if __name__ == "__main__":
    main()
